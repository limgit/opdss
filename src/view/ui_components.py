from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QGroupBox, QLineEdit, QComboBox,
                             QVBoxLayout, QCheckBox, QDateTimeEdit)
from PyQt5.QtCore import QDateTime

from enum import Enum, auto
from typing import Callable
import sys

from model.data_type import (StringDataType, BooleanDataType, IntegerDataType,
                             DateDataType)


def make_clickable(widget: QWidget, handler):
    class ClickableWidget(widget):
        def __init__(self, click_handler):
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
        elif self._input_type == InputType.ONE_OF:
            self._cbox_value.addItems(self._data_type.one_of)
            vbox_outmost.addWidget(self._cbox_value)
        self.setLayout(vbox_outmost)

    def mousePressEvent(self, event):
        constraint = ""
        if self._input_type == InputType.FIELD:
            min_len = self._data_type.min_length
            max_len = self._data_type.max_length
            if min_len != 0:
                constraint += "Minimum length " + str(min_len) + ". "
            if max_len != sys.maxsize:
                constraint += "Maximum length " + str(max_len) + "."
            if constraint == '':
                constraint = "None"
        elif self._input_type == InputType.ONE_OF:
            constraint = "Select from the items."
        self._clicked_handler(self.name, self.description, constraint)
        super().mousePressEvent(event)


class BooleanDataWidget(ComponentWidget):
    def __init__(self, data_type: BooleanDataType, name: str, description: str,
                 clicked_handler: Callable[[str, str, str], None]):
        super().__init__(name, description)

        self._data_type = data_type
        self._check_box = make_clickable(QCheckBox, self.mousePressEvent)
        self._clicked_handler = clicked_handler

        self.init_ui()

    @property
    def value(self) -> bool:
        return self._check_box.isChecked()

    @value.setter
    def value(self, value: bool) -> None:
        self._check_box.setChecked(value)

    def is_data_valid(self) -> bool:
        return True  # Boolean data is always valid

    def load_data_on_ui(self, value: bool) -> None:
        self.value = value

    def init_ui(self) -> None:
        self.setTitle(self.name + " (Boolean)")
        self._check_box.setText(self.name)
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(self._check_box)
        self.setLayout(vbox_outmost)

    def mousePressEvent(self, event):
        self._clicked_handler(self.name, self.description, "None.")
        super().mousePressEvent(event)


class IntegerDataWidget(ComponentWidget):
    def __init__(self, data_type: IntegerDataType, name: str, description: str,
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
    def value(self) -> int:
        if self._input_type == InputType.FIELD:
            return int(self._ledit_value.text())
        elif self._input_type == InputType.ONE_OF:
            return int(self._cbox_value.currentText())

    @value.setter
    def value(self, value: int) -> None:
        if self._input_type == InputType.FIELD:
            self._ledit_value.setText(str(value))
        elif self._input_type == InputType.ONE_OF:
            idx = self._cbox_value.findText(str(value))
            self._cbox_value.setCurrentIndex(idx)

    def is_data_valid(self) -> bool:
        if self._input_type == InputType.FIELD:
            return self._ledit_value.text().isdigit() and \
                   self._data_type.min <= self.value <= self._data_type.max
        elif self._input_type == InputType.ONE_OF:
            return self._cbox_value.currentText().isdigit() and \
                   self.value in self._data_type.one_of

    def load_data_on_ui(self, value: str) -> None:
        self.value = value

    def init_ui(self) -> None:
        self.setTitle(self.name + " (Integer)")
        vbox_outmost = QVBoxLayout()
        if self._input_type == InputType.FIELD:
            vbox_outmost.addWidget(self._ledit_value)
        elif self._input_type == InputType.ONE_OF:
            self._cbox_value.addItems([str(a) for a in self._data_type.one_of])
            vbox_outmost.addWidget(self._cbox_value)
        self.setLayout(vbox_outmost)

    def mousePressEvent(self, event):
        constraint = ""
        if self._input_type == InputType.FIELD:
            minimum = self._data_type.min
            maximum = self._data_type.max
            if minimum != 0:
                constraint += "Minimum value " + str(minimum) + ". "
            if maximum != sys.maxsize:
                constraint += "Maximum value " + str(maximum) + "."
            if constraint == '':
                constraint = "None"
        elif self._input_type == InputType.ONE_OF:
            constraint = "Select from the items."
        self._clicked_handler(self.name, self.description, constraint)
        super().mousePressEvent(event)


class DateTimeDataWidget(ComponentWidget):
    def __init__(self, data_type: DateDataType, name: str, description: str,
                 clicked_handler: Callable[[str, str, str], None]):
        super().__init__(name, description)

        self._data_type = data_type
        self._date_time = make_clickable(QDateTimeEdit, self.mousePressEvent)
        self._clicked_handler = clicked_handler

        self.init_ui()

    @property
    def value(self) -> str:
        return self._date_time.dateTime().toString("yyyy-MM-dd hh:mm")

    @value.setter
    def value(self, value: datetime) -> None:
        self._date_time.setDateTime(value)

    def is_data_valid(self) -> bool:
        return self._data_type.is_valid(self.value)

    def load_data_on_ui(self, value: str) -> None:
        self.value = value

    def init_ui(self) -> None:
        self._date_time.setDisplayFormat("yyyy-MM-dd hh:mm")

        self.setTitle(self.name + " (DateTime)")
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(self._date_time)
        self.setLayout(vbox_outmost)

    def mousePressEvent(self, event):
        constraint = ""
        min_value = self._data_type.min
        max_value = self._data_type.max
        if min_value != '1000-01-01 00:00':
            constraint += "Minimum date time " + min_value + ". "
        if max_value != '9999-12-31 23:59':
            constraint += "Maximum date time " + max_value + "."
        if constraint == '':
            constraint = "None"
        self._clicked_handler(self.name, self.description, constraint)
        super().mousePressEvent(event)
