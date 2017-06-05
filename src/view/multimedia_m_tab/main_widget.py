from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout)

from .multimedia_widget import MultimediaWidget
from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class MultimediaManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        self._media_widget = MultimediaWidget()
        self.init_ui()

    def multimedia_to_tree_item(self):
        # TODO: This is dummy code. Add functionality
        video_item = QTreeWidgetItem(['Video'])
        video_item.addChild(QTreeWidgetItem(['hello.mp4']))
        return [video_item]

    def init_ui(self):
        # Left side of screen
        multimedia_list = QTreeWidget()
        multimedia_list.setHeaderLabel(self._res['multimediaListLabel'])
        multimedia_list.addTopLevelItems(self.multimedia_to_tree_item())
        multimedia_list.expandAll()
        multimedia_list.itemSelectionChanged.connect(self.list_item_clicked)

        # Gather altogether
        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(multimedia_list, 1)
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
                pass
            else:
                if item_text == '+':
                    pass  # TODO: Add multimedia addition logic
                else:
                    # Selected one is multimedia
                    self._media_widget.load_data_on_ui()

