from PyQt5.QtWidgets import (QWidget, QGroupBox, QLabel, QComboBox,
                             QVBoxLayout)

from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class StatusManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._update_labels = list()
        self._signage_cboxes = list()

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        # TODO: Make this UI view more flexible (i.e. when number of display changed)
        vbox_outmost = QVBoxLayout()
        for i in range(3):
            # Last update label
            label_update = QLabel("Last Update: 17.04.09. 23:05")
            self._update_labels.append(label_update)

            # Combobox for selecting signage
            cbox_signage = QComboBox()
            self._signage_cboxes.append(cbox_signage)

            vbox_content = QVBoxLayout()
            vbox_content.addWidget(label_update)
            vbox_content.addWidget(cbox_signage)

            group_display = QGroupBox("Display " + str(i+1))
            group_display.setLayout(vbox_content)

            vbox_outmost.addWidget(group_display)
        vbox_outmost.addStretch(1)

        self.setLayout(vbox_outmost)
