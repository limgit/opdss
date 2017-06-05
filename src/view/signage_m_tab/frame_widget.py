from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QComboBox, QTabWidget)

import utils.utils as Utils
from controller.manager import TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class FrameWidget(QWidget):
    def __init__(self, sgn_mng: SignageManager, tpl_mng: TemplateManager):
        super().__init__()

        self._sgn_mng = sgn_mng
        self._tpl_mng = tpl_mng

        self._cbox_tpl = QComboBox()
        self._tab_data = FrameDataTab()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, sgn_id: str) -> None:
        # Change combobox item to frame's template
        tpl = self._sgn_mng.get_signage(sgn_id).frame.template
        idx = self._cbox_tpl.findText(Utils.gen_ui_text(tpl.definition.name, tpl.id))
        self._cbox_tpl.setCurrentIndex(idx)
        self._tab_data.load_data_on_ui()

    def init_ui(self) -> None:
        # Template list on combobox
        tpl_list = list()
        for tpl_id in self._tpl_mng.frame_templates:
            template = self._tpl_mng.frame_templates[tpl_id]
            tpl_list.append(Utils.gen_ui_text(template.definition.name, template.id))
        self._cbox_tpl.addItems(tpl_list)

        # Tab widget
        tab_frame_manage = QTabWidget()
        tab_frame_manage.addTab(self._tab_data, self._res['dataTabText'])

        # Buttons
        btn_save = QPushButton(self._res['saveButtonText'])
        # TODO: Add functionality
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        # TODO: Add functionality

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_save)
        hbox_buttons.addWidget(btn_cancel)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(self._cbox_tpl)
        vbox_outmost.addWidget(tab_frame_manage)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)


class FrameDataTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self) -> None:
        pass  # TODO: Add functionality

    def init_ui(self) -> None:
        pass  # TODO: Add functionality
