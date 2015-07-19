from PyQt4.QtGui import QWidget, QGridLayout
from View.map_view import MapView
from View.store_view import StoreView

__author__ = 'umqra'


class StateView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout = QGridLayout()
        self.layout.addWidget(MapView(self.model.map), 0, 0)
        self.layout.addWidget(StoreView(self.model.store), 1, 0)
        self.setLayout(self.layout)