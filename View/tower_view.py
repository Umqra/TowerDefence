__author__ = 'umqra'

from Model.towers import EnergyTower
from PyQt4.QtGui import QWidget, QPainter, QPixmap, QImage


def get_tower_view(tower):
    if isinstance(tower, EnergyTower):
        return EnergyTowerView(tower)
    return TowerView(tower)


class TowerView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def paintEvent(self, QPaintEvent):
        pass


class EnergyTowerView(TowerView):
    image = QImage('Resources/Images/tower.png').scaledToWidth(50)  # TODO: replace number to constant

    def __init__(self, model):
        super().__init__(model)
        self.pixmap = QPixmap(EnergyTowerView.image)
        self.height_pixmap = self.pixmap.height()

    def paintEvent(self, QPaintEvent):
        if not self.model.is_alive:
            self.close()
        qp = QPainter()
        qp.begin(self)
        bbox = self.model.shape.get_bounding_box()
        qp.drawPixmap(bbox[0].x - 10, bbox[0].y - 33, self.pixmap)
