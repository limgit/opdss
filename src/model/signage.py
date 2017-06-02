from pathlib import Path

from enum import Enum, auto
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from model.data_value import ObjectValue
from model.template import SceneTemplate, FrameTemplate


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
    def __init__(self, type: ScheduleType):
        pass  # todo: mock initializer


class Scene:
    def __init__(self, template: SceneTemplate, object_value: ObjectValue, duration: int=10, transition: TransitionType=TransitionType.NONE,
                 schedule: Schedule=None):
        if schedule is None:
            schedule = Schedule(ScheduleType.ALWAYS_VISIBLE)

        self._template = template
        self._duration = duration
        self._transition = transition
        self._schedule = schedule
        self._values = object_value


class Frame:
    def __init__(self, template: FrameTemplate, object_value: ObjectValue):
        self._template = template
        self._values = object_value


class Signage:
    def __init__(self, signage_id: str, resource_dir: Path, title: str='', description: str='', frame: Frame=None, scenes=None):
        if scenes is None:
            scenes = []

        self._id = signage_id
        self._resource_dir = resource_dir
        self._title = title
        self._description = description
        self._frame = frame
        self._scenes = scenes

    def render(self) -> str:
        dirs = [str(x._template._root_dir) for x in self._scenes]  # for scene template resources
        dirs.append(str(self._frame._template._root_dir))  # for frame template resources
        dirs.append(str(self._resource_dir))  # for index.html

        scenes = [str(x._template._root_dir.stem) + '.html' for x in self._scenes]
        frame = (str(self._frame._template._root_dir.stem) + '.html')

        durations = [x._duration for x in self._scenes]

        data = {str(x._template._root_dir.stem): x._values.get_dict() for x in self._scenes}
        data[str(self._frame._template._root_dir.stem)] = self._frame._values.get_dict()

        env = Environment(
            loader=FileSystemLoader(dirs)
        )

        template = env.get_template('index.html')

        print(data)

        return template.render(_durations=durations, _scenes=scenes, _frame=frame, **data)
