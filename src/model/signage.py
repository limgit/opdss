import json
from datetime import time
from pathlib import Path

from enum import Enum, auto
from typing import Callable, Tuple, List

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from model.data_value import ObjectValue
from model.template import SceneTemplate, FrameTemplate
from utils import utils


class ScheduleType(Enum):
    ALWAYS_VISIBLE = auto()
    ALWAYS_HIDDEN = auto()
    VISIBLE_ON_TIME = auto()
    HIDDEN_ON_TIME = auto()


class TransitionType(Enum):
    NONE = auto()
    PUSH = auto()
    FADE = auto()


class Schedule:
    def __init__(self, schedule_type: ScheduleType):
        self._type = schedule_type
        self._from = time(0, 0, 0)
        self._to = time(23, 59, 59)
        self._day_of_week = [True] * 7  # Mon ~ Sun

        self._on_change_handler = lambda: None

    @property
    def type(self) -> ScheduleType:
        return self._type

    @type.setter
    def type(self, new_type: ScheduleType) -> None:
        self._type = new_type
        self._on_change_handler()

    @property
    def from_time(self) -> time:
        return self._from

    @from_time.setter
    def from_time(self, new_time: time) -> None:
        self._from = new_time
        self._on_change_handler()

    @property
    def to_time(self) -> time:
        return self._to

    @to_time.setter
    def to_time(self, new_time: time) -> None:
        self._to = new_time
        self._on_change_handler()

    @property
    def day_of_week(self) -> List[bool]:
        return self._day_of_week[:]  # return copied value

    @day_of_week.setter
    def day_of_week(self, new_value: List[bool]) -> None:
        if not len(new_value) == 7:
            raise AttributeError()

        self._day_of_week = new_value
        self._on_change_handler()

    @property
    def on_value_change(self) -> None:
        raise ValueError  # don't try to access!

    @on_value_change.setter
    def on_value_change(self, handler: Callable[[None], None]) -> None:
        self._on_change_handler = handler

    def to_dict(self) -> dict:
        return {
            "type": self.type.name,
            "from": '{}:{}:{}'.format(self._from.hour, self._from.minute, self._from.second),
            "to": '{}:{}:{}'.format(self._to.hour, self._to.minute, self._to.second),
            "day_of_week": self.day_of_week
        }


class Scene:
    def __init__(self, template: SceneTemplate, object_value: ObjectValue, duration: int=10,
                 transition: TransitionType=TransitionType.NONE,
                 schedule: Schedule=None):
        if schedule is None:
            schedule = Schedule(ScheduleType.ALWAYS_VISIBLE)

        self._template = template
        self._duration = duration
        self._transition = transition
        self._schedule = schedule
        self._values = object_value
        self._on_change_handler = lambda: None

        def object_value_change_handler():
            self._on_change_handler()

        self._values.on_value_change = object_value_change_handler
        self._schedule.on_value_change = object_value_change_handler

    @property
    def template(self) -> SceneTemplate:
        return self._template

    @template.setter
    def template(self, new_template: SceneTemplate) -> None:
        self._template = new_template
        self._values = ObjectValue(None, new_template.definition, None)
        self._on_change_handler()

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, new_value: int) -> None:
        if new_value < 0:
            raise AttributeError()

        self._duration = new_value
        self._on_change_handler()

    @property
    def transition_type(self) -> TransitionType:
        return self._transition

    @transition_type.setter
    def transition_type(self, new_value: TransitionType) -> None:
        self._transition = new_value
        self._on_change_handler()

    @property
    def schedule(self) -> Schedule:
        return self._schedule

    @property
    def values(self) -> ObjectValue:
        return self._values

    @property
    def on_value_change(self) -> None:
        raise ValueError  # don't try to access!

    @on_value_change.setter
    def on_value_change(self, handler: Callable[[None], None]) -> None:
        self._on_change_handler = handler

    def to_dict(self) -> dict:
        return {
            "id": self.template.id,
            "duration": self.duration,
            "transition": self.transition_type.name,
            "scheduling": self._schedule.to_dict(),
            "data": self.values.get_values(False)
        }


