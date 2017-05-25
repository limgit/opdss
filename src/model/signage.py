import json
from pathlib import Path

import jinja2
from enum import Enum, auto

from controller import manager
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from model.template import SceneTemplate


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
    def __init__(self, template: SceneTemplate, duration: int=10, transition: TransitionType=TransitionType.NONE,
                 schedule: Schedule=None, values=None):
        if schedule is None:
            schedule = Schedule(ScheduleType.ALWAYS_VISIBLE)

        if values is None:
            values = dict()

        self._template = template
        self._duration = duration
        self._transition = transition
        self._schedule = schedule
        self._values = values


class Frame:
    pass


class Signage:
    def __init__(self, manifest_path: Path,
                 obj_mng: 'manager.ObjectManager'=None,
                 tmp_mng: 'manager.TemplateManager'=None):
        self._manifest_dir = manifest_path

        # create new signage if not exists
        if not manifest_path.exists():
            self._title = ''
            self._description = ''
            self._frame = None
            self._scene = []

            self.save()

            return

        # load from the signage file
        with manifest_path.open() as f:
            dct = json.load(f)

        self._title = dct['title']
        self._description = dct['description']
        self._frame = None  # todo: needs to implement frame related contents
        self._scene = []

        for scene_value in dct['scene']:
            self._scene.append(Scene(tmp_mng.get_scene_template(scene_value['id']),
                                     scene_value['duration'],
                                     TransitionType[scene_value['transition']],
                                     None,  # todo
                                     scene_value['data'])
                               )

    def save(self) -> None:
        return  # todo: write contents back to the file

    def render(self) -> str:
        dirs = [str(x._template._root_dir) for x in self._scene]
        dirs.append(str(self._manifest_dir.parent))

        templates = [str(x._template._root_dir.stem) + '.html' for x in self._scene]
        durations = [x._duration for x in self._scene]

        data = {str(x._template._root_dir.stem): x._values for x in self._scene}

        env = Environment(
            loader=FileSystemLoader(dirs)
        )

        template = env.get_template('index.html')

        return template.render(_durations=durations, _templates=templates, **data)
