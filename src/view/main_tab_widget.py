from PyQt5.QtWidgets import QWidget, QTabWidget
from view.resource_manager import ResourceManager


class MainTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.initUI()

    def initUI(self):
        signage_tab = QWidget()  # TODO: Change to custom widget
        self.addTab(signage_tab, self._res['signageManagementTabText'])

        data_tab = QWidget()  # TODO: Change to custom widget
        self.addTab(data_tab, self._res['dataManagementTabText'])

        multimedia_tab = QWidget()  # TODO: Change to custom widget
        self.addTab(multimedia_tab, self._res['multimediaManagementTabText'])

        template_tab = QWidget()  # TODO: Change to custom widget
        self.addTab(template_tab, self._res['templateManagementTabText'])

        status_tab = QWidget()  # TODO: Change to custom widget
        self.addTab(status_tab, self._res['statusManagementTabText'])

        log_tab = QWidget()  # TODO: Change to custom widget
        self.addTab(log_tab, self._res['logManagementTabText'])
