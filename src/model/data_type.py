import sys
from typing import TypeVar, Generic, Sequence

T = TypeVar('T')


class DataType(Generic[T]):
    def __init__(self, default: T):
        self._default = default

    @property
    def default(self):
        return self._default

    def is_valid(self, value: T):
        return value is not None


class StringDataType(DataType[str]):
    def __init__(self, dct: dict):
        super().__init__(dct['default'] if 'default' in dct.keys() else '')

        self._min_length = 0
        self._max_length = sys.maxsize
        self._one_of = []

        if 'min_length' in dct.keys():
            self.min_length = dct['min_length']

        if 'max_length' in dct.keys():
            self.max_length = dct['max_length']

        if 'one_of' in dct.keys():
            self.one_of = dct['one_of']

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

    def is_valid(self, value: str):
        return self.min_length <= len(value) <= self.max_length and value in self.one_of if self.one_of else True


class IntegerDataType(DataType):
    pass


class ObjectDataType(DataType):
    pass

STR_TO_TYPE = {
    "str": StringDataType,
    "int": IntegerDataType
}
