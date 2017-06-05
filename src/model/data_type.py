import copy
import sys
from datetime import datetime
from pathlib import Path
from typing import TypeVar, Generic, Sequence, Dict, Tuple

from model.data_value import ObjectValue

T = TypeVar('T')

# as DataType don't need to be changed dynamically, just use a dict class to initialize, not a Path.
# use a Path class for an initializer when we have to write back changes on a class to a file.


class DataType(Generic[T]):
    def __init__(self, default: T):
        self._default = default

    @property
    def default(self):
        return copy.copy(self._default)

    def is_valid(self, value: T):
        return value is not None


class StringDataType(DataType[str]):
    def __init__(self, default: int=0, min_length: int=0, max_length: int=sys.maxsize, one_of=None):
        super().__init__(default)

        if one_of is None:
            one_of = []

        self._min_length = min_length
        self._max_length = max_length
        self._one_of = one_of

    @property
    def min_length(self) -> int:
        return self._min_length

    @min_length.setter
    def min_length(self, new_value: int):
        if new_value < 0 or len(self.default) < new_value or self._min_length > self._max_length:
            raise AttributeError()

        self._min_length = new_value

    @property
    def max_length(self) -> int:
        return self._max_length

    @max_length.setter
    def max_length(self, new_value: int):
        if new_value > sys.maxsize or len(self.default) > new_value or self._min_length > self._max_length:
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
        return self._min_length <= len(value) <= self._max_length and (value in self._one_of if self._one_of else True)


class IntegerDataType(DataType[int]):
    def __init__(self, default: int=0, min_value: int=0, max_value: int=sys.maxsize, one_of=None):
        super().__init__(default)

        if one_of is None:
            one_of = []

        self._min = min_value
        self._max = max_value
        self._one_of = one_of

    @property
    def min(self) -> int:
        return self._min

    @min.setter
    def min(self, new_value: int):
        if self.default < new_value or self._min > self._max:
            raise AttributeError()

        self._min = new_value

    @property
    def max(self) -> int:
        return self._max

    @max.setter
    def max(self, new_value: int):
        if self.default > new_value or new_value > sys.maxsize:
            raise AttributeError()

        self._max = new_value

    @property
    def one_of(self) -> Sequence[int]:
        return self._one_of

    @one_of.setter
    def one_of(self, new_value: Sequence[int]):
        if self.default not in new_value:
            raise AttributeError

        self._one_of = new_value[:]

    def is_valid(self, value: int):
        return self._min <= value <= self._max and (value in self._one_of if self._one_of else True)


class ObjectDataType(DataType[ObjectValue]):
    def __init__(self, type_id: str, name: str='', dev_name: str='', dev_homepage: str='', description: str='',
                 fields: Dict[str, Tuple[DataType, str, str]]=None):

        if fields is None:
            fields = dict()

        self._id = type_id
        self._name = name
        self._dev_name = dev_name
        self._dev_homepage = dev_homepage
        self._description = description
        self._fields = fields

        super().__init__('')
        # super().__init__({key: value.default for key, value in fields.items()})

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def dev_name(self):
        return self._dev_name

    @property
    def dev_homepage(self):
        return self._dev_homepage

    @property
    def description(self):
        return self._description

    @property
    def fields(self) -> Dict[str, Tuple[DataType, str, str]]:
        return copy.copy(self._fields)

    def is_valid(self, value: ObjectValue):
        if value is None:
            return True

        return all([field_type[0].is_valid(value.get_value(field_key)) for field_key, field_type in self._fields.items()])


class BooleanDataType(DataType[bool]):
    def __init__(self, default: bool=False):
        super().__init__(default)


class DateDataType(DataType[datetime]):
    def __init__(self, default: datetime,
                 min_value: datetime=datetime(1, 1, 1, 1, 1, 1),
                 max_value: datetime=datetime(9999, 12, 31, 23, 59, 59)):

        super().__init__(default)

        self._min = min_value
        self._max = max_value

    @property
    def min(self) -> datetime:
        return self._min

    @min.setter
    def min(self, new_value: datetime):
        if self.default < new_value or self._min > self._max:
            raise AttributeError()

        self._min = new_value

    @property
    def max(self) -> datetime:
        return self._max

    @max.setter
    def max(self, new_value: datetime):
        if self.default > new_value or new_value > self._max:
            raise AttributeError()

        self._max = new_value

    def is_valid(self, value: datetime):
        return self._min <= value <= self._max


class ListDataType(DataType[list]):
    def __init__(self, data_type: DataType, min_len: int, max_len: int):
        self._min_len = min_len
        self._max_len = max_len
        self._data_type = data_type

        super().__init__([data_type.default for _ in range(min_len)])

    @property
    def min_len(self) -> int:
        return self._min_len

    @property
    def max_len(self) -> int:
        return self._max_len

    @property
    def data_type(self) -> DataType:
        return self._data_type

    def is_valid(self, value: list):
        return all([self._data_type.is_valid(x) for x in value])


class FileDataType(DataType[str]):
    def __init__(self, root_dir: Path):
        self._root_dir = root_dir
        super().__init__('my_file')

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    def is_valid(self, value: str) -> bool:
        return (self._root_dir / value).exists()


STR_TO_PRIMITIVE_TYPE = {
    'str': StringDataType,
    'int': IntegerDataType,
    'bool': BooleanDataType
}
