from PyQt5.QtWidgets import (QWidget, QTreeWidget, QGraphicsView, QTreeWidgetItem,
                             QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
                             QPlainTextEdit, QGroupBox, QPushButton)

from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class TemplateManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        self._template_widget = TemplateWidget()
        self.init_ui()

    def template_to_tree_item(self):
        # TODO: This is dummy code. Add functionality
        frame_label_item = QTreeWidgetItem(['Frame'])
        scene_label_item = QTreeWidgetItem(['Scene'])
        for scene_tpl_id in self._tpl_mng._scene_templates.keys():
            scene_item = QTreeWidgetItem([scene_tpl_id])
            scene_label_item.addChild(scene_item)
        return [frame_label_item, scene_label_item]

    def init_ui(self):
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

    def list_item_clicked(self):
        get_selected = self.sender().selectedItems()
        if get_selected:
            item = get_selected[0]
            item_text = item.text(0)
            if item.parent() is None:
                # It is at topmost level
                # Selected one is Scene/Frame
                pass
            else:
                # Selected one is scene/frame
                self._template_widget.load_data_on_ui()


class TemplateWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ledit_author = QLineEdit()
        self._gview_thumbnail = QGraphicsView()
        self._ledit_homepage = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()
        self._ptedit_depend = QPlainTextEdit()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self):
        pass  # TODO: Add functionality

    def init_ui(self):
        # ID display
        self._ledit_id.setEnabled(False)
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        # Name display
        self._ledit_name.setEnabled(False)
        vbox_name = QVBoxLayout()
        vbox_name.addWidget(self._ledit_name)

        group_name = QGroupBox(self._res['templateNameLabel'])
        group_name.setLayout(vbox_name)

        # Author display
        self._ledit_author.setEnabled(False)
        vbox_author = QVBoxLayout()
        vbox_author.addWidget(self._ledit_author)

        group_author = QGroupBox(self._res['templateAuthorLabel'])
        group_author.setLayout(vbox_author)

        vbox_name_author = QVBoxLayout()
        vbox_name_author.addWidget(group_name)
        vbox_name_author.addWidget(group_author)

        # Thumbnail display
        hbox_wrapper = QHBoxLayout()
        hbox_wrapper.addLayout(vbox_name_author)
        hbox_wrapper.addWidget(self._gview_thumbnail)

        # Homepage display
        self._ledit_homepage.setEnabled(False)
        vbox_homepage = QVBoxLayout()
        vbox_homepage.addWidget(self._ledit_homepage)

        group_homepage = QGroupBox(self._res['templateHomepageLabel'])
        group_homepage.setLayout(vbox_homepage)

        # Description display
        self._ptedit_descript.setEnabled(False)
        vbox_descript = QVBoxLayout()
        vbox_descript.addWidget(self._ptedit_descript)

        group_descript = QGroupBox(self._res['templateDescriptionLabel'])
        group_descript.setLayout(vbox_descript)

        # Dependency display
        self._ptedit_depend.setEnabled(False)
        vbox_depend = QVBoxLayout()
        vbox_depend.addWidget(self._ptedit_depend)

        group_depend = QGroupBox(self._res['templateDependencyLabel'])
        group_depend.setLayout(vbox_depend)

        # Button
        btn_delete = QPushButton(self._res['deleteButtonText'])
        # TODO: Add functionality

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_delete)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_id)
        vbox_outmost.addLayout(hbox_wrapper)
        vbox_outmost.addWidget(group_homepage)
        vbox_outmost.addWidget(group_descript)
        vbox_outmost.addWidget(group_depend)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)
