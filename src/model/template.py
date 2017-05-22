from typing import Dict, Tuple, Any

RequiredData = Dict[str, Tuple[Any, str, str]]  # todo: change 'Any' to 'DataType'


class Template:
    def __init__(self):
        self.title = ''
        self.dev_name = ''
        self.dev_homepage = ''
        self.description = ''
        self.required_data = {}


def json_to_template(dct):
    template = Template()
    template.title = dct['title']
    template.dev_name = dct['dev_name']
    template.dev_homepage = dct['dev_homepage']
    template.description = dct['description']
    # template.required_data = dct['required_data']  # todo

    return template


class FrameTemplate(Template):
    pass


class SceneTemplate(Template):
    pass
