from pathlib import Path

from model.data_type import ObjectDataType
from model.template import SceneTemplate


class ObjectManager:
    def __init__(self):
        pass

    def get_object_type(self, type_id: str) -> ObjectDataType:
        return None  # todo: mock implementation


class SignageManager:
    def __init__(self, dir_root: str):
        self._dir_root = dir_root
        self._signages = dict()

    def load(self) -> None:
        pass

    def add_signage(self, key: str, signage):  # todo: add type hint to signage parameter
        pass


class TemplateManager:
    def __init__(self, dir_root: str, obj_mng: ObjectManager):
        self._dir_root = dir_root
        self._obj_mng = obj_mng
        self._scene_templates = dict()
        self._frame_templates = dict()
        self.load()

    def load(self) -> None:
        scene_path = Path(self._dir_root + '/scene')
        scenes_dir = [x for x in scene_path.iterdir() if x.is_dir()]

        for scene_name, scene_dir in [(x.name, x) for x in scenes_dir]:
            self._scene_templates[scene_name] = SceneTemplate(scene_dir, self._obj_mng)
            print('{} loaded'.format(self._scene_templates[scene_name].title))


class MultimediaManager:
    pass
