import os
from datetime import time

from typing import Optional, Dict, Callable

import copy
import json
from collections import deque
from pathlib import Path

from model.data_type import ObjectDataType, ListDataType, STR_TO_PRIMITIVE_TYPE, DataType, FileDataType
from model.data_value import ObjectValue, FileValue
from model.signage import Signage, Scene, TransitionType, Frame, Schedule, ScheduleType
from model.template import SceneTemplate, FrameTemplate

import webserver.logger


class MultimediaManager:
    def __init__(self, root_dir: Path):
        self._root_Dir = root_dir
        self._image_type = FileDataType(root_dir / 'image')
        self._video_type = FileDataType(root_dir / 'video')
        self._images = dict()
        self._videos = dict()

    def load_all(self) -> None:
        image_files = self._image_type.root_dir.iterdir()
        video_files = self._video_type.root_dir.iterdir()

        for image_file in image_files:
            self.add_image(image_file)

        for video_file in video_files:
            self.add_video(video_file)

    def add_image(self, new_file_path: Path):
        # if new file is out of the media folder, copy the file to the media folder.
        if not new_file_path.parent.resolve().samefile(self._image_type.root_dir.parent):
            pass  # todo: copy file

        new_image = FileValue(self._image_type, new_file_path.name)

        def id_change_handler(old_name, new_name):
            pass  # todo: if new_image.file_name is changed, rename the file in the media folder.

        new_image.on_id_change = id_change_handler

        self._images[new_image.file_name] = new_image

    def add_video(self, new_file_path: Path):
        pass  # todo

    # todo: add getter of image/video_type and images/videos and remove_image/video(self, to_delete: FileValue)


class ObjectManager:
    def __init__(self, dir_root: Path):
        self._dir_root = dir_root
        self._object_types = dict()
        self._object_values = dict()
        self.load_all()

    @property
    def object_types(self) -> Dict[str, ObjectDataType]:
        return copy.copy(self._object_types)

    def get_object_type(self, type_id: str) -> ObjectDataType:
        return self._object_types[type_id]

    def get_object_value(self, type_instance: ObjectDataType, value_id: str) -> ObjectValue:
        return self._object_values[type_instance][value_id] if value_id else None

    def get_object_values(self, type_instance: ObjectDataType) -> Dict[str, ObjectValue]:
        return copy.copy(self._object_values[type_instance])

    def load_all(self) -> None:
        types_dir = [x for x in self._dir_root.iterdir() if x.is_dir()]

        # todo: currently, a method to handle dependency problem is awful.
        # -> if a dependency problem occurs, just postpone that type.
        # in worst case, infinite loop could be occurred!
        type_queue = deque([(x.name, x) for x in types_dir])
        while type_queue:
            current_type = type_queue.popleft()
            type_id, type_dir = current_type

            # initialize new object type
            with (type_dir / 'manifest.json').open() as f:
                mnf_contents = json.load(f)
                new_type = self.load_object_type(type_id, mnf_contents)

            if not new_type:
                type_queue.append(current_type)
                continue

            self._object_types[type_id] = new_type

            # loads object values
            self._object_values[new_type] = dict()

            for value_id, value_path in [(x.stem, x) for x in type_dir.glob('*.json')]:
                if value_id == 'manifest':
                    continue

                with value_path.open() as f:
                    new_object = self.load_object_value(value_id, new_type, json.load(f))

                self.add_object_value(new_object)
            # print('{} loaded'.format(new_type._name))
            log_level = 1
            log1 = webserver.logger.Logger(new_type.name, 1, log_level)

    def load_object_type(self, type_id: str, data: dict) -> ObjectDataType:
        # populate raw fields values to real python objects
        if 'fields' in data.keys():
            fields = {}
            for field_id, field_value in data['fields'].items():
                try:
                    fields[field_id] = (self.dict_to_type(field_value[2]), field_value[0], field_value[1])
                except KeyError:
                    return None

            data['fields'] = fields

        new_type = ObjectDataType(type_id=type_id, **data)

        return new_type

    def dict_to_type(self, json_data: dict) -> DataType:
        target_type = json_data['type']
        type_params = copy.deepcopy(json_data)
        del type_params['type']

        if target_type[0] == '[':
            split_index = target_type.find(']')
            type_prefix = target_type[1:split_index]
            type_postfix = target_type[split_index + 1:]

            list_min, list_max = [int(x) for x in type_prefix.split(',')]
            type_params['type'] = type_postfix
            type_instance = ListDataType(self.dict_to_type(type_params), list_min, list_max)
        elif target_type[0] == '$':
            type_id = target_type[1:]
            type_instance = self.get_object_type(type_id)
        else:
            type_instance = STR_TO_PRIMITIVE_TYPE[target_type](**type_params)

        return type_instance

    def load_object_value(self, object_id: Optional[str], data_type: ObjectDataType, data: dict) -> ObjectValue:
        new_object = ObjectValue(object_id, data_type, self)

        for field_id, field_value in data.items():
            new_object.set_value(field_id, field_value)

        return new_object

    def add_object_value(self, new_object: ObjectValue) -> None:
        object_dir = self._dir_root / new_object.data_type.id

        def id_change_handler(old_id, new_id):
            del self._object_values[new_object.data_type][old_id]
            self._object_values[new_object.data_type][new_id] = new_object

            os.remove(str(object_dir / (old_id + '.json')))
            # todo: find references and update them. it should be hard work! :weary:

        def value_change_handler():
            with (object_dir / (new_object.id + '.json')).open('w') as f:
                f.write(json.dumps(new_object.get_values(False)))

        new_object.on_id_change = id_change_handler
        new_object.on_value_change = value_change_handler

        self._object_values[new_object.data_type][new_object.id] = new_object


