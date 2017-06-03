from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QStackedWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QPlainTextEdit, QGroupBox,
                             QPushButton, QComboBox, QTabWidget)
from typing import Callable
from enum import Enum, auto
import random

import utils.utils as Utils
from controller.manager import ObjectManager, TemplateManager, SignageManager
from model.data_value import ObjectValue
from model.signage import Scene
from view.resource_manager import ResourceManager


class ChangeType(Enum):
    DELETE = auto()
    SAVE = auto()


class Direction(Enum):
    UP = auto()
    DOWN = auto()


class SignageManagementTab(QWidget):
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        super().__init__()

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._res = ResourceManager()
        # Left part of screen
        self._signage_list = QTreeWidget()
        self._btn_up = QPushButton(self._res['upButtonText'])
        self._btn_down = QPushButton(self._res['downButtonText'])
        # Right part of screen
        self._stacked_widget = QStackedWidget()
        self._widget_idx = dict()

        self.init_ui()

    def signage_to_tree_item(self) -> [QTreeWidgetItem]:
        signage_items = []
        # For all signage
        for signage_id in self._sgn_mng.signages.keys():
            signage = self._sgn_mng.get_signage(signage_id)
            signage_text = Utils.gen_ui_text(signage.title, signage.id)
            signage_item = QTreeWidgetItem([signage_text])

            # Add frame
            frame_tpl = signage.frame.template
            frame_text = Utils.gen_ui_text(frame_tpl.definition.name, frame_tpl.id)
            frame_item = QTreeWidgetItem(["F:" + frame_text])
            signage_item.addChild(frame_item)

            # Add scene
            idx = 1
            for scene in signage.scenes:
                scene_tpl = scene.template
                scene_text = Utils.gen_ui_text(scene_tpl.definition.name, scene_tpl.id)
                scene_item = QTreeWidgetItem([str(idx) + ":" + scene_text])
                signage_item.addChild(scene_item)
                idx += 1

            # Add scene addition button
            scene_addition_item = QTreeWidgetItem(["+"])
            signage_item.addChild(scene_addition_item)
            signage_items.append(signage_item)

        # Add signage addition button
        signage_addition_item = QTreeWidgetItem(["+"])
        signage_items.append(signage_addition_item)
        return signage_items

    def init_ui(self) -> None:
        # Left side of screen
        self._signage_list.setHeaderLabel(self._res['signageListLabel'])
        self._signage_list.addTopLevelItems(self.signage_to_tree_item())
        self._signage_list.expandAll()
        self._signage_list.itemSelectionChanged.connect(self.update_ui_component)

        # Buttons
        self._btn_up.clicked.connect(self.move_button_clicked)
        self._btn_down.clicked.connect(self.move_button_clicked)
        # Disable at first
        self._btn_up.setEnabled(False)
        self._btn_down.setEnabled(False)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self._btn_up)
        hbox_buttons.addWidget(self._btn_down)

        vbox_left = QVBoxLayout()
        vbox_left.addWidget(self._signage_list)
        vbox_left.addLayout(hbox_buttons)

        # Right side of screen
        def signage_change_handler(change_type: ChangeType, sgn_text: str) -> None:
            # Get selected signage item
            get_selected = self._signage_list.selectedItems()
            if get_selected:
                item = get_selected[0]
                if change_type == ChangeType.SAVE:
                    # Update QTreeWidgetItem
                    item.setText(0, sgn_text)
        signage_widget = SignageWidget(self._sgn_mng, signage_change_handler)
        self._widget_idx['signage'] = self._stacked_widget.addWidget(signage_widget)
        frame_widget = FrameWidget(self._tpl_mng)
        self._widget_idx['frame'] = self._stacked_widget.addWidget(frame_widget)
        self._widget_idx['scene'] = self._stacked_widget.addWidget(SceneWidget())

        # Gather altogether
        hbox_outmost = QHBoxLayout()
        hbox_outmost.addLayout(vbox_left, 1)
        hbox_outmost.addWidget(self._stacked_widget, 5)

        self.setLayout(hbox_outmost)

    # Move given item up or down
    def _move_scene_item(self, selected_item: QTreeWidgetItem, direction: Direction) -> None:
        # UI Modification
        parent = selected_item.parent()  # Signage of selected scene
        sel_idx = int(selected_item.text(0).split(':')[0])

        if direction == Direction.DOWN:
            offset = +1
        elif direction == Direction.UP:
            offset = -1
        target_item = parent.child(sel_idx + offset)
        target_text = ':'.join(target_item.text(0).split(':')[1:])
        sel_text = ':'.join(selected_item.text(0).split(':')[1:])

        parent.child(sel_idx).setText(0, str(sel_idx + offset) + ':' + sel_text)
        parent.removeChild(parent.child(sel_idx + offset))
        moved_item = QTreeWidgetItem([str(sel_idx) + ':' + target_text])
        parent.insertChild(sel_idx, moved_item)
        self.update_ui_component()  # Update UI status

        # Data Modification
        sgn_id = Utils.ui_text_to_id(parent.text(0))
        signage = self._sgn_mng.get_signage(sgn_id)
        signage.rearrange_scene(sel_idx - 1, sel_idx - 1 + offset)  # Index starts from 0 here

    def move_button_clicked(self) -> None:
        button_text = self.sender().text()
        get_selected = self._signage_list.selectedItems()
        if get_selected:
            item = get_selected[0]
            if button_text == self._res['upButtonText']:
                # Up button clicked. Guaranteed it can be moved up
                self._move_scene_item(item, Direction.UP)
            elif button_text == self._res['downButtonText']:
                # Down button clicked. Guaranteed it can be moved down
                self._move_scene_item(item, Direction.DOWN)

    def update_ui_component(self) -> None:
        get_selected = self._signage_list.selectedItems()
        if get_selected:
            item = get_selected[0]
            item_text = item.text(0)
            if item.parent() is None:
                # Selected one is at topmost level
                # Signage cannot move up or down, so disable UP/DOWN button
                self._btn_up.setEnabled(False)
                self._btn_up.setEnabled(False)
                if item_text == "+":
                    pass  # TODO: Add signage addition logic
                else:
                    # Selected one is signage
                    sgn_id = Utils.ui_text_to_id(item_text)
                    idx = self._widget_idx['signage']
                    self._stacked_widget.widget(idx).load_data_on_ui(sgn_id)
                    self._stacked_widget.setCurrentIndex(idx)
            else:
                sgn_id = Utils.ui_text_to_id(item.parent().text(0))
                if item_text.startswith("F:"):
                    # Selected one is frame
                    # Frame cannot move up or down, so disable UP/DOWN button
                    self._btn_up.setEnabled(False)
                    self._btn_down.setEnabled(False)

                    frame_tpl_id = Utils.ui_text_to_id(item_text[2:])
                    idx = self._widget_idx['frame']
                    self._stacked_widget.widget(idx).load_data_on_ui(frame_tpl_id)
                    self._stacked_widget.setCurrentIndex(idx)
                elif item_text == '+':
                    # Add scene to signage
                    parent = item.parent()
                    signage = self._sgn_mng.get_signage(sgn_id)
                    new_scene = self._create_scene()
                    signage.add_scene(new_scene)

                    # Add scene to list on UI
                    # Make current item's text as added scene
                    num_child = parent.childCount()
                    scene_tpl = new_scene.template
                    scene_text = Utils.gen_ui_text(scene_tpl.definition.name, scene_tpl.id)
                    item.setText(0, str(num_child - 1) + ":" + scene_text)
                    parent.addChild(QTreeWidgetItem(['+']))

                    self.update_ui_component()  # Update UI status
                else:
                    # Selected one is scene
                    scene_idx = int(item_text.split(':')[0])
                    signage = self._sgn_mng.get_signage(sgn_id)
                    # First, scene can be moved
                    self._btn_up.setEnabled(True)
                    self._btn_down.setEnabled(True)
                    if scene_idx == 1:
                        # Scene at top. Cannot move up
                        self._btn_up.setEnabled(False)
                    if scene_idx == len(signage.scenes):
                        # Scene at bottom. Cannot move down
                        self._btn_down.setEnabled(False)
                    idx = self._widget_idx['scene']
                    self._stacked_widget.widget(idx).load_data_on_ui()
                    self._stacked_widget.setCurrentIndex(idx)

    def _create_scene(self) -> Scene:
        scene_tpls = list(self._tpl_mng.scene_templates.keys())
        initial_tpl_id = random.choice(scene_tpls)
        # Default template
        initial_tpl = self._tpl_mng.scene_templates[initial_tpl_id]

        # Default values
        obj_value = ObjectValue(None, initial_tpl.definition, self._obj_mng)

        return Scene(initial_tpl, obj_value)


