from PyQt4.QtGui import QWidget, QPainter, QImage, QPixmap
from PyQt4 import QtGui
import math

__author__ = 'umqra'

from Model.bullets import EnergyBullet


def get_bullet_view(bullet):
    if isinstance(bullet, EnergyBullet):
        return EnergyBulletView(bullet)
    return BulletView(bullet)


class BulletView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.state = 0

    def paintEvent(self, QPaintEvent):
        pass


class EnergyBulletView(BulletView):
    images = [
        QImage('Resources/Images/energy_bullet_0').scaledToWidth(25),
        QImage('Resources/Images/energy_bullet_0').scaledToWidth(25),
        QImage('Resources/Images/energy_bullet_1').scaledToWidth(25),
        QImage('Resources/Images/energy_bullet_1').scaledToWidth(25),
        QImage('Resources/Images/energy_bullet_2').scaledToWidth(25),
        QImage('Resources/Images/energy_bullet_2').scaledToWidth(25),
    ]

    count_states = 6

    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        if not self.model.is_alive:
            self.close()
        qp = QPainter()
        qp.begin(self)
        direction = self.model.direction
        angle_in_rad = direction.angle
        pixmap = QPixmap(
            EnergyBulletView.images[self.state].transformed(QtGui.QTransform().rotateRadians(angle_in_rad)))
        bbox = self.model.shape.get_bounding_box()
        qp.drawPixmap(bbox[0].x, bbox[0].y, pixmap)
        self.state = (self.state + 1) % EnergyBulletView.count_states