from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QStackedWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPlainTextEdit, QGroupBox,
                             QPushButton)

from controller.manager import ObjectManager, TemplateManager, SignageManager
from view.resource_manager import ResourceManager


class DataManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        self._stacked_widget = QStackedWidget()
        self._widget_idx = dict()
        self._widget_idx['type'] = self._stacked_widget.addWidget(DataTypeWidget())
        self._widget_idx['data'] = self._stacked_widget.addWidget(DataWidget())
        self.init_ui()

    def data_to_tree_item(self):
        data_type_items = []
        # For all data type
        for data_type_id in self._obj_mng._object_types.keys():
            data_type_item = QTreeWidgetItem([data_type_id])
            # Add data
            for data_id in self._obj_mng._object_values[self._obj_mng._object_types[data_type_id]].keys():
                data_item = QTreeWidgetItem([data_id])
                data_type_item.addChild(data_item)
            data_addition_item = QTreeWidgetItem(["+"])
            data_type_item.addChild(data_addition_item)
            data_type_items.append(data_type_item)
        return data_type_items

    def init_ui(self):
        # Left side of screen
        data_list = QTreeWidget()
        data_list.setHeaderLabel(self._res['dataTypeListLabel'])
        data_list.addTopLevelItems(self.data_to_tree_item())
        data_list.expandAll()
        data_list.itemSelectionChanged.connect(self.list_item_clicked)

        # Gather altogether
        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(data_list, 1)
        hbox_outmost.addWidget(self._stacked_widget, 4)
        self.setLayout(hbox_outmost)

    def list_item_clicked(self):
        get_selected = self.sender().selectedItems()
        if get_selected:
            item = get_selected[0]
            item_text = item.text(0)
            if item.parent() is None:
                # It is at topmost level
                # Selected one is data type
                idx = self._widget_idx['type']
                self._stacked_widget.widget(idx).load_data_on_ui(self._obj_mng, item_text)
                self._stacked_widget.setCurrentIndex(idx)
            else:
                if item_text == '+':
                    pass  # TODO: Add data addition logic
                else:
                    # Selected one is data
                    idx = self._widget_idx['data']
                    self._stacked_widget.widget(idx).load_data_on_ui()
                    self._stacked_widget.setCurrentIndex(idx)


class DataTypeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ledit_author = QLineEdit()
        self._ledit_homepage = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()
        self._ptedit_depend = QPlainTextEdit()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, obj_mng: ObjectManager, data_type_id: str):
        data_type = obj_mng._object_types[data_type_id]
        self._ledit_id.setText(data_type_id)
        self._ledit_name.setText(data_type._name)
        self._ledit_author.setText(data_type._dev_name)
        self._ledit_homepage.setText(data_type._dev_homepage)
        self._ptedit_descript.setPlainText(data_type._description)
        # TODO: Show user data type dependency

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

        group_name = QGroupBox(self._res['dataTypeNameLabel'])
        group_name.setLayout(vbox_name)

        # Author display
        self._ledit_author.setEnabled(False)
        vbox_author = QVBoxLayout()
        vbox_author.addWidget(self._ledit_author)

        group_author = QGroupBox(self._res['dataTypeAuthorLabel'])
        group_author.setLayout(vbox_author)

        # Homepage display
        self._ledit_homepage.setEnabled(False)
        vbox_homepage = QVBoxLayout()
        vbox_homepage.addWidget(self._ledit_homepage)

        group_homepage = QGroupBox(self._res['dataTypeHomepageLabel'])
        group_homepage.setLayout(vbox_homepage)

        # Description display
        self._ptedit_descript.setEnabled(False)
        vbox_descript = QVBoxLayout()
        vbox_descript.addWidget(self._ptedit_descript)

        group_descript = QGroupBox(self._res['dataTypeDescriptionLabel'])
        group_descript.setLayout(vbox_descript)

        # Dependency display
        self._ptedit_depend.setEnabled(False)
        vbox_depend = QVBoxLayout()
        vbox_depend.addWidget(self._ptedit_depend)

        group_depend = QGroupBox(self._res['dataTypeDependencyLabel'])
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
        vbox_outmost.addWidget(group_name)
        vbox_outmost.addWidget(group_author)
        vbox_outmost.addWidget(group_homepage)
        vbox_outmost.addWidget(group_descript)
        vbox_outmost.addWidget(group_depend)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)


class DataWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_id = QLineEdit()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self):
        pass  # TODO: Create logic

    def init_ui(self):
        # ID display
        label_id = QLabel(self._res['idLabel'])

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self._ledit_id)

        # TODO: Add data-type specific components

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
        vbox_outmost.addLayout(hbox_id)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)
