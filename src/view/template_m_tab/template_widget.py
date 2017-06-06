from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPlainTextEdit,
                             QGroupBox, QPushButton, QMessageBox)
from typing import Callable

import utils.utils as utils
from controller.manager import TemplateManager
from model.template import Template, SceneTemplate
from view.resource_manager import ResourceManager


class TemplateWidget(QWidget):
    def __init__(self, tpl_mng: TemplateManager, value_change_handler: Callable[[utils.ChangeType, str], None]):
        super().__init__()

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ledit_author = QLineEdit()
        self._ledit_homepage = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()

        self._tpl_mng = tpl_mng
        self._tpl = None
        self._value_change_handler = value_change_handler

        self._res = ResourceManager()
        self.init_ui()

    def clear_data_on_ui(self) -> None:
        self._ledit_id.setText('')
        self._ledit_name.setText('')
        self._ledit_author.setText('')
        self._ledit_homepage.setText('')
        self._ptedit_descript.setPlainText('')

    def load_data_on_ui(self, tpl: Template) -> None:
        self._tpl = tpl
        tpl_metadata = tpl.definition
        self._ledit_id.setText(tpl.id)
        self._ledit_name.setText(tpl_metadata.name)
        self._ledit_author.setText(tpl_metadata.dev_name)
        self._ledit_homepage.setText(tpl_metadata.dev_homepage)
        self._ptedit_descript.setPlainText(tpl_metadata.description)

    def init_ui(self) -> None:
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

        group_name = QGroupBox(self._res['templateNameLabel'])
        group_name.setLayout(vbox_name)

        # Author display
        self._ledit_author.setEnabled(False)
        vbox_author = QVBoxLayout()
        vbox_author.addWidget(self._ledit_author)

        group_author = QGroupBox(self._res['templateAuthorLabel'])
        group_author.setLayout(vbox_author)

        # Homepage display
        self._ledit_homepage.setEnabled(False)
        vbox_homepage = QVBoxLayout()
        vbox_homepage.addWidget(self._ledit_homepage)

        group_homepage = QGroupBox(self._res['templateHomepageLabel'])
        group_homepage.setLayout(vbox_homepage)

        # Description display
        self._ptedit_descript.setEnabled(False)
        vbox_descript = QVBoxLayout()
        vbox_descript.addWidget(self._ptedit_descript)

        group_descript = QGroupBox(self._res['templateDescriptionLabel'])
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
            try:
                if isinstance(self._tpl, SceneTemplate):
                    self._tpl_mng.remove_scene_template(self._tpl)
                else:
                    self._tpl_mng.remove_frame_template(self._tpl)
            except ReferenceError as e:
                QMessageBox.warning(self, "Can't delete",
                                    "This template can't be deleted. " + ', '.join(e.args[0].keys()) + " reference this",
                                    QMessageBox.Ok, QMessageBox.Ok)
                return
            self._value_change_handler(utils.ChangeType.DELETE)