class TemplateManager:
    def __init__(self, dir_root: Path, obj_mng: ObjectManager):
        self._dir_root = dir_root
        self._obj_mng = obj_mng
        self._scene_templates = dict()
        self._frame_templates = dict()
        self.load_all()

    @property
    def scene_templates(self) -> Dict[str, SceneTemplate]:
        return copy.copy(self._scene_templates)

    @property
    def frame_templates(self) -> Dict[str, FrameTemplate]:
        return copy.copy(self._frame_templates)

    def get_scene_template(self, key: str) -> SceneTemplate:
        return self._scene_templates[key]

    def get_frame_template(self, key: str) -> FrameTemplate:
        return self._frame_templates[key]

    def load_all(self) -> None:
        # load scenes
        scene_path = self._dir_root / 'scene'
        scenes_dir = [x for x in scene_path.iterdir() if x.is_dir()]

        for scene_tpl_id, scene_dir in [(x.name, x) for x in scenes_dir]:
            with (scene_dir / 'manifest.json').open() as f:
                self._scene_templates[scene_tpl_id] = SceneTemplate(scene_tpl_id,
                                                                    self._obj_mng.load_object_type('', json.load(f)),
                                                                    scene_dir)

                webserver.logger.Logger(self._scene_templates[scene_tpl_id].definition.name, 2, 2)

        # load frames
        frame_path = self._dir_root / 'frame'
        frames_dir = [x for x in frame_path.iterdir() if x.is_dir()]

        for frame_tpl_id, frame_dir in [(x.name, x) for x in frames_dir]:
            with (frame_dir / 'manifest.json').open() as f:
                self._frame_templates[frame_tpl_id] = FrameTemplate(frame_tpl_id,
                                                                    self._obj_mng.load_object_type('', json.load(f)),
                                                                    frame_dir)

                webserver.logger.Logger(self._frame_templates[frame_tpl_id].definition.name, 2, 3)


