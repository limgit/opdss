from PyQt5.QtWidgets import QTabWidget

from controller.manager import ObjectManager, TemplateManager, SignageManager, MultimediaManager, ChannelManager
from view.resource_manager import ResourceManager
from view.signage_m_tab import SignageManagementTab
from view.data_m_tab import DataManagementTab
from view.multimedia_m_tab import MultimediaManagementTab
from view.template_m_tab import TemplateManagementTab
from view.status_m_tab import StatusManagementTab
from view.log_m_tab import LogManagementTab


class MainTabWidget(QTabWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        signage_tab = SignageManagementTab(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.addTab(signage_tab, self._res['signageManagementTabText'])

        data_tab = DataManagementTab(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.addTab(data_tab, self._res['dataManagementTabText'])

        multimedia_tab = MultimediaManagementTab(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.addTab(multimedia_tab, self._res['multimediaManagementTabText'])

        template_tab = TemplateManagementTab(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.addTab(template_tab, self._res['templateManagementTabText'])

        status_tab = StatusManagementTab(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.addTab(status_tab, self._res['statusManagementTabText'])

        log_tab = LogManagementTab(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.addTab(log_tab, self._res['logManagementTabText'])
