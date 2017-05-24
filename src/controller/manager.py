from pathlib import Path

from model.data_type import ObjectDataType
from model.signage import Signage
from model.template import SceneTemplate


class ObjectManager:
    def __init__(self):
        pass

    def get_object_type(self, type_id: str) -> ObjectDataType:
        return None  # todo: mock implementation


class MultimediaManager:
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

    def get_scene_template(self, key: str) -> SceneTemplate:
        return self._scene_templates[key]


class SignageManager:
    def __init__(self, dir_root: str, obj_mng: ObjectManager, tpl_mng: TemplateManager):
        self._tpl_mng = tpl_mng
        self._obj_mng = obj_mng
        self._dir_root = dir_root
        self._signages = dict()
        self.load()

    def load(self) -> None:
        signage_path = Path(self._dir_root)

        for signage_id, signage_dir in [(x.stem, x) for x in signage_path.glob('*.json')]:
            self._signages[signage_id] = Signage(signage_dir, self._obj_mng, self._tpl_mng)
            print('{} loaded'.format(self._signages[signage_id]._title))

    def get_signage(self, key: str) -> Signage:
        return self._signages[key]

    def add_signage(self, key: str, signage: Signage):
        pass
