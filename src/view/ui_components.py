from PyQt5.QtWidgets import (QGroupBox, QLineEdit, QComboBox, QVBoxLayout)
from enum import Enum, auto

from model.data_type import StringDataType


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
    def __init__(self, data_type: StringDataType, name: str, description: str):
        super().__init__(name, description)

        self._data_type = data_type
        if len(self._data_type.one_of) == 0:
            # No one of field. Custom data
            self._input_type = InputType.FIELD
            self._ledit_value = QLineEdit()
        else:
            # one of field exist. Select from combobox
            self._input_type = InputType.ONE_OF
            self._cbox_value = QComboBox()

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
            self.setLayout(self._cbox_value)

