from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QComboBox, QTabWidget,
                             QTextBrowser, QMessageBox)
from typing import Callable
from datetime import datetime

import utils.utils as Utils
from controller.manager import TemplateManager
from model.signage import Frame
from model.template import FrameTemplate
from model.data_type import (StringDataType, BooleanDataType,
                             IntegerDataType, DateDataType)
from view.resource_manager import ResourceManager
from view.ui_components import (StringDataWidget, BooleanDataWidget,
                                IntegerDataWidget, DateTimeDataWidget)


class FrameWidget(QWidget):
    def __init__(self, tpl_mng: TemplateManager, value_change_handler: Callable[[Utils.ChangeType, str], None]):
        super().__init__()

        self._tpl_mng = tpl_mng
        self._frame = None
        self._value_change_handler = value_change_handler

        self._cbox_tpl = QComboBox()
        self._tab_data = FrameDataTab()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, frame: Frame) -> None:
        self._frame = frame
        # Change combobox item to frame's template
        tpl = frame.template
        idx = self._cbox_tpl.findText(Utils.gen_ui_text(tpl.definition.name, tpl.id))
        self._cbox_tpl.setCurrentIndex(idx)

        self._tab_data.load_data_on_ui(self._frame)

    def init_ui(self) -> None:
        # Template list on combobox
        tpl_list = list()
        for tpl_id in self._tpl_mng.frame_templates:
            template = self._tpl_mng.get_frame_template(tpl_id)
            tpl_list.append(Utils.gen_ui_text(template.definition.name, template.id))
        self._cbox_tpl.addItems(tpl_list)
        self._cbox_tpl.currentIndexChanged.connect(self.combobox_changed)

        # Tab widget
        tab_frame_manage = QTabWidget()
        tab_frame_manage.addTab(self._tab_data, self._res['dataTabText'])

        # Buttons
        btn_save = QPushButton(self._res['saveButtonText'])
        btn_save.clicked.connect(self.button_clicked)
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        btn_cancel.clicked.connect(self.button_clicked)

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

    def combobox_changed(self) -> None:
        combobox_text = self.sender().currentText()
        tpl_id = Utils.ui_text_to_id(combobox_text)
        tpl = self._tpl_mng.get_frame_template(tpl_id)
        self._tab_data.load_ui(tpl)

    def button_clicked(self) -> None:
        button_text = self.sender().text()
        if button_text == self._res['saveButtonText']:
            # Check is input data valid. If not, do not save it
            if not self._tab_data.is_data_valid():
                QMessageBox.warning(self, self._res['dataInvalidTitle'],
                                    self._res['dataInvalidDescription'],
                                    QMessageBox.Ok, QMessageBox.Ok)
                return

            # Now it's OK to save
            # Set frame's template
            tpl_id = Utils.ui_text_to_id(self._cbox_tpl.currentText())
            tpl = self._tpl_mng.get_frame_template(tpl_id)
            self._frame.template = tpl

            self._tab_data.save(self._frame)

            # Invoke value change handler to edit QTreeWidgetItem
            frame_text = Utils.gen_ui_text(tpl.definition.name, tpl.id)
            self._value_change_handler(Utils.ChangeType.SAVE, frame_text)
        elif button_text == self._res['cancelButtonText']:
            # Load the previous data
            self.load_data_on_ui(self._frame)


class FrameDataTab(QWidget):
    def __init__(self):
        super().__init__()

        self._vbox_data = QVBoxLayout()
        self._component_widgets = dict()  # id -> ComponentWidget
        self._tview_detail = QTextBrowser()

        self._res = ResourceManager()
        self.init_ui()

    def load_ui(self, template: FrameTemplate) -> None:
        # Clean the previous layout
        self._component_widgets = dict()
        for i in range(self._vbox_data.count()):
            widget = self._vbox_data.itemAt(0).widget()
            self._vbox_data.removeWidget(widget)
            widget.deleteLater()
        self._tview_detail.setText("")

        # Load the new layout
        fields = template.definition.fields
        for field_id in fields.keys():
            def clicked_handler(name: str, description: str, constraint: str) -> None:
                text = "<b>" + name + "</b><br />"
                text += description + "<br />"
                text += "Constraint: " + constraint
                self._tview_detail.setText(text)

            field = fields[field_id]  # Tuple[DataType, name, description]
            if isinstance(field[0], StringDataType):
                widget = StringDataWidget(field[0], field[1], field[2], clicked_handler)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
            elif isinstance(field[0], BooleanDataType):
                widget = BooleanDataWidget(field[0], field[1], field[2], clicked_handler)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
            elif isinstance(field[0], IntegerDataType):
                widget = IntegerDataWidget(field[0], field[1], field[2], clicked_handler)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
            elif isinstance(field[0], DateDataType):
                widget = DateTimeDataWidget(field[0], field[1], field[2], clicked_handler)
                widget.value = datetime.strptime(field[0].default, DateDataType.format)
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
                # TODO: Add more UI components according to data type

    def load_data_on_ui(self, frame: Frame) -> None:
        self.load_ui(frame.template)
        for field_id in frame.values.get_values().keys():
            field_value = frame.values.get_value(field_id)
            if field_id in self._component_widgets:  # TODO: This line should be removed
                self._component_widgets[field_id].value = field_value

    def init_ui(self) -> None:
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(self._vbox_data)
        vbox_outmost.addWidget(self._tview_detail)
        self.setLayout(vbox_outmost)

    def save(self, frame: Frame) -> None:
        # Gather all data
        values = dict()
        for field_id in self._component_widgets.keys():
            widget = self._component_widgets[field_id]
            values[field_id] = widget.value
        # Save it
        frame.values.set_values(**values)

    def is_data_valid(self) -> bool:
        for field_id in self._component_widgets.keys():
            widget = self._component_widgets[field_id]
            if not widget.is_data_valid():
                return False
        return True