class Frame:
    def __init__(self, template: FrameTemplate, object_value: ObjectValue):
        self._template = template
        self._values = object_value
        self._on_change_handler = lambda: None

        def object_value_change_handler():
            self._on_change_handler()

        self._values.on_value_change = object_value_change_handler

    @property
    def template(self) -> FrameTemplate:
        return self._template

    @template.setter
    def template(self, new_template: FrameTemplate) -> None:
        self._template = new_template
        self._values = new_template.definition.default
        self._on_change_handler()

    @property
    def values(self) -> ObjectValue:
        return self._values

    @property
    def on_value_change(self) -> None:
        raise ValueError  # don't try to access!

    @on_value_change.setter
    def on_value_change(self, handler: Callable[[None], None]) -> None:
        self._on_change_handler = handler

    def to_dict(self) -> dict:
        return {
            "id": self.template.id,
            "data": self.values.get_values(False)
        }


class Signage:
    def __init__(self, signage_id: str, title: str= '',
                 description: str='', frame: Frame=None, scenes=None):
        if scenes is None:
            scenes = []

        self._id = ''
        self._title = title
        self._description = description
        self._frame = frame
        self._scenes = []

        self._id_change_handler = lambda x, y: None
        self._value_change_handler = lambda: None

        self.id = signage_id  # validate new id

        for scene in scenes:
            self.add_scene(scene)

        self._frame.on_value_change = self._handler_wrapper

    def _handler_wrapper(self):
        self._value_change_handler()

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        utils.validate_id(new_id)

        old_id = self._id
        self._id = new_id
        self._id_change_handler(old_id, new_id)
        self._value_change_handler()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str) -> None:
        self._title = new_title

        self._value_change_handler()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_value: str) -> None:
        self._description = new_value

        self._value_change_handler()

    @property
    def scenes(self) -> Tuple[Scene]:
        return tuple(self._scenes)

    @property
    def frame(self) -> Frame:
        return self._frame

    @property
    def on_id_change(self) -> None:
        raise ValueError  # don't try to access!

    # (old_id, new_id)
    @on_id_change.setter
    def on_id_change(self, handler: Callable[[str, str], None]) -> None:
        self._id_change_handler = handler

    @property
    def on_value_change(self) -> None:
        raise ValueError  # don't try to access!

    @on_value_change.setter
    def on_value_change(self, handler: Callable[[None], None]) -> None:
        self._value_change_handler = handler

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "frame": self.frame.to_dict(),
            "scenes": [x.to_dict() for x in self.scenes]
        }

    def add_scene(self, new_scene: Scene) -> None:
        new_scene.on_value_change = self._handler_wrapper
        self._scenes.append(new_scene)
        self._value_change_handler()

    def remove_scene(self, to_delete: Scene) -> None:
        to_delete.on_value_change = lambda: None
        self._scenes.remove(to_delete)

    def rearrange_scene(self, index_1: int, index_2: int) -> None:
        self._scenes[index_1], self._scenes[index_2] = self._scenes[index_2], self._scenes[index_1]
        self._value_change_handler()

    def render(self, resource_dir: Path) -> str:
        dirs = [str(x.template.root_dir) for x in self._scenes]  # for scene template resources
        dirs.append(str(self._frame.template.root_dir))  # for frame template resources
        dirs.append(str(resource_dir))  # for index.html

        scenes = [str(x.template.root_dir.stem) + '.html' for x in self._scenes]
        frame = (str(self._frame.template.root_dir.stem) + '.html')

        schedules = [json.dumps(x.schedule.to_dict()) for x in self._scenes]
        durations = [x.duration for x in self._scenes]

        data = {str(x.template.root_dir.stem): x.values.get_values() for x in self._scenes}
        data[str(self._frame.template.root_dir.stem)] = self._frame.values.get_values()

        env = Environment(
            loader=FileSystemLoader(dirs)
        )

        template = env.get_template('index.html')

        print(data)

        return template.render(_schedules=schedules, _durations=durations, _scenes=scenes, _frame=frame, **data)
