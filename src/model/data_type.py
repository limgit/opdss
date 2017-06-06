import copy
import sys
from datetime import datetime
from pathlib import Path
from typing import TypeVar, Generic, Sequence, Dict, Tuple

from model.data_value import ObjectValue, FileValue

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
        # super().__init__({key: value[0].default for key, value in fields.items()})

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

    def has_references(self, to_check) -> bool:
        return to_check in [x[0] if not isinstance(x[0], ListDataType) else x[0].data_type for x in self._fields.values()]


class BooleanDataType(DataType[bool]):
    def __init__(self, default: bool=False):
        super().__init__(default)


class DateDataType(DataType[str]):
    format = '%Y-%m-%d %H:%M'

    def __init__(self,
                 min_value: str='1000-01-01 00:00',
                 max_value: str='9999-12-31 23:59'):

        super().__init__(datetime.now().strftime(DateDataType.format))

        self._min = datetime.strptime(min_value, DateDataType.format)
        self._max = datetime.strptime(max_value, DateDataType.format)

    @property
    def min(self) -> str:
        return self._min.strftime(DateDataType.format)

    @min.setter
    def min(self, new_value: str):
        new_datetime = datetime.strptime(new_value, DateDataType.format)

        if self.default < new_datetime or self._min > self._max:
            raise AttributeError()

        self._min = new_datetime

    @property
    def max(self) -> str:
        return self._max.strftime(DateDataType.format)

    @max.setter
    def max(self, new_value: str):
        new_datetime = datetime.strptime(new_value, DateDataType.format)

        if self.default > new_datetime or new_datetime > self._max:
            raise AttributeError()

        self._max = new_datetime

    def is_valid(self, value: str):
        new_datetime = datetime.strptime(value, DateDataType.format) if isinstance(value, str) else value

        return self._min <= new_datetime <= self._max


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
        super().__init__('')

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    def is_valid(self, value: str) -> bool:
        if not value:
            return True

        if isinstance(value, FileValue):
            return True  # todo

        return (self._root_dir / value).exists()


STR_TO_PRIMITIVE_TYPE = {
    'str': StringDataType,
    'int': IntegerDataType,
    'bool': BooleanDataType,
    'datetime': DateDataType
}
