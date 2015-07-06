from PyQt4.QtGui import QColor
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
        pass

    def get_normal_light(self):
        return 30


class MapTest(QtGui.QWidget):
    fps = 20
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 600)
        self.map = GameMap(30, 30, MockState())
        self.map.initialize_from_file('map2.txt')
        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapTest.interval, self)

    def timerEvent(self, e):
        logging.debug('Start tick!')
        for x in range(self.map.height):
            logging.debug(' '.join([str(y.lighting.value) for y in self.map.map[x]]))

        for x in range(self.map.height):
            for y in range(self.map.width):
                self.map.map[x][y].start_tick()
        for x in range(self.map.height):
            for y in range(self.map.width):
                self.map.map[x][y].tick(MapTest.interval / 1000)
        for x in range(self.map.height):
            for y in range(self.map.width):
                self.map.map[x][y].end_tick()
        self.repaint()

    def mousePressEvent(self, e):
        size = 15
        x = e.x() // size
        y = e.y() // size
        print('press', x, y)
        print(self.map.map[x][y].lighting.light_impulse.value)
        self.map.map[x][y].lighting.add_impulse(LightImpulse(500))
        print(self.map.map[x][y].lighting.light_impulse.value)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        size = 15
        for x in range(self.map.height):
            for y in range(self.map.width):
                value = int(self.map.map[x][y].lighting.value)
                qp.fillRect(x * size, y * size, size, size, QColor.fromRgb(value, value, value))
                qp.drawRect(x * size, y * size, size, size)


def main():
    args = parse_arguments()

    app = QtGui.QApplication(sys.argv)
    widget = MapTest()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()