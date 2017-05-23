from typing import TypeVar, Generic

from model.data_type import DataType

T = TypeVar('T')


class DataValue(Generic[T]):
    def __init__(self, data_type: DataType[T]):
        self._value = data_type.default
        self._data_type = data_type
        self._on_change = lambda: None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: T):
        self._value = new_value

    @property
    def data_type(self):
        return self._data_type

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, new_value: function):
        self._on_change = new_value