class SignageWidget(QWidget):
    def __init__(self, sgn_mng: SignageManager, value_change_handler: Callable[[ChangeType, str], None]):
        super().__init__()

        self._value_change_handler = value_change_handler
        self._sgn_mng = sgn_mng

        self._ledit_id = QLineEdit()
        self._ledit_name = QLineEdit()
        self._ptedit_descript = QPlainTextEdit()

        self._sgn_id = None
        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, sgn_id: str) -> None:
        self._sgn_id = sgn_id
        signage = self._sgn_mng.get_signage(sgn_id)
        self._ledit_id.setText(sgn_id)
        self._ledit_name.setText(signage.title)
        self._ptedit_descript.setPlainText(signage.description)

    def init_ui(self) -> None:
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
        vbox_outmost.addLayout(hbox_id)
        vbox_outmost.addWidget(group_name)
        vbox_outmost.addWidget(group_descript)
        vbox_outmost.addStretch(1)
        vbox_outmost.addLayout(hbox_buttons)

        self.setLayout(vbox_outmost)

    def button_clicked(self) -> None:
        button_text = self.sender().text()
        if button_text == self._res['deleteButtonText']:
            # TODO: Delete selected signage
            self._value_change_handler(ChangeType.DELETE)
        elif button_text == self._res['saveButtonText']:
            # Save to signage
            signage = self._sgn_mng.get_signage(self._sgn_id)
            signage.id = self._ledit_id.text()
            signage.title = self._ledit_name.text()
            signage.description = self._ptedit_descript.toPlainText()

            # Update the signage id
            self._sgn_id = self._ledit_id.text()

            # Invoke value change handler to edit QTreeWidgetItem
            sgn_text = Utils.gen_ui_text(signage.title, self._sgn_id)
            self._value_change_handler(ChangeType.SAVE, sgn_text)
        elif button_text == self._res['cancelButtonText']:
            # Load the previous data
            self.load_data_on_ui(self._sgn_id)


