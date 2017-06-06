from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPlainTextEdit, QGroupBox,
                             QPushButton, QMessageBox)
from typing import Callable

import utils.utils as Utils
from model.signage import Signage
from view.resource_manager import ResourceManager


class SignageWidget(QWidget):
    def __init__(self, value_change_handler: Callable[[Utils.ChangeType, str], None]):
        super().__init__()

        self._value_change_handler = value_change_handler

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()

        self._signage = None
        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, signage: Signage) -> None:
        self._signage = signage
        self._ledit_id.setText(signage.id)
        self._ledit_name.setText(signage.title)
        self._ptedit_descript.setPlainText(signage.description)

    def init_ui(self) -> None:
        # ID display
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        # Name display
        vbox_name = QVBoxLayout()
        vbox_name.addWidget(self._ledit_name)

        group_name = QGroupBox(self._res['signageNameLabel'])
        group_name.setLayout(vbox_name)

        # Description display
        vbox_descript = QVBoxLayout()
        vbox_descript.addWidget(self._ptedit_descript)

        group_descript = QGroupBox(self._res['signageDescriptionLabel'])
        group_descript.setLayout(vbox_descript)

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
        vbox_outmost.addWidget(group_name)
        vbox_outmost.addWidget(group_descript)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)

    def button_clicked(self) -> None:
        button_text = self.sender().text()
        if button_text == self._res['deleteButtonText']:
            # TODO: Delete selected signage
            self._value_change_handler(Utils.ChangeType.DELETE)
        elif button_text == self._res['saveButtonText']:
            # ID Validation
            try:
                Utils.validate_id(self._ledit_id.text())
            except AttributeError:
                QMessageBox.warning(self, self._res['idInvalidTitle'],
                                    self._res['idInvalidDescription'],
                                    QMessageBox.Ok, QMessageBox.Ok)
                return  # Do not save signage

            # Save to signage
            self._signage.id = self._ledit_id.text()
            self._signage.title = self._ledit_name.text()
            self._signage.description = self._ptedit_descript.toPlainText()

            # Invoke value change handler to edit QTreeWidgetItem
            sgn_text = Utils.gen_ui_text(self._signage.title, self._signage.id)
            self._value_change_handler(Utils.ChangeType.SAVE, sgn_text)
        elif button_text == self._res['cancelButtonText']:
            # Load the previous data
            self.load_data_on_ui(self._signage)
