import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QPushButton, QHBoxLayout, QVBoxLayout)

from webserver.web_server import WebServer
from controller.manager import (ObjectManager, TemplateManager,
                                SignageManager, MultimediaManager,
                                ChannelManager)
from view.resource_manager import ResourceManager
from view.main_tab_widget import MainTabWidget


class MainWidget(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._res = ResourceManager()

        self._web_server = WebServer(self._chn_mng, self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng)

        self._btn_run = QPushButton(self._res['runButtonText'])
        self._btn_stop = QPushButton(self._res['stopButtonText'])

        self._vbox_outmost = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
        # Run button
        self._btn_run.clicked.connect(self.button_clicked)

        # Stop button
        self._btn_stop.clicked.connect(self.button_clicked)
        self._btn_stop.setEnabled(False)

        # Refresh button
        btn_refresh = QPushButton(self._res['refreshButtonText'])
        btn_refresh.clicked.connect(self.button_clicked)

        # Tab widget
        tab_widget_main = MainTabWidget(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)

        # Layout buttons
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self._btn_run)
        hbox_buttons.addWidget(self._btn_stop)
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_refresh)

        # Layout buttons and tab widget
        self._vbox_outmost.addLayout(hbox_buttons)
        self._vbox_outmost.addWidget(tab_widget_main)

        # Set layout
        self.setLayout(self._vbox_outmost)

    def button_clicked(self):
        button_text = self.sender().text()
        if button_text == self._res['runButtonText']:
            self._btn_run.setEnabled(False)
            self._btn_stop.setEnabled(True)
            self._web_server.start()
        elif button_text == self._res['stopButtonText']:
            self._btn_run.setEnabled(True)
            self._btn_stop.setEnabled(False)
            self._web_server.stop()
        elif button_text == self._res['refreshButtonText']:
            widget = self._vbox_outmost.itemAt(1).widget()
            self._vbox_outmost.removeWidget(widget)
            widget.deleteLater()
            tab_widget_mainn = MainTabWidget(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
            self._vbox_outmost.addWidget(tab_widget_mainn)





class MainWindow(QMainWindow):
    def __init__(self, root_path: Path):
        super().__init__()

        self._root_path = root_path.resolve()

        self._mtm_mng = MultimediaManager(root_path / 'media')
        self._obj_mng = ObjectManager(self._root_path / 'data', self._mtm_mng)
        self._tpl_mng = TemplateManager(self._root_path / 'template', self._obj_mng)
        self._sgn_mng = SignageManager(self._root_path / 'signage', self._obj_mng, self._tpl_mng)
        self._chn_mng = ChannelManager(self._root_path / 'channel', self._sgn_mng)

        self._mtm_mng.bind_managers(self._sgn_mng, self._obj_mng)
        self._obj_mng.bind_managers(self._tpl_mng, self._sgn_mng)

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        main_widget = MainWidget(self._obj_mng, self._tpl_mng, self._sgn_mng, self._mtm_mng, self._chn_mng)
        self.setCentralWidget(main_widget)

        self.setGeometry(300, 300, 1200, 750)
        self.setWindowTitle(self._res['mainWindowTitle'])
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(Path('../../data'))
    sys.exit(app.exec_())
