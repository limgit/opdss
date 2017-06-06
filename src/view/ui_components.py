from PyQt5.QtWidgets import (QWidget, QGroupBox, QLineEdit, QComboBox,
                             QVBoxLayout)
from PyQt5.Qt import QMouseEvent
from enum import Enum, auto
from typing import Callable
import sys

from model.data_type import StringDataType


def make_clickable(widget: QWidget, handler: Callable[[QMouseEvent], None]):
    class ClickableWidget(widget):
        def __init__(self, click_handler: Callable[[QMouseEvent], None]):
            super().__init__()
            self._click_handler = click_handler

        def mousePressEvent(self, event):
            self._click_handler(event)
            super().mousePressEvent(event)
    return ClickableWidget(handler)


class InputType(Enum):
    FIELD = auto()
    ONE_OF = auto()


class ComponentWidget(QGroupBox):
    def __init__(self, name: str, description: str):
        super().__init__()

        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description


class StringDataWidget(ComponentWidget):
    def __init__(self, data_type: StringDataType, name: str, description: str,
                 clicked_handler: Callable[[str, str, str], None]):
        super().__init__(name, description)

        self._data_type = data_type
        if len(self._data_type.one_of) == 0:
            # No one of field. Custom data
            self._input_type = InputType.FIELD
            self._ledit_value = make_clickable(QLineEdit, self.mousePressEvent)
        else:
            # one of field exist. Select from combobox
            self._input_type = InputType.ONE_OF
            self._cbox_value = make_clickable(QComboBox, self.mousePressEvent)
        self._clicked_handler = clicked_handler

        self.init_ui()

    @property
    def value(self) -> str:
        if self._input_type == InputType.FIELD:
            return self._ledit_value.text()
        elif self._input_type == InputType.ONE_OF:
            return self._cbox_value.currentText()

    @value.setter
    def value(self, value: str) -> None:
        if self._input_type == InputType.FIELD:
            self._ledit_value.setText(value)
        elif self._input_type == InputType.ONE_OF:
            idx = self._cbox_value.findText(value)
            self._cbox_value.setCurrentIndex(idx)

    def is_data_valid(self) -> bool:
        if self._input_type == InputType.FIELD:
            return self._data_type.min_length <= \
                   len(self.value) \
                   <= self._data_type.max_length
        elif self._input_type == InputType.ONE_OF:
            return self.value in self._data_type.one_of

    def load_data_on_ui(self, value: str) -> None:
        self.value = value

    def init_ui(self) -> None:
        self.setTitle(self.name + " (String)")
        vbox_outmost = QVBoxLayout()
        if self._input_type == InputType.FIELD:
            vbox_outmost.addWidget(self._ledit_value)
            self.setLayout(vbox_outmost)
        elif self._input_type == InputType.ONE_OF:
            self._cbox_value.addItems(self._data_type.one_of)
            vbox_outmost.addWidget(self._cbox_value)
            self.setLayout(self._cbox_value)

    def mousePressEvent(self, event):
        constraint = ""
        if self._input_type == InputType.FIELD:
            min_len = self._data_type.min_length
            max_len = self._data_type.max_length
            if min_len != 0:
                constraint += "Minimum length " + str(min_len) + ". "
            if max_len != sys.maxsize:
                constraint += "Maximum length " + str(max_len) + "."
        self._clicked_handler(self.name, self.description, constraint)
        super().mousePressEvent(event)
