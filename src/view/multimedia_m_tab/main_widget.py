from pathlib import Path

from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QFileDialog)

import utils.utils as utils
from .multimedia_widget import MultimediaWidget
from controller.manager import ObjectManager, TemplateManager, SignageManager, MultimediaManager, ChannelManager
from view.resource_manager import ResourceManager


class MultimediaManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._res = ResourceManager()
        self._multimedia_list = QTreeWidget()

        def multimedia_change_handler(change_type: utils.ChangeType, mtm_text: str=''):
            get_selected = self._multimedia_list.selectedItems()
            if get_selected:
                item = get_selected[0]
                if change_type == utils.ChangeType.DELETE:
                    parent = item.parent()
                    parent.removeChild(item)
        self._media_widget = MultimediaWidget(self._mtm_mng, multimedia_change_handler)
        self.init_ui()

    def multimedia_to_tree_item(self) -> [QTreeWidgetItem]:
        video_label_item = QTreeWidgetItem(['Video'])
        for video_id in self._mtm_mng.videos.keys():
            video_item = QTreeWidgetItem([video_id])
            video_label_item.addChild(video_item)
        video_label_item.addChild(QTreeWidgetItem(['+']))

        image_label_item = QTreeWidgetItem(['Image'])
        for image_id in self._mtm_mng.images.keys():
            image_item = QTreeWidgetItem([image_id])
            image_label_item.addChild(image_item)
        image_label_item.addChild(QTreeWidgetItem(['+']))

        return [video_label_item, image_label_item]

    def init_ui(self):
        # Left side of screen
        self._multimedia_list = QTreeWidget()
        self._multimedia_list.setHeaderLabel(self._res['multimediaListLabel'])
        self._multimedia_list.addTopLevelItems(self.multimedia_to_tree_item())
        self._multimedia_list.expandAll()
        self._multimedia_list.itemSelectionChanged.connect(self.list_item_clicked)

        # Gather altogether
        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(self._multimedia_list, 1)
        hbox_outmost.addWidget(self._media_widget, 4)
        self.setLayout(hbox_outmost)

    def list_item_clicked(self):
        get_selected = self.sender().selectedItems()
        if get_selected:
            item = get_selected[0]
            item_text = item.text(0)
            if item.parent() is None:
                # It is at topmost level
                # Selected one is Video/Image
                self._media_widget.clear_data_on_ui()
            else:
                if item_text == '+':
                    item.setSelected(False)
                    if item.parent().text(0) == "Image":
                        title = "Select Image"
                        extensions = "JPG Files (*.jpg);;JPEG Files (*.jpeg);;PNG Files (*.png)"
                    else:
                        title = "Select Video"
                        extensions = "MP4 Files (*.mp4);;OGG Files (*.ogg)"
                    options = QFileDialog.Options()
                    options |= QFileDialog.DontUseNativeDialog
                    file_name, _ = QFileDialog.getOpenFileName(self, title, "",
                                                               extensions, options=options)
                    if file_name:
                        if item.parent().text(0) == "Image":
                            self._mtm_mng.add_image(Path(file_name))
                        else:
                            self._mtm_mng.add_video(Path(file_name))
                        file_id = file_name.split('/')[-1]
                        item.setText(0, file_id)

                        item.parent().addChild(QTreeWidgetItem(['+']))
                else:
                    # Selected one is multimedia
                    if item.parent().text(0) == 'Image':
                        # Selected one is image
                        mtm = self._mtm_mng.get_image(item_text)
                    else:
                        # Selected one is video
                        mtm = self._mtm_mng.get_video(item_text)
                    self._media_widget.load_data_on_ui(mtm)

