from PyQt5.QtWidgets import (QWidget, QGraphicsView, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QGroupBox, QPushButton)

from view.resource_manager import ResourceManager


class MultimediaWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_name = QLineEdit()
        self._gview_preview = QGraphicsView()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self):
        pass  # TODO: Add functionality

    def init_ui(self):
        # Name display
        label_name = QLabel(self._res['nameLabel'])

        hbox_name = QHBoxLayout()
        hbox_name.addWidget(label_name)
        hbox_name.addWidget(self._ledit_name)

        # Preview display
        vbox_preview = QVBoxLayout()
        vbox_preview.addWidget(self._gview_preview)

        group_preview = QGroupBox(self._res['multimediaPreviewLabel'])
        group_preview.setLayout(vbox_preview)

        # Buttons
        btn_delete = QPushButton(self._res['deleteButtonText'])
        # TODO: Add functionality
        btn_save = QPushButton(self._res['saveButtonText'])
        # TODO: Add functionality
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        # TODO: Add functionality

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_delete)
        hbox_buttons.addWidget(btn_save)
        hbox_buttons.addWidget(btn_cancel)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_name)
        vbox_outmost.addWidget(group_preview)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)