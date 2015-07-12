from datetime import datetime
from PyQt4.QtGui import QColor
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
        return 51 * 5 - (delta.seconds % 51) * 5 + 1


class MapTest(QtGui.QWidget):
    fps = 20
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.map = GameMap(10, 10, MockState())
        self.map.initialize_from_file('map1.txt')

        chooser = SimpleChooser(self.map)
        t1 = EnergyTower(Polygon([Point(45, 15), Point(55, 45), Point(55, 55), Point(45, 55)]), chooser,
                         GameFraction.Light)
        t2 = EnergyTower(Polygon([Point(205, 205), Point(215, 205), Point(215, 215), Point(205, 215)]), chooser,
                         GameFraction.Dark)
        t3 = EnergyTower(Polygon([Point(305, 55), Point(315, 55), Point(315, 65), Point(305, 65)]), chooser,
                         GameFraction.Dark)
        self.map.add_tower(t1)
        self.map.add_tower(t2)
        self.map.add_tower(t3)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapTest.interval, self)

    def timerEvent(self, e):
        self.map.tick(MapTest.interval / 1000)
        self.repaint()

    def mousePressEvent(self, e):
        size = 30
        x = e.x() // size
        y = e.y() // size
        self.map.map[x][y].lighting.add_impulse(LightImpulse(500))

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        size = 30
        for x in range(self.map.height):
            for y in range(self.map.width):
                value = int(self.map.map[x][y].lighting.value)
                qp.fillRect(x * size, y * size, size, size, QColor.fromRgb(value, value, value))
                qp.drawRect(x * size, y * size, size, size)

        for bullet in self.map.bullets:
            bullet_size = 10
            qpts = []
            for p in bullet.shape.shape:
                qpts.append(QPointF(p.x, p.y))
            qp.drawPolygon(*qpts)
        for tower in self.map.towers:
            p = tower.shape.get_center_of_mass()
            qp.drawText(QPointF(p.x, p.y), "Tower {}".format(tower.health))


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MapTest()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()