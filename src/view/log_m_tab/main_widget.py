from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget)

from controller.manager import ObjectManager, TemplateManager, SignageManager, MultimediaManager, ChannelManager
from view.resource_manager import ResourceManager


class LogManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._list_log = QListWidget()

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        # TODO: Need fixes
        self._list_log.addItem("[2017-04-09 23:00] [Info] Signage web server started.")

        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(self._list_log)

        self.setLayout(vbox_outmost)
