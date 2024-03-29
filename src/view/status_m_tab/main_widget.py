from PyQt5.QtWidgets import (QWidget, QGroupBox, QLabel, QComboBox,
                             QVBoxLayout)

import utils.utils as utils
from controller.manager import ObjectManager, TemplateManager, SignageManager, MultimediaManager, ChannelManager
from model.channel import Channel
from view.resource_manager import ResourceManager


class StatusManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._widgets = list()

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        vbox_outmost = QVBoxLayout()
        for channel_id in self._chn_mng.channels.keys():
            widget = ChannelWidget(self._chn_mng.channels[channel_id], self._sgn_mng)
            self._widgets.append(widget)
            vbox_outmost.addWidget(widget)
        vbox_outmost.addStretch(1)

        self.setLayout(vbox_outmost)

    def showEvent(self, event):
        for i in range(len(self._widgets)):
            self._widgets[i].load_data_on_ui()


class ChannelWidget(QGroupBox):
    def __init__(self, channel: Channel, sgn_mng: SignageManager):
        super().__init__()

        self._channel = channel
        self._sgn_mng = sgn_mng

        self._label = QLabel()
        self._cbox_signages = QComboBox()

        self.init_ui()

    def load_data_on_ui(self) -> None:
        self._cbox_signages.clear()
        sgn = self._channel.signage
        signage_texts = list()
        curr_sgn_idx = 0
        for sgn_id in self._sgn_mng.signages.keys():
            if sgn_id == sgn.id:
                curr_sgn_idx = len(signage_texts)
            signage = self._sgn_mng.get_signage(sgn_id)
            signage_texts.append(utils.gen_ui_text(signage.title, signage.id))

        self._cbox_signages.addItem(signage_texts[curr_sgn_idx])
        for sgn_text in reversed(signage_texts[:curr_sgn_idx]):
            self._cbox_signages.insertItem(0, sgn_text)
        for sgn_text in signage_texts[curr_sgn_idx+1:]:
            self._cbox_signages.addItem(sgn_text)
        label_text = "Number of connections: " + str(self._channel.request_connection_count())
        self._label.setText(label_text)

    def init_ui(self) -> None:
        self.setTitle(self._channel.id)

        signage_texts = list()
        for sgn_id in self._sgn_mng.signages.keys():
            signage = self._sgn_mng.get_signage(sgn_id)
            signage_texts.append(utils.gen_ui_text(signage.title, signage.id))
        self._cbox_signages.addItems(signage_texts)
        self._cbox_signages.currentIndexChanged.connect(self._signage_changed)

        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(self._label)
        vbox_outmost.addWidget(self._cbox_signages)

        self.setLayout(vbox_outmost)

    def _signage_changed(self):
        sgn_id = utils.ui_text_to_id(self._cbox_signages.currentText())
        if not sgn_id:
            return

        self._channel.signage = self._sgn_mng.get_signage(sgn_id)
