from PyQt4.QtCore import Qt
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QGridLayout, QPainter, QPixmap, QPushButton, QLabel, QScrollArea, QHBoxLayout
from Model.bullets import Bullet
from Model.towers import Tower, EnergyTower, LightTower, JustTower, Fortress
from Model.wave import Gate
from View.bullet_view import get_bullet_view
from View.custom_label import CustomLabel
from View.gate_view import GateView
from View.tower_view import get_tower_view, EnergyTowerView, LightTowerView, JustTowerView, FortressView

from Controller.controller_events import StoreControllerEvent

__author__ = 'umqra'

view_by_model = {
    EnergyTower: EnergyTowerView,
    LightTower: LightTowerView,
    JustTower: JustTowerView,
    Gate: GateView,
    Fortress: FortressView,
}


def get_view_class_by_model(item_type):
    return view_by_model[item_type]


class StoreItemView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.view = get_view_class_by_model(self.model.item_type)
        self.layout = QGridLayout()
        self.layout.setVerticalSpacing(2)

        title = CustomLabel(model.title)

        preview = QLabel()
        preview.setFixedHeight(self.view.image.height())
        preview.setFixedWidth(self.view.image.width())
        preview.setPixmap(QPixmap(self.view.image))

        cost = CustomLabel("{}$".format(model.cost))

        self.layout.addWidget(title, 0, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(preview, 1, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(cost, 2, 0, QtCore.Qt.AlignCenter)
        self.setToolTip(model.description)
        self.setLayout(self.layout)

    def mousePressEvent(self, e):
        self.model.controller.handle_event(StoreControllerEvent(e, self.model.item_type, self.model))


class StoreView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setFixedWidth(500)

        container = QWidget()

        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(0)
        for index, item in enumerate(self.model.items):
            self.layout.addWidget(StoreItemView(item), 0, index)
        self.layout.setRowStretch(1, 1)
        container.setLayout(self.layout)

        self.scroller = QScrollArea()
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(False)
        self.scroller.setWidget(container)

        hLayout = QHBoxLayout(self)
        hLayout.addWidget(self.scroller)
        self.setLayout(hLayout)