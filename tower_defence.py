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


def clear_layout(layout):
    if layout != None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clear_layout(child.layout())


class Game(QtGui.QWidget):
    fps = 40
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 800)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.state = None
        self.state_view = None
        self.load_level(Level1)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(Game.interval, self)


    def load_level(self, level_loader):
        self.reset_game()
        self.state = GameState(self)
        self.state.initialize_with_loader(level_loader)
        self.state_view = StateView(self.state)
        self.layout.addWidget(self.state_view)

        self.setMouseTracking(True)

    def reset_game(self):
        clear_layout(self.layout)

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
        if self.state.pause:
            return
        self.state.tick(Game.interval / 1000)
        self.repaint()


def main():
    app = QtGui.QApplication(sys.argv)
    widget = Game()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()