from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton)

from view.resource_manager import ResourceManager


class DataWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self):
        pass  # TODO: Create logic

    def init_ui(self):
        # ID display
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        # TODO: Add data-type specific components

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
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)
