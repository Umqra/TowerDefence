from datetime import datetime
from PyQt4.QtGui import QColor, QPixmap, QImage, QGridLayout, QApplication
from PyQt4.QtCore import QPointF
import math
from Geometry.line import Line
from Geometry.point import Point
from Geometry.polygon import Polygon
from Geometry.segment import Segment
from Gui import gui_tower_defence
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


def main():
    gui_tower_defence.run()

if __name__ == "__main__":
    main()