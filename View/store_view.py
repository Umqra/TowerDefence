from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QGridLayout, QPainter, QPixmap, QPushButton, QLabel
from Model.bullets import Bullet
from Model.towers import Tower, EnergyTower
from View.bullet_view import get_bullet_view
from View.tower_view import get_tower_view, EnergyTowerView

__author__ = 'umqra'

view_by_model = {
    EnergyTower: EnergyTowerView,
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

        title = QLabel(model.title)

        preview = QLabel()
        preview.setFixedHeight(self.view.image.height())
        preview.setFixedWidth(self.view.image.width())
        preview.setPixmap(QPixmap(self.view.image))

        cost = QLabel("{}$".format(model.cost))

        self.layout.addWidget(title, 0, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(preview, 1, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(cost, 2, 0, QtCore.Qt.AlignCenter)
        self.setToolTip(model.description)
        self.setLayout(self.layout)


class StoreView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(0)
        for index, item in enumerate(self.model.items):
            self.layout.addWidget(StoreItemView(item), 0, index)
        self.layout.setRowStretch(1, 1)
        self.setLayout(self.layout)