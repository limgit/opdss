from typing import TypeVar, Callable, Any, Optional

from model import data_type

from utils import utils

T = TypeVar('T')


class ObjectValue:
    def __init__(self, object_id: Optional[str], data_type: 'data_type.ObjectDataType'):
        self._id = ''
        self._values = {}
        self._data_type = data_type
        self._id_change_handler = lambda x, y: None
        self._value_change_handler = lambda: None

        self.id = object_id

        for field_key, field_type in data_type._fields.items():
            self._values[field_key] = field_type.default

    def set_value(self, key: str, value: Any) -> None:
        self._set_value(key, value)
        self._value_change_handler()

    # if multiple values should be changed, use this method instead of 'set_value'
    # if you don't, change handler will be called whenever single value is changed.
    def set_values(self, **values):
        for key, value in values:
            self._set_value(key, value)

        self._value_change_handler()

    def _set_value(self, key: str, value: Any):
        if key not in self._data_type._fields.keys():
            raise KeyError

        if not self._data_type._fields[key].is_valid(value):
            raise AttributeError

        self._values[key] = value

    def get_value(self, key: str):
        return self._values[key]

    def get_dict(self, use_reference: bool=True):
        to_return = {x: y for x, y in self._values.items()}

        for field_id, field_value in to_return.items():
            if isinstance(field_value, ObjectValue):
                to_return[field_id] = field_value.get_dict() if use_reference else field_value.id
            elif isinstance(field_value, list) and isinstance(field_value[0], ObjectValue):
                to_return[field_id] = [x.get_dict() if use_reference else x.id for x in to_return[field_id]]

        return to_return

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, new_id: Optional[str]) -> None:
        utils.validate_id(new_id)

        old_id = self._id
        self._id = new_id
        self._id_change_handler(old_id, new_id)

    @property
    def data_type(self) -> 'data_type.ObjectDataType':
        return self._data_type

    @property
    def on_id_change(self) -> None:
        raise ValueError  # don't try to access!

    # (old_id, new_id)
    @on_id_change.setter
    def on_id_change(self, handler: Callable[[str, str], None]) -> None:
        self._id_change_handler = handler

    @property
    def on_value_change(self) -> None:
        raise ValueError  # don't try to access!

    @on_value_change.setter
    def on_value_change(self, handler: Callable[[None], None]) -> None:
        self._value_change_handler = handler


