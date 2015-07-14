from datetime import datetime
from PyQt4.QtGui import QColor, QPixmap, QImage, QGridLayout
from PyQt4.QtCore import QPointF
import math
from Geometry.line import Line
from Geometry.point import Point
from Geometry.polygon import Polygon
from Geometry.segment import Segment
from Model.bullets import Bullet, EnergyBullet
from Model.game_fraction import GameFraction
from Model.game_map import GameMap
from Model.light import LightImpulse
from Model.towers import EnergyTower, SimpleChooser
from View.bullet_view import EnergyBulletView
from View.tower_view import EnergyTowerView

__author__ = 'umqra'

import sys
import argparse
from PyQt4 import QtGui, QtCore

import logging
import logging.config

logging.config.fileConfig('logging.conf')


def parse_arguments():
    parser = argparse.ArgumentParser(description="Tower defence game")
    parser.add_argument("-c", "--console", help="Turn on console mode", action="store_true")
    return parser.parse_args()


class MockState:
    def __init__(self):
        self.start_time = datetime.now()

    def get_normal_light(self):
        delta = datetime.now() - self.start_time
        return (delta.seconds % 51) * 5 + 1


class MapTest(QtGui.QWidget):
    fps = 40
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.map = GameMap(10, 10, MockState())
        self.map.initialize_from_file('map1.txt')

        chooser = SimpleChooser(self.map)
        t1 = EnergyTower(Polygon([Point(50, 50), Point(100, 50), Point(100, 100), Point(50, 100)]), chooser,
                         GameFraction.Light)
        t2 = EnergyTower(Polygon([Point(200, 200), Point(250, 200), Point(250, 250), Point(200, 250)]), chooser,
                         GameFraction.Dark)
        t3 = EnergyTower(Polygon([Point(350, 50), Point(400, 50), Point(400, 100), Point(350, 50)]), chooser,
                         GameFraction.Dark)
        self.layout = QGridLayout()
        v1 = EnergyTowerView(t1)
        v2 = EnergyTowerView(t2)
        v3 = EnergyTowerView(t3)
        self.layout.addWidget(v1, 0, 0)
        self.layout.addWidget(v2, 0, 0)
        self.layout.addWidget(v3, 0, 0)
        self.map.add_tower(t1)
        self.map.add_tower(t2)
        self.map.add_tower(t3)
        self.setLayout(self.layout)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapTest.interval, self)

        self.tower_image = QPixmap(QImage('Resources/Images/tower.png').scaledToWidth(50))

    def timerEvent(self, e):

        self.map.tick(MapTest.interval / 1000)
        self.repaint()

    def mousePressEvent(self, e):
        size = 50
        x = e.x() // size
        y = e.y() // size
        self.map.map[x][y].lighting.add_impulse(LightImpulse(500))

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        size = 50
        for x in range(self.map.height):
            for y in range(self.map.width):
                value = int(self.map.map[x][y].lighting.value)
                qp.fillRect(x * size, y * size, size, size, QColor.fromRgb(value, value, value))
                qp.drawRect(x * size, y * size, size, size)

        for bullet in self.map.bullets:
            if not hasattr(bullet, 'test'):
                bullet.test = 1
                b_cur = EnergyBulletView(bullet)
                self.layout.addWidget(b_cur, 0, 0)

def main():
    app = QtGui.QApplication(sys.argv)
    widget = MapTest()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()