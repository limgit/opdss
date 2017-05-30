from typing import TypeVar

from model import data_type

T = TypeVar('T')


class ObjectValue:
    def __init__(self, data_type: 'data_type.ObjectDataType'):
        self._values = {}
        self._data_type = data_type

        for field_key, field_type in data_type._fields.items():
            self._values[field_key] = field_type.default

    def set_value(self, key: str, value) -> None:
        if key not in self._data_type._fields.keys():
            raise KeyError

        if not self._data_type._fields[key].is_valid(value):
            raise AttributeError

        self._values[key] = value

    def get_value(self, key: str):
        return self._values[key]

    def get_dict(self):
        to_return = {x: y for x, y in self._values.items()}

        for field_id, field_value in to_return.items():
            if isinstance(field_value, ObjectValue):
                to_return[field_id] = field_value.get_dict()
            elif isinstance(field_value, list) and isinstance(field_value[0], ObjectValue):
                to_return[field_id] = [x.get_dict() for x in to_return[field_id]]

        return to_return

