import os

from typing import Optional

import copy
import json
from collections import deque
from pathlib import Path

from model.data_type import ObjectDataType, ListDataType, STR_TO_PRIMITIVE_TYPE, DataType
from model.data_value import ObjectValue
from model.signage import Signage, Scene, TransitionType, Frame
from model.template import SceneTemplate, FrameTemplate


class ObjectManager:
    def __init__(self, dir_root: Path):
        self._dir_root = dir_root
        self._object_types = dict()
        self._object_values = dict()
        self.load_all()

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

            print('{} loaded'.format(new_type._name))

    def load_object_type(self, type_id: str, data: dict) -> ObjectDataType:
            # populate raw fields values to real python objects
            if 'fields' in data.keys():
                fields = {}
                for field_id, field_value in data['fields'].items():
                    try:
                        fields[field_id] = self.dict_to_type(field_value[2])
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
        new_object = ObjectValue(object_id, data_type)

        for field_id, field_value in data.items():
            field_type = data_type._fields[field_id]

            if isinstance(field_type, ObjectDataType):
                field_value = self.get_object_value(field_type, field_value)
            elif isinstance(field_type, ListDataType) and isinstance(field_type._data_type, ObjectDataType):
                field_value = [self.get_object_value(field_type._data_type, x) for x in field_value]

            new_object.set_value(field_id, field_value)

        return new_object

    def get_object_type(self, type_id: str) -> ObjectDataType:
        return self._object_types[type_id]

    def get_object_value(self, type_instance: ObjectDataType, value_id: str) -> ObjectValue:
        return self._object_values[type_instance][value_id]

    def add_object_value(self, new_object: ObjectValue) -> None:
        object_dir = self._dir_root / new_object.data_type._id

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


class MultimediaManager:
    pass


class TemplateManager:
    def __init__(self, dir_root: Path, obj_mng: ObjectManager):
        self._dir_root = dir_root
        self._obj_mng = obj_mng
        self._scene_templates = dict()
        self._frame_templates = dict()
        self.load_all()

    def load_all(self) -> None:
        # load scenes
        scene_path = self._dir_root / 'scene'
        scenes_dir = [x for x in scene_path.iterdir() if x.is_dir()]

        for scene_tpl_id, scene_dir in [(x.name, x) for x in scenes_dir]:
            with (scene_dir / 'manifest.json').open() as f:
                self._scene_templates[scene_tpl_id] = SceneTemplate(scene_tpl_id,
                                                                  self._obj_mng.load_object_type('', json.load(f)),
                                                                  scene_dir)
                print('{} loaded'.format(self._scene_templates[scene_tpl_id].definition._name))

        # load frames
        frame_path = self._dir_root / 'frame'
        frames_dir = [x for x in frame_path.iterdir() if x.is_dir()]

        for frame_tpl_id, frame_dir in [(x.name, x) for x in frames_dir]:
            with (frame_dir / 'manifest.json').open() as f:
                self._frame_templates[frame_tpl_id] = FrameTemplate(frame_tpl_id,
                                                                    self._obj_mng.load_object_type('', json.load(f)),
                                                                    frame_dir)
                print('{} loaded'.format(self._frame_templates[frame_tpl_id].definition._name))

    def get_scene_template(self, key: str) -> SceneTemplate:
        return self._scene_templates[key]

    def get_frame_template(self, key: str) -> FrameTemplate:
        return self._frame_templates[key]


class SignageManager:
    def __init__(self, dir_root: Path, obj_mng: ObjectManager, tpl_mng: TemplateManager):
        self._tpl_mng = tpl_mng
        self._obj_mng = obj_mng
        self._dir_root = dir_root
        self._signages = dict()
        self.load_all()

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

                scenes.append(Scene(scene_template,
                                    scene_data,
                                    scene_value['duration'],
                                    TransitionType[scene_value['transition']],
                                    None  # todo
                                    )
                              )
            # load a frame
            frame_value = dct['frame']
            frame_template = self._tpl_mng.get_frame_template(frame_value['id'])
            frame_data = self._obj_mng.load_object_value(None, frame_template.definition, frame_value['data'])
            frame = Frame(frame_template, frame_data)

            self._signages[signage_id] = Signage(signage_id, signage_mnf.parent,
                                                 dct['title'], dct['description'], frame, scenes)
            print('{} loaded'.format(self._signages[signage_id]._title))

    def get_signage(self, key: str) -> Signage:
        return self._signages[key]

    def add_signage(self, key: str, signage: Signage):
        pass
