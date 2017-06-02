from typing import Optional

import re


def validate_id(id_value: Optional[str]) -> None:
    if id_value is not None and not re.match('[a-z]+[a-z0-9_]*', id_value):
        raise AttributeError()
