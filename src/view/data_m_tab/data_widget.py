from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextBrowser, QMessageBox)
from typing import Callable

import utils.utils as Utils
from model.data_type import ObjectDataType, StringDataType
from model.data_value import ObjectValue
from view.resource_manager import ResourceManager
from view.ui_components import StringDataWidget


class DataWidget(QWidget):
    def __init__(self, value_change_handler: Callable[[Utils.ChangeType, str], None]):
        super().__init__()

        self._data = None

        self._ledit_id = QLineEdit()
        self._vbox_data = QVBoxLayout()
        self._component_widgets = dict()  # id -> ComponentWidget
        self._tview_detail = QTextBrowser()

        self._value_change_handler = value_change_handler

        self._res = ResourceManager()
        self.init_ui()

    def load_ui(self, data_type: ObjectDataType) -> None:
        # Clean the previous layout
        self._component_widgets = dict()
        for i in range(self._vbox_data.count()):
            widget = self._vbox_data.itemAt(0).widget()
            self._vbox_data.removeWidget(widget)
            widget.deleteLater()
        self._tview_detail.setText("")

        # Load the new layout
        fields = data_type.fields
        for field_id in fields.keys():
            def clicked_handler(name: str, description: str, constraint: str) -> None:
                text = "<b>" + name + "</b><br />"
                text += description + "<br />"
                text += "Constraint: " + constraint
                self._tview_detail.setText(text)

            field = fields[field_id]  # Tuple[DataType, name, description]
            if isinstance(field[0], StringDataType):
                widget = StringDataWidget(field[0], field[1], field[2], clicked_handler)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
                # TODO: Add more UI components according to data type

    def load_data_on_ui(self, data: ObjectValue):
        self._data = data
        self._ledit_id.setText(data.id)
        self.load_ui(data.data_type)
        for field_id in data.get_values().keys():
            field_value = data.get_value(field_id)
            if field_id in self._component_widgets:  # TODO: This line should be removed
                self._component_widgets[field_id].value = field_value

    def init_ui(self):
        # ID display
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        vbox_real_data = QVBoxLayout()
        vbox_real_data.addLayout(self._vbox_data)
        vbox_real_data.addWidget(self._tview_detail)

        # Buttons
        btn_delete = QPushButton(self._res['deleteButtonText'])
        btn_delete.clicked.connect(self.button_clicked)
        btn_save = QPushButton(self._res['saveButtonText'])
        btn_save.clicked.connect(self.button_clicked)
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        btn_cancel.clicked.connect(self.button_clicked)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_delete)
        hbox_buttons.addWidget(btn_save)
        hbox_buttons.addWidget(btn_cancel)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_id)
        vbox_outmost.addLayout(vbox_real_data)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)

    def button_clicked(self):
        button_text = self.sender().text()
        if button_text == self._res['deleteButtonText']:
            pass  # TODO: Add deletion functionality
        elif button_text == self._res['saveButtonText']:
            # Check is input data valid. If not, do not save it
            if not self.is_data_valid():
                QMessageBox.warning(self, self._res['dataInvalidTitle'],
                                    self._res['dataInvalidDescription'],
                                    QMessageBox.Ok, QMessageBox.Ok)
                return

            # Now it's OK to save
            self.save()

            # Invoke value change handler to edit QTreeWidgetItem
            self._value_change_handler(Utils.ChangeType.SAVE, self._ledit_id.text())
        elif button_text == self._res['cancelButtonText']:
            self.load_data_on_ui(self._data)

    def save(self) -> None:
        # Gather all data
        values = dict()
        for field_id in self._component_widgets.keys():
            widget = self._component_widgets[field_id]
            values[field_id] = widget.value
        # Save it
        self._data.id = self._ledit_id.text()
        self._data.set_values(**values)

    def is_data_valid(self) -> bool:
        try:
            Utils.validate_id(self._ledit_id.text())
        except AttributeError:
            return False

        for field_id in self._component_widgets.keys():
            widget = self._component_widgets[field_id]
            if not widget.is_data_valid():
                return False
        return True
