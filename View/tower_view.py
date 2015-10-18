from Infrastructure.get_resources import get_default_image, load_image
from View.loader_widget import LoaderWidget, LoaderType
from View.static_view import StaticObjectView

__author__ = 'umqra'

from Model.towers import EnergyTower, LightTower, JustTower, Fortress
from PyQt4.QtGui import QWidget, QPainter, QPixmap, QImage, QColor, QGridLayout, QLabel
from PyQt4.QtCore import Qt


def get_tower_view(tower):
    if isinstance(tower, EnergyTower):
        return EnergyTowerView(tower)
    elif isinstance(tower, LightTower):
        return LightTowerView(tower)
    elif isinstance(tower, JustTower):
        return JustTowerView(tower)
    elif isinstance(tower, Fortress):
        return FortressView(tower)
    return TowerView(tower)


class TowerView(StaticObjectView):
    def __init__(self, model):
        super().__init__(model)
        self.model = model


class EnergyTowerView(TowerView):
    image = load_image("energy_tower.png", 50)

    def __init__(self, model):
        super().__init__(model)
        self.pixmap = QPixmap(EnergyTowerView.image)
        self.height_pixmap = self.pixmap.height()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

    def mousePressEvent(self, QMouseEvent):
        print("Press {}".format(self))


class LightTowerView(TowerView):
    image = load_image("light_tower.png", 50)

    def __init__(self, model):
        super().__init__(model)
        self.pixmap = QPixmap(LightTowerView.image)
        self.height_pixmap = self.pixmap.height()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

    def mousePressEvent(self, QMouseEvent):
        print("Press {}".format(self))


class JustTowerView(TowerView):
    image = load_image("just_tower.png", 50)

    def __init__(self, model):
        super().__init__(model)
        self.pixmap = QPixmap(JustTowerView.image)
        self.height_pixmap = self.pixmap.height()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

    def mousePressEvent(self, QMouseEvent):
        print("Press {}".format(self))


class FortressView(TowerView):
    image = load_image("fortress.png", 50)

    def __init__(self, model):
        super().__init__(model)
        self.pixmap = QPixmap(FortressView.image)
        self.height_pixmap = self.pixmap.height()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

    def mousePressEvent(self, QMouseEvent):
        print("Press {}".format(self))