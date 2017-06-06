from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton)

from model.data_value import FileValue
from view.resource_manager import ResourceManager


class MultimediaWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_name = QLineEdit()

        self._res = ResourceManager()
        self.init_ui()

    def clear_data_on_ui(self):
        self._ledit_name.setText('')

    def load_data_on_ui(self, mtm: FileValue):
        self._ledit_name.setText(mtm.file_name)

    def init_ui(self):
        # Name display
        label_name = QLabel(self._res['nameLabel'])

        hbox_name = QHBoxLayout()
        hbox_name.addWidget(label_name)
        hbox_name.addWidget(self._ledit_name)

        # Buttons
        btn_delete = QPushButton(self._res['deleteButtonText'])
        btn_delete.clicked.connect(self.button_clicked)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_delete)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_name)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)

    def button_clicked(self):
        button_text = self.sender().text()
        if button_text == self._res['deleteButtonText']:
            pass  # TODO: Add deletion logic
