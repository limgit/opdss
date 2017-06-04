from pathlib import Path
from typing import TypeVar, Callable, Any, Optional

from controller import manager
from model import data_type
from utils import utils

T = TypeVar('T')


class FileValue:
    def __init__(self, file_type: 'data_type.FileDataType', file_name: str):
        self._data_type = file_type
        self._file_name = ''
        self._on_id_change_handler = lambda old_id, new_id: None

        self._file_name = file_name  # set with is_valid methods

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, new_name: str) -> None:
        self._data_type.is_valid(new_name)

        old_name = self._file_name
        self._file_name = new_name
        self._on_id_change_handler(old_name, new_name)

    @property
    def file_path(self) -> Path:
        return self._data_type.root_dir / self._file_name

    @property
    def on_id_change(self) -> None:
        raise ValueError  # don't try to access!

    @on_id_change.setter
    def on_id_change(self, handler: Callable[[str, str], None]) -> None:
        self._on_id_change_handler = handler


class ObjectValue:
    def __init__(self, object_id: Optional[str], data_type: 'data_type.ObjectDataType', obj_mng: 'manager.ObjectManager'):
        self._id = ''
        self._values = {}
        self._data_type = data_type
        self._id_change_handler = lambda x, y: None
        self._value_change_handler = lambda: None
        self._obj_mng = obj_mng  # I hope this reference could be removed...

        self.id = object_id

        for field_key, field_type in data_type.fields.items():
            self.set_value(field_key, field_type[0].default)

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
        if key not in self._data_type.fields.keys():
            raise KeyError

        field_type = self._data_type.fields[key][0]

        if isinstance(field_type, data_type.ObjectDataType):
            value = self._obj_mng.get_object_value(field_type, value)
        elif isinstance(field_type, data_type.ListDataType) and isinstance(field_type.data_type, data_type.ObjectDataType):
            value = [self._obj_mng.get_object_value(field_type.data_type, x) for x in value]

        if not self._data_type.fields[key][0].is_valid(value):
            raise AttributeError

        self._values[key] = value

    def get_value(self, key: str):
        return self._values[key]

    def get_values(self, use_reference: bool=True):
        to_return = {x: y for x, y in self._values.items()}

        for field_id, field_value in to_return.items():
            if isinstance(field_value, ObjectValue):
                to_return[field_id] = field_value.get_values() if use_reference else field_value.id
            elif isinstance(field_value, list) and isinstance(field_value[0], ObjectValue):
                to_return[field_id] = [x.get_values() if use_reference else x.id for x in to_return[field_id]]

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
        self._value_change_handler()

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
