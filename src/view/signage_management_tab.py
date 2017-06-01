from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QStackedWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPlainTextEdit, QGroupBox,
                             QPushButton, QComboBox, QTabWidget)

from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class SignageManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        self._stacked_widget = QStackedWidget()
        self._widget_idx = dict()
        self._widget_idx['signage'] = self._stacked_widget.addWidget(SignageWidget())
        self._widget_idx['frame'] = self._stacked_widget.addWidget(FrameWidget())
        # TODO: Add widgets for scene
        self.initUI()

    def signage_to_tree_item(self):
        top_level_items = []
        # For all signage
        for key in self._sgn_mng._signages.keys():
            top_item = QTreeWidgetItem([key])
            frame_item = QTreeWidgetItem(["F:"])  # Add frame
            top_item.addChild(frame_item)
            idx = 1
            # Add signage
            for scene in self._sgn_mng._signages[key]._scene:
                scene_template_name = scene._template._definition._name
                scene_item = QTreeWidgetItem([str(idx) + ":" + scene_template_name])
                top_item.addChild(scene_item)
                idx += 1
            scene_addition_item = QTreeWidgetItem(["+"])
            top_item.addChild(scene_addition_item)
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
        signage_list.itemSelectionChanged.connect(self.list_item_clicked)

        # TODO: Add Up/Down button

        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(signage_list, 1)
        hbox_outmost.addWidget(self._stacked_widget, 5)
        self.setLayout(hbox_outmost)

    def list_item_clicked(self):
        get_selected = self.sender().selectedItems()
        if get_selected:
            item = get_selected[0]
            item_text = item.text(0)
            if item.parent() is None:
                # It is at topmost level
                if item_text == "+":
                    pass  # TODO: Add signage addition logic
                else:
                    idx = self._widget_idx['signage']
                    self._stacked_widget.widget(idx).load_data_on_UI(self._sgn_mng, item_text)
                    self._stacked_widget.setCurrentIndex(idx)
            else:
                if item_text.startswith("F:"):
                    # Selected one is frame
                    idx = self._widget_idx['frame']
                    self._stacked_widget.widget(idx).load_data_on_UI()
                    self._stacked_widget.setCurrentIndex(idx)
                elif item_text == '+':
                    pass  # TODO: Add scene addition logic
                else:
                    # Selected one is scene
                    pass


class SignageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()

        self._res = ResourceManager()
        self.initUI()

    def load_data_on_UI(self, sgn_mng: SignageManager, sgn_id: str):
        signage = sgn_mng._signages[sgn_id]
        self._ledit_id.setText(sgn_id)
        self._ledit_name.setText(signage._title)
        self._ptedit_descript.setPlainText(signage._description)

    def initUI(self):
        # ID display
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        # Name display
        vbox_name = QVBoxLayout()
        vbox_name.addWidget(self._ledit_name)

        group_name = QGroupBox(self._res['signageNameLabel'])
        group_name.setLayout(vbox_name)

        # Description display
        vbox_descript = QVBoxLayout()
        vbox_descript.addWidget(self._ptedit_descript)

        group_descript = QGroupBox(self._res['signageDescriptionLabel'])
        group_descript.setLayout(vbox_descript)

        # Buttons
        btn_delete = QPushButton(self._res['deleteButtonText'])
        # TODO: Add functionality
        btn_save = QPushButton(self._res['saveButtonText'])
        # TODO: Add functionality
        btn_cancel = QPushButton(self._res['cancelButtonText'])

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_delete)
        hbox_buttons.addWidget(btn_save)
        hbox_buttons.addWidget(btn_cancel)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(hbox_id)
        vbox_outmost.addWidget(group_name)
        vbox_outmost.addWidget(group_descript)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)


class FrameWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._cbox_tpl = QComboBox()
        self._tab_data = FrameDataTab()

        self._res = ResourceManager()
        self.initUI()

    def load_data_on_UI(self):
        # TODO: Maybe more functionality?
        self._tab_data.load_data_on_UI()

    def initUI(self):
        # TODO: Read template list and add it by cbox.addItems(list)
        # Tab widget
        tab_frame_manage = QTabWidget()
        tab_frame_manage.addTab(self._tab_data, self._res['dataTabText'])

        # Buttons
        btn_save = QPushButton(self._res['saveButtonText'])
        # TODO: Add functionality
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        # TODO: Add functionality

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)
        hbox_buttons.addWidget(btn_save)
        hbox_buttons.addWidget(btn_cancel)

        # Getting altogether
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(self._cbox_tpl)
        vbox_outmost.addWidget(tab_frame_manage)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)


class FrameDataTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.initUI()

    def load_data_on_UI(self):
        pass  # TODO: Add functionality

    def initUI(self):
        # TODO: This is dummy code. Have to edit it
        vbox = QVBoxLayout()
        self.setLayout(vbox)


class SceneWidget(QWidget):
    pass
