from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QHBoxLayout)

from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class SignageManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        self.initUI()

    def signage_to_tree_item(self):
        top_level_items = []
        # For all signage
        for key in self._sgn_mng._signages.keys():
            top_item = QTreeWidgetItem([key])
            frame_item = QTreeWidgetItem(["F:"])  # Add frame
            top_item.addChild(frame_item)
            idx = 1
            # Add signages
            for scene in self._sgn_mng._signages[key]._scene:
                scene_template_name = scene._template._definition._name
                scene_item = QTreeWidgetItem([str(idx) + ":" + scene_template_name])
                top_item.addChild(scene_item)
                idx += 1
            top_level_items.append(top_item)
        signage_addition_item = QTreeWidgetItem(["+"])
        top_level_items.append(signage_addition_item)
        return top_level_items

    def initUI(self):
        # Left side of screen
        signage_list = QTreeWidget()
        signage_list.setHeaderLabel('Signage')
        signage_list.addTopLevelItems(self.signage_to_tree_item())
        signage_list.expandAll()

        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(signage_list)
        self.setLayout(hbox_outmost)
        # Right side of screen

