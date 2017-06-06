from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                             QLineEdit, QPlainTextEdit, QGroupBox,
                             QPushButton)

from controller.manager import ObjectManager
from view.resource_manager import ResourceManager


class DataTypeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ledit_author = QLineEdit()
        self._ledit_homepage = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, obj_mng: ObjectManager, data_type_id: str):
        data_type = obj_mng.get_object_type(data_type_id)
        self._ledit_id.setText(data_type_id)
        self._ledit_name.setText(data_type.name)
        self._ledit_author.setText(data_type.dev_name)
        self._ledit_homepage.setText(data_type.dev_homepage)
        self._ptedit_descript.setPlainText(data_type.description)

    def init_ui(self):
        # ID display
        self._ledit_id.setEnabled(False)
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        # Name display
        self._ledit_name.setEnabled(False)
        vbox_name = QVBoxLayout()
        vbox_name.addWidget(self._ledit_name)

        group_name = QGroupBox(self._res['dataTypeNameLabel'])
        group_name.setLayout(vbox_name)

        # Author display
        self._ledit_author.setEnabled(False)
        vbox_author = QVBoxLayout()
        vbox_author.addWidget(self._ledit_author)

        group_author = QGroupBox(self._res['dataTypeAuthorLabel'])
        group_author.setLayout(vbox_author)

        # Homepage display
        self._ledit_homepage.setEnabled(False)
        vbox_homepage = QVBoxLayout()
        vbox_homepage.addWidget(self._ledit_homepage)

        group_homepage = QGroupBox(self._res['dataTypeHomepageLabel'])
        group_homepage.setLayout(vbox_homepage)

        # Description display
        self._ptedit_descript.setEnabled(False)
        vbox_descript = QVBoxLayout()
        vbox_descript.addWidget(self._ptedit_descript)

        group_descript = QGroupBox(self._res['dataTypeDescriptionLabel'])
        group_descript.setLayout(vbox_descript)

        # Button
        btn_delete = QPushButton(self._res['deleteButtonText'])
        btn_delete.clicked.connect(self.button_clicked)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_delete)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_id)
        vbox_outmost.addWidget(group_name)
        vbox_outmost.addWidget(group_author)
        vbox_outmost.addWidget(group_homepage)
        vbox_outmost.addWidget(group_descript)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)

    def button_clicked(self):
        button_text = self.sender().text()
        if button_text == self._res['deleteButtonText']:
            pass  # TODO: Add DataType Deletion logic
