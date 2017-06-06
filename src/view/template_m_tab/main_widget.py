from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QHBoxLayout)

import utils.utils as utils
from .template_widget import TemplateWidget
from controller.manager import ObjectManager, TemplateManager, SignageManager, MultimediaManager, ChannelManager
from view.resource_manager import ResourceManager


class TemplateManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._res = ResourceManager()
        self._template_widget = TemplateWidget()
        self.init_ui()

    def template_to_tree_item(self) -> [QTreeWidgetItem]:
        frame_label_item = QTreeWidgetItem([self._res['frameLabel']])
        for frame_tpl_id in self._tpl_mng.frame_templates.keys():
            frame_tpl = self._tpl_mng.get_frame_template(frame_tpl_id)
            frame_text = utils.gen_ui_text(frame_tpl.definition.name, frame_tpl.id)
            frame_item = QTreeWidgetItem([frame_text])
            frame_label_item.addChild(frame_item)

        scene_label_item = QTreeWidgetItem([self._res['sceneLabel']])
        for scene_tpl_id in self._tpl_mng.scene_templates.keys():
            scene_tpl = self._tpl_mng.get_scene_template(scene_tpl_id)
            scene_text = utils.gen_ui_text(scene_tpl.definition.name, scene_tpl.id)
            scene_item = QTreeWidgetItem([scene_text])
            scene_label_item.addChild(scene_item)
        return [frame_label_item, scene_label_item]

    def init_ui(self) -> None:
        # Left side of screen
        multimedia_list = QTreeWidget()
        multimedia_list.setHeaderLabel(self._res['templateListLabel'])
        multimedia_list.addTopLevelItems(self.template_to_tree_item())
        multimedia_list.expandAll()
        multimedia_list.itemSelectionChanged.connect(self.list_item_clicked)

        # Gather altogether
        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(multimedia_list, 1)
        hbox_outmost.addWidget(self._template_widget, 4)
        self.setLayout(hbox_outmost)

    def list_item_clicked(self) -> None:
        get_selected = self.sender().selectedItems()
        if get_selected:
            item = get_selected[0]
            item_text = item.text(0)
            if item.parent() is None:
                # It is at topmost level
                # Selected one is Scene/Frame
                self._template_widget.clear_data_on_ui()
            else:
                # Selected one is frame/scene
                tpl_id = utils.ui_text_to_id(item_text)
                if item.parent().text(0) == self._res['frameLabel']:
                    # Selected one is frame template
                    tpl = self._tpl_mng.get_frame_template(tpl_id)
                else:
                    # Selected one is scene template
                    tpl = self._tpl_mng.get_scene_template(tpl_id)
                self._template_widget.load_data_on_ui(tpl)
