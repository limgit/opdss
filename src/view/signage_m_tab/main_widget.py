from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem,
                             QStackedWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton)
from enum import Enum, auto
import random

import utils.utils as Utils
from .signage_widget import SignageWidget
from .frame_widget import FrameWidget
from .scene_widget import SceneWidget
from controller.manager import ObjectManager, TemplateManager, SignageManager
from model.data_value import ObjectValue
from model.signage import Scene
from view.resource_manager import ResourceManager


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
        def signage_change_handler(change_type: Utils.ChangeType, sgn_text: str) -> None:
            # Get selected signage item
            get_selected = self._signage_list.selectedItems()
            if get_selected:
                item = get_selected[0]
                if change_type == Utils.ChangeType.SAVE:
                    # Update QTreeWidgetItem
                    item.setText(0, sgn_text)
        signage_widget = SignageWidget(self._sgn_mng, signage_change_handler)
        self._widget_idx['signage'] = self._stacked_widget.addWidget(signage_widget)
        frame_widget = FrameWidget(self._sgn_mng, self._tpl_mng)
        self._widget_idx['frame'] = self._stacked_widget.addWidget(frame_widget)
        scene_widget = SceneWidget(self._sgn_mng, self._tpl_mng)
        self._widget_idx['scene'] = self._stacked_widget.addWidget(scene_widget)

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

        # Data Modification
        sgn_id = Utils.ui_text_to_id(parent.text(0))
        signage = self._sgn_mng.get_signage(sgn_id)
        signage.rearrange_scene(sel_idx - 1, sel_idx - 1 + offset)  # Index starts from 0 here

        # Update UI status
        self.update_ui_component()

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

                    idx = self._widget_idx['frame']
                    self._stacked_widget.widget(idx).load_data_on_ui(sgn_id)
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
                    self._stacked_widget.widget(idx).load_data_on_ui(sgn_id, scene_idx - 1)
                    self._stacked_widget.setCurrentIndex(idx)

    def _create_scene(self) -> Scene:
        scene_tpls = list(self._tpl_mng.scene_templates.keys())
        initial_tpl_id = random.choice(scene_tpls)
        # Default template
        initial_tpl = self._tpl_mng.scene_templates[initial_tpl_id]

        # Default values
        obj_value = ObjectValue(None, initial_tpl.definition, self._obj_mng)

        return Scene(initial_tpl, obj_value)
