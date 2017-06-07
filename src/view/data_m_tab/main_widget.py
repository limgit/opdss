from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QStackedWidget, QHBoxLayout, QMessageBox, QInputDialog)

import utils.utils as utils
from model.data_value import ObjectValue
from .data_type_widget import DataTypeWidget
from .data_widget import DataWidget
from controller.manager import ObjectManager, TemplateManager, SignageManager, MultimediaManager, ChannelManager
from view.resource_manager import ResourceManager


class DataManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager,
                 mtm_mng: MultimediaManager, chn_mng: ChannelManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng
        self._chn_mng = chn_mng

        self._data_list = QTreeWidget()

        self._res = ResourceManager()
        self._stacked_widget = QStackedWidget()
        self._widget_idx = dict()
        self.init_ui()

    def data_to_tree_item(self):
        data_type_items = []
        # For all data type
        for data_type_id in self._obj_mng.object_types.keys():
            data_type = self._obj_mng.get_object_type(data_type_id)
            data_type_text = utils.gen_ui_text(data_type.name, data_type.id)
            data_type_item = QTreeWidgetItem([data_type_text])
            # Add data
            for data_id in self._obj_mng.get_object_values(data_type).keys():
                data_item = QTreeWidgetItem([data_id])
                data_type_item.addChild(data_item)
            data_addition_item = QTreeWidgetItem(["+"])
            data_type_item.addChild(data_addition_item)
            data_type_items.append(data_type_item)
        return data_type_items

    def init_ui(self):
        # Left side of screen
        self._data_list.setHeaderLabel(self._res['dataTypeListLabel'])
        self._data_list.addTopLevelItems(self.data_to_tree_item())
        self._data_list.expandAll()
        self._data_list.itemSelectionChanged.connect(self.list_item_clicked)

        def data_type_change_handler(change_type: utils.ChangeType, data_text: str='') -> None:
            # Get selected signage item
            get_selected = self._data_list.selectedItems()
            if get_selected:
                item = get_selected[0]
                if change_type == utils.ChangeType.DELETE:
                    # Remove QTreeWidgetItem
                    self._data_list.removeItemWidget(item)
        data_type_widget = DataTypeWidget(self._obj_mng, data_type_change_handler)
        self._widget_idx['type'] = self._stacked_widget.addWidget(data_type_widget)

        def data_change_handler(change_type: utils.ChangeType, data_text: str='') -> None:
            # Get selected signage item
            get_selected = self._data_list.selectedItems()
            if get_selected:
                item = get_selected[0]
                if change_type == utils.ChangeType.SAVE:
                    # Update QTreeWidgetItem
                    item.setText(0, data_text)
                elif change_type == utils.ChangeType.DELETE:
                    # Remove QTreeWidgetItem
                    parent = item.parent()
                    parent.removeChild(item)
                    parent.setSelected(True)
        data_widget = DataWidget(self._obj_mng, self._mtm_mng, data_change_handler)
        self._widget_idx['data'] = self._stacked_widget.addWidget(data_widget)

        # Gather altogether
        hbox_outmost = QHBoxLayout()
        hbox_outmost.addWidget(self._data_list, 1)
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
                data_type_id = utils.ui_text_to_id(item_text)
                data_type = self._obj_mng.get_object_type(data_type_id)
                self._stacked_widget.widget(idx).load_data_on_ui(data_type)
                self._stacked_widget.setCurrentIndex(idx)
            else:
                if item_text == '+':
                    item.setSelected(False)
                    text, ok = QInputDialog.getText(self, self._res['idDialogTitle'],
                                                    self._res['idDialogDescription'])
                    if ok:
                        try:
                            utils.validate_id(text)
                        except AttributeError:
                            QMessageBox.warning(self, self._res['idInvalidTitle'],
                                                self._res['idInvalidDescription'],
                                                QMessageBox.Ok, QMessageBox.Ok)
                            return  # Invalid ID. Do not create signage
                        data_type_id = utils.ui_text_to_id(item.parent().text(0))
                        data_type = self._obj_mng.get_object_type(data_type_id)
                        self._obj_mng.add_object_value(ObjectValue(text, data_type, self._obj_mng, self._mtm_mng))
                        item.setText(0, text)
                        item.parent().addChild(QTreeWidgetItem(['+']))
                else:
                    # Selected one is data
                    idx = self._widget_idx['data']
                    data_type_id = utils.ui_text_to_id(item.parent().text(0))
                    data_type = self._obj_mng.get_object_type(data_type_id)
                    data = self._obj_mng.get_object_value(data_type, item_text)
                    self._stacked_widget.widget(idx).load_data_on_ui(data)
                    self._stacked_widget.setCurrentIndex(idx)
