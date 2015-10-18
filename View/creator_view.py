from PyQt4.QtGui import QWidget, QGridLayout
from Model.map_cell import all_cells
from View.control_panel_view import ControlPanelView
from View.custom_label import CustomLabel
from View.info_panel_view import InfoPanelView
from View.landscape_editor import LandscapeEditorView
from View.map_creator_view import MapCreatorView
from View.map_view import MapView
from View.store_view import StoreView

__author__ = 'umqra'


class CreatorView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.views.append(self)

        self.layout = QGridLayout()

        #self.layout.addWidget(CreatorControlPanelView(self.model), 1, 0)
        self.layout.addWidget(MapCreatorView(self.model.map), 1, 1)
        self.layout.addWidget(LandscapeEditorView(self.model.map, all_cells), 2, 1)
        #self.layout.addWidget(StoreView(self.model.store), 2, 1)
        #self.layout.addWidget(CreatorInfoPanel(self.model), 1, 2)
        self.layout.setColumnStretch(2, 3)
        self.layout.setColumnStretch(0, 2)
        self.setLayout(self.layout)
