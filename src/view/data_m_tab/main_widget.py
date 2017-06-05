from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QStackedWidget, QHBoxLayout)

from .data_type_widget import DataTypeWidget
from .data_widget import DataWidget
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
