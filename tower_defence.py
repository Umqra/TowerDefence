from datetime import datetime
from PyQt4.QtGui import QColor
import math
from Geometry.line import Line
from Geometry.point import Point
from Geometry.polygon import Polygon
from Geometry.segment import Segment
from Model.game_map import GameMap
from Model.light import LightImpulse

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
    fps = 20
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.map = GameMap(10, 10, MockState())
        self.map.initialize_from_file('map1.txt')
        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapTest.interval, self)

    def timerEvent(self, e):
        self.map.tick(MapTest.interval / 1000)
        self.repaint()

    def mousePressEvent(self, e):
        size = 30
        x = e.x() // size
        y = e.y() // size
        print('press', x, y)
        print(self.map.map[x][y].lighting.light_impulse.value)
        self.map.map[x][y].lighting.add_impulse(LightImpulse(500))
        print(self.map.map[x][y].lighting.light_impulse.value)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        size = 30
        for x in range(self.map.height):
            for y in range(self.map.width):
                value = int(self.map.map[x][y].lighting.value)

                qp.fillRect(x * size, y * size, size, size, QColor.fromRgb(value, value, value))
                qp.drawRect(x * size, y * size, size, size)


def main():
    args = parse_arguments()
    A = Point(1, 0)
    B = Point(4, 3)
    C = Point(5, 6)
    D = Point(-1, 100)
    p = Polygon([A, B, C, D])
    print(p)
    p.rotate_around_origin(math.pi / 2)
    print(p)
    return

    app = QtGui.QApplication(sys.argv)
    widget = MapTest()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()