from PyQt4.QtGui import QWidget, QGridLayout, QLineEdit
import datetime
import jsonpickle
import pickle

from Model.map_cell import all_cells
from View.creator_control_panel_view import CreatorControlPanelView
from PyQtExtension.custom_button import CustomButton
from View.landscape_editor import LandscapeEditorView
from View.map_creator_view import MapCreatorView
from View.store_view import StoreView


__author__ = 'umqra'


class CreatorControlButtons(QWidget):
    def __init__(self, creator):
        super().__init__()
        self.creator = creator

        self.switch_store_button = CustomButton("Store")
        self.switch_store_button.clicked.connect(self.switch_store)

        self.level_name = QLineEdit()
        self.level_name.setPlaceholderText("Input level name...")
        self.save_button = CustomButton("Save")
        self.save_button.clicked.connect(self.save_level)

        self.layout = QGridLayout()
        self.layout.addWidget(self.switch_store_button, 1, 0)
        self.layout.setRowMinimumHeight(2, 40)
        self.layout.addWidget(self.level_name, 3, 0)
        self.layout.addWidget(self.save_button, 4, 0)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(10, 1)
        self.setLayout(self.layout)

    def switch_store(self):
        if self.switch_store_button.text() == "Store":
            self.switch_store_button.setText("Landscape")
            self.creator.set_store_view()
        else:
            self.switch_store_button.setText("Store")
            self.creator.set_landscape_view()

    def save_level(self):
        filename = self.level_name.text()
        if filename == "":
            return
        self.creator.save_level(filename + ".tdl")


class CreatorView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.views.append(self)

        self.layout = QGridLayout()

        self.layout.addWidget(CreatorControlPanelView(self.model), 1, 2)
        self.layout.addWidget(MapCreatorView(self.model.map), 1, 1)

        self.layout.addWidget(CreatorControlButtons(self), 1, 0)

        self.current_store = LandscapeEditorView(self.model.map, all_cells)
        self.layout.addWidget(self.current_store, 2, 1)
        self.layout.setColumnStretch(2, 3)
        self.layout.setColumnStretch(0, 2)
        self.layout.setRowStretch(3, 1)
        self.setLayout(self.layout)

    def set_store_view(self):
        self.current_store.close()
        self.current_store = StoreView(self.model.store)
        self.layout.addWidget(self.current_store, 2, 1)

    def set_landscape_view(self):
        self.current_store.close()
        self.current_store = LandscapeEditorView(self.model.map, all_cells)
        self.layout.addWidget(self.current_store, 2, 1)

    def save_level(self, filename):
        with open(filename, 'wb') as f:
            f.write(pickle.dumps(self.model))