class FrameWidget(QWidget):
    def __init__(self, tpl_mng: TemplateManager):
        super().__init__()

        self._tpl_mng = tpl_mng

        self._cbox_tpl = QComboBox()
        self._tab_data = FrameDataTab()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self, tpl_id: str) -> None:
        # Change combobox item to frame's template
        tpl = self._tpl_mng.frame_templates[tpl_id]
        idx = self._cbox_tpl.findText(Utils.gen_ui_text(tpl.definition.name, tpl.id))
        self._cbox_tpl.setCurrentIndex(idx)
        self._tab_data.load_data_on_ui()

    def init_ui(self) -> None:
        # Template list on combobox
        tpl_list = list()
        for tpl_id in self._tpl_mng.frame_templates:
            template = self._tpl_mng.frame_templates[tpl_id]
            tpl_list.append(Utils.gen_ui_text(template.definition.name, template.id))
        self._cbox_tpl.addItems(tpl_list)

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
        self.init_ui()

    def load_data_on_ui(self):
        pass  # TODO: Add functionality

    def init_ui(self):
        # TODO: This is dummy code. Have to edit it
        vbox = QVBoxLayout()
        self.setLayout(vbox)


class SceneWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._cbox_tpl = QComboBox()
        self._tab_data = SceneDataTab()
        self._tab_transition = SceneTransitionTab()
        self._tab_scheduling = SceneSchedulingTab()

        self._res = ResourceManager()
        self.init_ui()

    def load_data_on_ui(self):
        pass  # TODO: Add functionality

    def init_ui(self):
        # TODO: Read template list and add it by cbox.addItems(list)
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

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        pass  # TODO: Add functionality


class SceneTransitionTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        pass  # TODO: Add functionality


class SceneSchedulingTab(QWidget):
    def __init__(self):
        super().__init__()

        self._res = ResourceManager()
        self.init_ui()

    def init_ui(self):
        pass  # TODO: Add functionality
