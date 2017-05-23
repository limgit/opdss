import sys
from typing import TypeVar, Generic, Sequence

from model.data_value import DataValue

T = TypeVar('T')


class DataType(Generic[T]):
    def __init__(self, default: T):
        self._default = default

    @property
    def default(self):
        return self._default

    def is_valid(self, data_value: DataValue[T]):
        return data_value is not None


class StringDataType(DataType[str]):
    def __init__(self, default: str):
        super().__init__(default)

        self._min_length = 0
        self._max_length = sys.maxsize
        self._one_of = []

    @property
    def min_length(self) -> int:
        return self._min_length

    @min_length.setter
    def min_length(self, new_value: int):
        if new_value < 0 or len(self.default) < new_value or self.min_length > self.max_length:
            raise AttributeError()

        self._min_length = new_value

    @property
    def max_length(self) -> int:
        return self._max_length

    @max_length.setter
    def max_length(self, new_value: int):
        if new_value > sys.maxsize or len(self.default) > new_value or self.min_length > self.max_length:
            raise AttributeError()

        self._max_length = new_value

    @property
    def one_of(self) -> Sequence[str]:
        return self._one_of

    @one_of.setter
    def one_of(self, new_value: Sequence[str]):
        if self.default not in new_value:
            raise AttributeError()

        self._one_of = new_value[:]

    def is_valid(self, data_value: DataValue[str]):
        value = data_value.value

        return self.min_length <= len(value) <= self.max_length and value in self.one_of if self.one_of else True