class SignageManager:
    def __init__(self, dir_root: Path, obj_mng: ObjectManager, tpl_mng: TemplateManager):
        self._tpl_mng = tpl_mng
        self._obj_mng = obj_mng
        self._dir_root = dir_root
        self._signages = dict()
        self.load_all()

    @property
    def signages(self) -> Dict[str, Signage]:
        return copy.copy(self._signages)

    def get_signage(self, key: str) -> Signage:
        return self._signages[key]

    def load_all(self) -> None:
        for signage_id, signage_mnf in [(x.stem, x) for x in self._dir_root.glob('*.json')]:

            # load from the signage file
            with signage_mnf.open() as f:
                dct = json.load(f)

            # load scenes
            scenes = []
            for scene_value in dct['scenes']:
                scene_template = self._tpl_mng.get_scene_template(scene_value['id'])
                scene_data = self._obj_mng.load_object_value(None, scene_template.definition, scene_value['data'])

                schedule_value = scene_value['scheduling']
                scene_schedule = Schedule(ScheduleType[schedule_value['type']])

                if 'from' in schedule_value.keys():
                    scene_schedule.from_time = time(*[int(x) for x in schedule_value['from'].split(':')])

                if 'to' in schedule_value.keys():
                    scene_schedule.to_time = time(*[int(x) for x in schedule_value['to'].split(':')])

                if 'day_of_week' in schedule_value.keys():
                    scene_schedule.date_of_week = schedule_value['day_of_week']

                scenes.append(Scene(scene_template,
                                    scene_data,
                                    scene_value['duration'],
                                    TransitionType[scene_value['transition']],
                                    scene_schedule
                                    )
                              )
            # load a frame
            frame_value = dct['frame']
            frame_template = self._tpl_mng.get_frame_template(frame_value['id'])
            frame_data = self._obj_mng.load_object_value(None, frame_template.definition, frame_value['data'])
            frame = Frame(frame_template, frame_data)

            new_signage = Signage(signage_id, signage_mnf.parent, dct['title'], dct['description'], frame, scenes)
            self.add_signage(new_signage)

            webserver.logger.Logger(new_signage.title, 3, 4)

    def add_signage(self, new_signage: Signage) -> None:
        signage_path = self._dir_root / (new_signage.id + '.json')

        def id_change_handler(old_id, new_id):
            del self._signages[old_id]
            self._signages[new_id] = new_signage

            os.remove(str(signage_path))

        def value_change_handler():
            with signage_path.open('w') as f:
                f.write(json.dumps(new_signage.to_dict()))

        new_signage.on_id_change = id_change_handler
        new_signage.on_value_change = value_change_handler

        self._signages[new_signage.id] = new_signage


class ChannelManager:
    from model.channel import Channel  # due to cyclic import problem, import Channel class locally.

    def __init__(self, root_path: Path, sgn_mng: SignageManager):
        self._root_path = root_path
        self._channels = dict()
        self._sgn_mng = sgn_mng

        self._refresh_event_handler = lambda channel: None
        self._count_event_handler = lambda channel: 0

        self.load_all()

    @property
    def root_path(self) -> Path:
        return self._root_path

    @property
    def channels(self) -> Dict[str, Channel]:
        return copy.copy(self._channels)

    @property
    def refresh_event_handler(self) -> Callable[['Channel'], None]:
        return self._refresh_event_handler

    @refresh_event_handler.setter
    def refresh_event_handler(self, new_handler: Callable[['Channel'], None]) -> None:
        self._refresh_event_handler = new_handler

    @property
    def count_event_handler(self) -> Callable[['Channel'], int]:
        return self._count_event_handler

    @count_event_handler.setter
    def count_event_handler(self, new_handler: Callable[['Channel'], int]) -> None:
        self._count_event_handler = new_handler

    def get_channel(self, channel_id: str) -> Channel:
        return self._channels[channel_id]

    def load_all(self):
        for channel_id, channel_file in [(x.stem, x) for x in self._root_path.glob('*.json')]:
            # load from the signage file
            with channel_file.open() as f:
                dct = json.load(f)

            from model.channel import Channel
            new_channel = Channel(channel_id, dct['description'], self._sgn_mng.get_signage(dct['signage']))
            self.add_channel(new_channel)

    def add_channel(self, new_channel: Channel) -> None:
        def id_change_handler(channel, old_id):
            channel_path = self._root_path / (old_id + '.json')

            del self._channels[old_id]
            self._channels[channel.id] = channel

            os.remove(str(channel_path))

        def value_change_handler(channel):
            channel_path = self._root_path / (channel.id + '.json')

            with channel_path.open('w') as f:
                f.write(json.dumps(channel.to_dict()))

        new_channel.id_change_handler = id_change_handler
        new_channel.value_change_handler = value_change_handler
        new_channel.refresh_event_handler = lambda channel: self._refresh_event_handler(channel)
        new_channel.count_event_handler = lambda channel: self._count_event_handler(channel)

        self._channels[new_channel.id] = new_channel

    def remove_channel(self, to_delete: Channel):
        pass