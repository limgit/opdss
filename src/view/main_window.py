import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QPushButton, QHBoxLayout, QVBoxLayout)

from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager
from view.main_tab_widget import MainTabWidget


class MainWidget(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        self.initUI()

    def initUI(self):
        # Run button
        btn_run = QPushButton(self._res['runButtonText'])
        # TODO: Add functionality: btn_run.clicked.connect(self.handler)

        # Stop button
        btn_stop = QPushButton(self._res['stopButtonText'])
        # TODO: Add functionality: btn_run.clicked.connect(self.handler)

        # Refresh button
        btn_refresh = QPushButton(self._res['refreshButtonText'])
        # TODO: Add functionality: btn_run.clicked.connect(self.handler)

        # Layout buttons
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(btn_run)
        hbox_buttons.addWidget(btn_stop)
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_refresh)

        # Tab widget
        tab_widget_main = MainTabWidget(self._obj_mng, self._tpl_mng, self._sgn_mng)

        # Layout buttons and tab widget
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_buttons)
        vbox_outmost.addWidget(tab_widget_main)

        # Set layout
        self.setLayout(vbox_outmost)


class MainWindow(QMainWindow):
    def __init__(self, root_path: Path):
        super().__init__()

        self._root_path = root_path.resolve()

        self._obj_mng = ObjectManager(self._root_path / 'data')
        self._tpl_mng = TemplateManager(self._root_path / 'template', self._obj_mng)
        self._sgn_mng = SignageManager(self._root_path / 'signage', self._obj_mng, self._tpl_mng)

        self._res = ResourceManager()
        self.initUI()

    def initUI(self):
        main_widget = MainWidget(self._obj_mng, self._tpl_mng, self._sgn_mng)
        self.setCentralWidget(main_widget)

        self.setGeometry(300, 300, 1200, 750)
        self.setWindowTitle(self._res['mainWindowTitle'])
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(Path('../../data'))
    sys.exit(app.exec_())
