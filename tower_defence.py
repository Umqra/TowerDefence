from datetime import datetime
from PyQt4.QtGui import QColor, QPixmap, QImage, QGridLayout
from PyQt4.QtCore import QPointF
import math
from Controller.map_controller import MapController
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
from View.map_view import MapView
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
        return 255


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
        self.map.add_tower(t1)
        self.map.add_tower(t2)
        self.map.add_tower(t3)
        self.layout.addWidget(MapView(self.map, MapController(self.map)))
        self.setLayout(self.layout)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapTest.interval, self)

    def timerEvent(self, e):
        self.map.tick(MapTest.interval / 1000)
        self.repaint()

    def mousePressEvent(self, e):
        self.map.add_impulse_at_position(e.x(), e.y())


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MapTest()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()