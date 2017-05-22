import json
from pathlib import Path

from model.template import json_to_template


class SignageManager:
    def __init__(self, dir_root: str):
        self._dir_root = dir_root
        self._signages = dict()

    def load(self) -> None:
        pass

    def add_signage(self, key: str, signage):  # todo: add type hint to signage parameter
        pass


class TemplateManager:
    def __init__(self, dir_root: str):
        self._dir_root = dir_root
        self._scene_templates = dict()
        self._frame_templates = dict()
        self.load()

    def load(self) -> None:
        scene_path = Path(self._dir_root + '/scene')
        scenes_dir = [x for x in scene_path.iterdir() if x.is_dir()]

        for scene_name, scene_manifest in [(x.name, Path(str(x) + '/manifest.json')) for x in scenes_dir]:
            with scene_manifest.open() as f:
                new_scene_template = json.load(f, object_hook=json_to_template)

            self._scene_templates[scene_name] = new_scene_template

class ObjectManager:
    pass


class MultimediaManager:
    pass
