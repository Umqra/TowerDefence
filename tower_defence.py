from datetime import datetime
from PyQt4.QtGui import QColor, QPixmap, QImage, QGridLayout
from PyQt4.QtCore import QPointF
import math
from Geometry.line import Line
from Geometry.point import Point
from Geometry.polygon import Polygon
from Geometry.segment import Segment
from Model.game_fraction import GameFraction
from Model.game_map import GameMap
from Model.game_state import GameState
from Model.level_loader import Level1
from Model.light import LightImpulse
from Model.towers import EnergyTower, SimpleChooser
from View.bullet_view import EnergyBulletView
from View.loader_widget import LoaderWidget
from View.map_view import MapView
from View.state_view import StateView
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


class MapTest(QtGui.QWidget):
    fps = 40
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 800)
        state = GameState()

        state.initialize_with_loader(Level1)

        self.state = state

        self.layout = QGridLayout()
        self.layout.addWidget(StateView(state))

        self.setLayout(self.layout)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapTest.interval, self)

        self.setMouseTracking(True)

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QtCore.QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)
        QtGui.QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def timerEvent(self, e):
        self.state.tick(MapTest.interval / 1000)
        self.repaint()


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MapTest()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()