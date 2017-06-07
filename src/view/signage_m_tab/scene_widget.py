from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QComboBox, QTabWidget,
                             QTextBrowser, QMessageBox, QLineEdit,
                             QGroupBox, QCheckBox, QTimeEdit, QLabel)
from typing import Callable
from datetime import datetime

import utils.utils as utils
from controller.manager import TemplateManager, ObjectManager, MultimediaManager
from model.signage import Scene, TransitionType, ScheduleType, Signage
from model.template import SceneTemplate
from model.data_type import (StringDataType, BooleanDataType,
                             IntegerDataType, DateDataType, ObjectDataType, FileDataType, ListDataType)
from view.resource_manager import ResourceManager
from view.ui_components import (StringDataWidget, BooleanDataWidget,
                                IntegerDataWidget, DateTimeDataWidget, ObjectDataWidget, MediaWidget, ListDataWidget)


class SceneWidget(QWidget):
    def __init__(self, tpl_mng: TemplateManager, obj_mng: ObjectManager, mtm_mng: MultimediaManager, value_change_handler: Callable[[utils.ChangeType, str], None]):
        super().__init__()

        self._tpl_mng = tpl_mng
        self._obj_mng = obj_mng
        self._mtm_mng = mtm_mng

        self._cbox_tpl = QComboBox()
        self._tab_data = SceneDataTab(obj_mng, mtm_mng)
        self._tab_transition = SceneTransitionTab()
        self._tab_scheduling = SceneSchedulingTab()

        self._signage = None
        self._scene_idx = 0
        self._value_change_handler = value_change_handler

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, signage: Signage, scene_idx: int) -> None:
        # scene_idx from 0
        self._signage = signage
        self._scene_idx = scene_idx
        scene = signage.scenes[scene_idx]
        # Set current item of combobox
        tpl = scene.template
        idx = self._cbox_tpl.findText(utils.gen_ui_text(tpl.definition.name, tpl.id))
        self._cbox_tpl.setCurrentIndex(idx)

        self._tab_data.load_data_on_ui(scene)
        self._tab_transition.load_data_on_ui(scene)
        self._tab_scheduling.load_data_on_ui(scene)

    def init_ui(self) -> None:
        # Template list on combobox
        tpl_list = list()
        for tpl_id in self._tpl_mng.scene_templates:
            template = self._tpl_mng.get_scene_template(tpl_id)
            tpl_list.append(utils.gen_ui_text(template.definition.name, template.id))
        self._cbox_tpl.addItems(tpl_list)
        self._cbox_tpl.currentIndexChanged.connect(self.combobox_changed)

        # Tab widget
        tab_scene_manage = QTabWidget()
        tab_scene_manage.addTab(self._tab_data, self._res['dataTabText'])
        tab_scene_manage.addTab(self._tab_transition, self._res['transitionTabText'])
        tab_scene_manage.addTab(self._tab_scheduling, self._res['schedulingTabText'])

        # Buttons
        btn_delete = QPushButton(self._res['deleteButtonText'])
        btn_delete.clicked.connect(self.button_clicked)
        btn_save = QPushButton(self._res['saveButtonText'])
        btn_save.clicked.connect(self.button_clicked)
        btn_cancel = QPushButton(self._res['cancelButtonText'])
        btn_cancel.clicked.connect(self.button_clicked)

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

    def combobox_changed(self) -> None:
        combobox_text = self.sender().currentText()
        tpl_id = utils.ui_text_to_id(combobox_text)
        tpl = self._tpl_mng.get_scene_template(tpl_id)
        self._tab_data.load_ui(tpl)

    def button_clicked(self) -> None:
        button_text = self.sender().text()
        scene = self._signage.scenes[self._scene_idx]
        if button_text == self._res['deleteButtonText']:
            try:
                self._signage.remove_scene(self._signage.scenes[self._scene_idx])
            except ReferenceError as e:
                QMessageBox.warning(self, "Can't delete",
                                    "This scene can't be deleted. " + ', '.join(e.args[0].keys()) + " reference this",
                                    QMessageBox.Ok, QMessageBox.Ok)
                return
            self._value_change_handler(utils.ChangeType.DELETE, str(self._scene_idx))
        elif button_text == self._res['saveButtonText']:
            # Check is input data valid. If not, do not save it
            if not self._tab_data.is_data_valid() or \
               not self._tab_transition.is_data_valid() or \
               not self._tab_scheduling.is_data_valid():
                QMessageBox.warning(self, self._res['dataInvalidTitle'],
                                    self._res['dataInvalidDescription'],
                                    QMessageBox.Ok, QMessageBox.Ok)
                return

            # Now it's OK to save
            # Set scene's template
            tpl_id = utils.ui_text_to_id(self._cbox_tpl.currentText())
            tpl = self._tpl_mng.get_scene_template(tpl_id)

            scene.template = tpl

            self._tab_data.save(scene)
            self._tab_scheduling.save(scene)
            self._tab_transition.save(scene)

            # Invoke value change handler to edit QTreeWidgetItem
            scene_text = utils.gen_ui_text(tpl.definition.name, tpl.id)
            self._value_change_handler(utils.ChangeType.SAVE, scene_text)
        elif button_text == self._res['cancelButtonText']:
            # Load the previous data
            self.load_data_on_ui(self._signage, self._scene_idx)


class SceneDataTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, mtm_mng: MultimediaManager):
        super().__init__()

        self._vbox_data = QVBoxLayout()
        self._component_widgets = dict()  # id -> ComponentWidget
        self._tview_detail = QTextBrowser()

        self._obj_mng = obj_mng
        self._mtm_mng = mtm_mng

        self._res = ResourceManager()
        self.init_ui()

    def load_ui(self, template: SceneTemplate) -> None:
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
            elif isinstance(field[0], ObjectDataType):
                widget = ObjectDataWidget(field[0], field[1], field[2], clicked_handler, self._obj_mng)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
            elif isinstance(field[0], FileDataType):
                widget = MediaWidget(field[0] is self._mtm_mng.image_type, field[1], field[2], clicked_handler, self._mtm_mng)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
            elif isinstance(field[0], ListDataType):
                widget = ListDataWidget(field[0], field[1], field[2], clicked_handler)
                widget.value = field[0].default
                self._component_widgets[field_id] = widget
                self._vbox_data.addWidget(widget)
                # TODO: Add more UI components according to data type

    def load_data_on_ui(self, scene: Scene) -> None:
        # scene_idx from 0
        self.load_ui(scene.template)
        flat_values = scene.values.get_values(False)
        for field_id in scene.values.get_values().keys():
            field_value = flat_values[field_id]
            if field_id in self._component_widgets:  # TODO: This line should be removed
                self._component_widgets[field_id].value = field_value

    def init_ui(self) -> None:
        vbox_outmost = QVBoxLayout()
        vbox_outmost.addLayout(self._vbox_data)
        vbox_outmost.addWidget(self._tview_detail)
        self.setLayout(vbox_outmost)

    def save(self, scene: Scene) -> None:
        # Gather all data
        values = dict()
        for field_id in self._component_widgets.keys():
            widget = self._component_widgets[field_id]
            values[field_id] = widget.value
        # Save it
        scene.values.set_values(**values)

    def is_data_valid(self) -> bool:
        for field_id in self._component_widgets.keys():
            widget = self._component_widgets[field_id]
            if not widget.is_data_valid():
                return False
        return True


class SceneTransitionTab(QWidget):
    def __init__(self):
        super().__init__()

        self._ledit_duration = QLineEdit()
        self._cbox_type = QComboBox()

        self._res = ResourceManager()
        self.init_ui()

    @staticmethod
    def transition_type_to_text(transition_type: TransitionType) -> str:
        return transition_type.name.capitalize()

    @staticmethod
    def text_to_transition_type(text: str) -> TransitionType:
        return TransitionType[text.upper()]

    def load_data_on_ui(self, scene: Scene) -> None:
        self._ledit_duration.setText(str(scene.duration))
        idx = self._cbox_type.findText(self.transition_type_to_text(scene.transition_type))
        self._cbox_type.setCurrentIndex(idx)

    def init_ui(self) -> None:
        vbox_duration = QVBoxLayout()
        vbox_duration.addWidget(self._ledit_duration)

        group_duration = QGroupBox(self._res['sceneDurationLabel'])
        group_duration.setLayout(vbox_duration)

        transitions = [self.transition_type_to_text(TransitionType.NONE),
                       self.transition_type_to_text(TransitionType.PUSH),
                       self.transition_type_to_text(TransitionType.FADE)]
        self._cbox_type.addItems(transitions)

        vbox_transition = QVBoxLayout()
        vbox_transition.addWidget(self._cbox_type)

        group_transition = QGroupBox(self._res['sceneTransitionLabel'])
        group_transition.setLayout(vbox_transition)

        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(group_duration)
        vbox_outmost.addWidget(group_transition)
        vbox_outmost.addStretch(1)

        self.setLayout(vbox_outmost)

    def save(self, scene: Scene) -> None:
        scene.duration = int(self._ledit_duration.text())
        transition = self._cbox_type.currentText()
        scene.transition_type = self.text_to_transition_type(transition)

    def is_data_valid(self) -> bool:
        return self._ledit_duration.text().isdigit()


class SceneSchedulingTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()

        self._cbox_type = QComboBox()
        self._check_day = list()
        days = self._res['days'].split(', ')
        for day in days:
            self._check_day.append(QCheckBox(day))

        self._time_from = QTimeEdit()
        self._time_to = QTimeEdit()

        self.init_ui()

    @staticmethod
    def schedule_type_to_text(schedule_type: ScheduleType) -> str:
        return schedule_type.name.capitalize().replace('_', ' ')

    @staticmethod
    def text_to_schedule_type(text: str) -> ScheduleType:
        return ScheduleType[text.upper().replace(' ', '_')]

    def load_data_on_ui(self, scene: Scene) -> None:
        schedule = scene.schedule
        type_text = self.schedule_type_to_text(schedule.type)
        idx = self._cbox_type.findText(type_text)
        self._cbox_type.setCurrentIndex(idx)

        for i in range(7):
            self._check_day[i].setChecked(schedule.day_of_week[i])

        self._time_from.setTime(schedule.from_time)
        self._time_to.setTime(schedule.to_time)

    def init_ui(self) -> None:
        schedule_type = [self.schedule_type_to_text(ScheduleType.ALWAYS_HIDDEN),
                         self.schedule_type_to_text(ScheduleType.ALWAYS_VISIBLE),
                         self.schedule_type_to_text(ScheduleType.HIDDEN_ON_TIME),
                         self.schedule_type_to_text(ScheduleType.VISIBLE_ON_TIME)]
        self._cbox_type.addItems(schedule_type)

        vbox_schedule_type = QVBoxLayout()
        vbox_schedule_type.addWidget(self._cbox_type)

        group_schedule_type = QGroupBox(self._res['scheduleTypeLabel'])
        group_schedule_type.setLayout(vbox_schedule_type)

        hbox_day = QHBoxLayout()
        for i in range(len(self._check_day)):
            hbox_day.addWidget(self._check_day[i])

        group_day = QGroupBox(self._res['dayLabel'])
        group_day.setLayout(hbox_day)

        self._time_from.setDisplayFormat("HH:mm:ss")
        self._time_to.setDisplayFormat("HH:mm:ss")

        hbox_time = QHBoxLayout()
        hbox_time.addWidget(self._time_from)
        hbox_time.addWidget(QLabel('to'))
        hbox_time.addWidget(self._time_to)
        hbox_time.addStretch(1)

        group_time = QGroupBox(self._res['timeLabel'])
        group_time.setLayout(hbox_time)

        vbox_outmost = QVBoxLayout()
        vbox_outmost.addWidget(group_schedule_type)
        vbox_outmost.addWidget(group_day)
        vbox_outmost.addWidget(group_time)
        vbox_outmost.addStretch(1)

        self.setLayout(vbox_outmost)

    def save(self, scene: Scene) -> None:
        scene.schedule.type = self.text_to_schedule_type(self._cbox_type.currentText())

        day_of_week = list()
        for i in range(len(self._check_day)):
            day_of_week.append(self._check_day[i].isChecked())
        scene.schedule.day_of_week = day_of_week

        scene.schedule.from_time = self._time_from.time().toPyTime()
        scene.schedule.to_time = self._time_to.time().toPyTime()

    def is_data_valid(self) -> bool:
        return self._time_from.time() < self._time_to.time()
