from PyQt4.QtGui import QWidget, QGridLayout
from View.custom_label import CustomLabel
from View.info_panel_view import InfoPanelView
from View.map_view import MapView
from View.store_view import StoreView

__author__ = 'umqra'


class StateView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.views.append(self)

        self.layout = QGridLayout()
        self.notifications_view = CustomLabel(self.model.notification)
        self.layout.addWidget(self.notifications_view, 0, 0)
        self.layout.addWidget(MapView(self.model.map), 1, 0)
        self.layout.addWidget(StoreView(self.model.store), 2, 0)
        self.layout.addWidget(InfoPanelView(self.model), 1, 1)
        self.setLayout(self.layout)

    def update(self):
        self.notifications_view.setText(self.model.notification)