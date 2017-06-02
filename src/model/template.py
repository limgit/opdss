from pathlib import Path

from model.data_type import ObjectDataType


class Template:
    def __init__(self, template_id: str, object_type: ObjectDataType, path: Path):
        self._id = template_id
        self._root_dir = path
        self._definition = object_type


class FrameTemplate(Template):
    pass


class SceneTemplate(Template):
    pass
