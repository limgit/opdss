from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QComboBox, QTabWidget)

import utils.utils as Utils
from controller.manager import TemplateManager, SignageManager
from model.signage import Signage
from model.template import SceneTemplate
from model.data_type import StringDataType
from view.resource_manager import ResourceManager
from view.ui_components import StringDataWidget


class SceneWidget(QWidget):
    def __init__(self, sgn_mng: SignageManager, tpl_mng: TemplateManager):
        super().__init__()

        self._sgn_mng = sgn_mng
        self._tpl_mng = tpl_mng

        self._cbox_tpl = QComboBox()
        self._tab_data = SceneDataTab()
        self._tab_transition = SceneTransitionTab()
        self._tab_scheduling = SceneSchedulingTab()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, sgn_id: str, scene_idx: int) -> None:
        # scene_idx from 0
        # Set current item of combobox
        signage = self._sgn_mng.get_signage(sgn_id)
        tpl = signage.scenes[scene_idx].template
        idx = self._cbox_tpl.findText(Utils.gen_ui_text(tpl.definition.name, tpl.id))
        self._cbox_tpl.setCurrentIndex(idx)

        self._tab_data.load_data_on_ui(signage, scene_idx)
        self._tab_transition.load_data_on_ui()
        self._tab_scheduling.load_data_on_ui()

    def init_ui(self) -> None:
        # Template list on combobox
        tpl_list = list()
        for tpl_id in self._tpl_mng.scene_templates:
            template = self._tpl_mng.get_scene_template(tpl_id)
            tpl_list.append(Utils.gen_ui_text(template.definition.name, template.id))
        self._cbox_tpl.addItems(tpl_list)

        # Tab widget
        tab_scene_manage = QTabWidget()
        tab_scene_manage.addTab(self._tab_data, self._res['dataTabText'])
        tab_scene_manage.addTab(self._tab_transition, self._res['transitionTabText'])
        tab_scene_manage.addTab(self._tab_scheduling, self._res['schedulingTabText'])

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
        vbox_outmost.addWidget(self._cbox_tpl)
        vbox_outmost.addWidget(tab_scene_manage)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)


class SceneDataTab(QWidget):
    def __init__(self):
        super().__init__()

        self._vbox_data = QVBoxLayout()
        self._component_widgets = dict()  # id -> ComponentWidget

        self._res = ResourceManager()
        self.init_ui()

    def load_ui(self, template: SceneTemplate) -> None:
        # Clean the previous layout
        self._component_widgets = dict()
        for i in range(self._vbox_data.count()):
            self._vbox_data.itemAt(0).widget().setParent(None)

        # Load the new layout
        fields = template.definition.fields
        for field_id in fields.keys():
            field = fields[field_id]  # Tuple[DataType, name, description]
            if isinstance(field[0], StringDataType):
                widget = StringDataWidget(field[0], field[1], field[2])
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
            # TODO: Add more UI components according to data type

        self.setLayout(self._vbox_data)

    def load_data_on_ui(self, signage: Signage, scene_idx: int) -> None:
        # scene_idx from 0
        scene = signage.scenes[scene_idx]
        self.load_ui(scene.template)
        for field_id in scene.values.get_values().keys():
            field_value = scene.values.get_value(field_id)
            if field_id in self._component_widgets:  # TODO: This line should be removed
                self._component_widgets[field_id].value = field_value

    def init_ui(self) -> None:
        pass  # Nothing needed


class SceneTransitionTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self) -> None:
        pass  # TODO: Add functionality

    def init_ui(self) -> None:
        pass  # TODO: Add functionality


class SceneSchedulingTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self) -> None:
        pass  # TODO: Add functionality

    def init_ui(self) -> None:
        pass  # TODO: Add functionality
