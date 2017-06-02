from pathlib import Path

from model.data_type import ObjectDataType


class Template:
    def __init__(self, template_id: str, definition: ObjectDataType, path: Path):
        self._id = template_id
        self._root_dir = path
        self._definition = definition

    @property
    def id(self) -> str:
        return self._id

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    @property
    def definition(self) -> ObjectDataType:
        return self._definition


class FrameTemplate(Template):
    pass


class SceneTemplate(Template):
    pass
