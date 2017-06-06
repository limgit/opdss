from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextBrowser)

from model.data_type import ObjectDataType, StringDataType
from model.data_value import ObjectValue
from view.resource_manager import ResourceManager
from view.ui_components import StringDataWidget


class DataWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()
        self._vbox_data = QVBoxLayout()
        self._component_widgets = dict()  # id -> ComponentWidget
        self._tview_detail = QTextBrowser()

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
        # TODO: Add functionality
        btn_save = QPushButton(self._res['saveButtonText'])
        # TODO: Add functionality
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        # TODO: Add functionality

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
