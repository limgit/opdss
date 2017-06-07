from pathlib import Path

from jinja2 import Environment, FileSystemLoader

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

    def render(self, data: dict) -> str:
        env = Environment(
            loader=FileSystemLoader(str(self._root_dir))
        )

        template = env.get_template('{}.html'.format(self._id))

        return template.render(x=data)


class FrameTemplate(Template):
    pass


class SceneTemplate(Template):
    pass
