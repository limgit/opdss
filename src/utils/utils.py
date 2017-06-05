from typing import Optional

import re


def validate_id(id_value: Optional[str]) -> None:
    if id_value is not None and not re.match('[a-z]+[a-z0-9_]*', id_value):
        raise AttributeError()


def gen_ui_text(name: str, id_value: str) -> str:
    return name + " [" + id_value + "]"


def ui_text_to_id(text: str) -> str:
    return text.split('[')[-1].split(']')[0]
