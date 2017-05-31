import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget,
                             QPushButton, QHBoxLayout, QVBoxLayout)
from view.resource_manager import ResourceManager


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

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
        tab_widget_main = QTabWidget()  # TODO: Change this to custom tab widget class

        # Layout buttons and tab widget
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_buttons)
        vbox_outmost.addWidget(tab_widget_main)

        # Set layout
        self.setLayout(vbox_outmost)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.initUI()

    def initUI(self):
        main_widget = MainWidget()
        self.setCentralWidget(main_widget)

        self.setGeometry(300, 300, 1200, 750)
        self.setWindowTitle(self._res['mainWindowTitle'])
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
