from PyQt5.QtWidgets import (QWidget, QTreeWidget, QGraphicsView, QTreeWidgetItem,
                             QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
                             QGroupBox, QPushButton)

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
