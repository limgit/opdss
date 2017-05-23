import json
from pathlib import Path

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from typing import Dict, Tuple, Any

from controller import manager
from model.data_type import STR_TO_TYPE

RequiredData = Dict[str, Tuple[str, str, Any]]  # todo: change 'Any' to 'DataType'


class Template:
    def __init__(self, root_dir: Path, obj_mng: 'manager.ObjectManager'):
        self._root_dir = root_dir

        manifest_path = self._root_dir / 'manifest.json'

        with manifest_path.open() as f:
            dct = json.load(f)

        self.title = dct['title']
        self.dev_name = dct['dev_name']
        self.dev_homepage = dct['dev_homepage']
        self.description = dct['description']
        self.required_data = dict()

        for required_data_key, required_data_value in dct['required_data'].items():
            copied = required_data_value[:]

            target_type = copied[2]['type']

            if target_type in STR_TO_TYPE:
                copied[2] = STR_TO_TYPE[target_type](copied[2])
            elif target_type == "object":
                copied[2] = obj_mng.get_object_type(dct['object_type_id'])
            else:
                raise AttributeError()

            self.required_data[required_data_key] = copied

    def render(self, variables: dict) -> str:
        env = Environment(
            loader=FileSystemLoader(str(self._root_dir))
        )
        template = env.get_template('index.html')

        return template.render(**variables)


class FrameTemplate(Template):
    pass


class SceneTemplate(Template):
    pass
