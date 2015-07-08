__author__ = 'umqra'

import logging

logger = logging.getLogger(__name__)


class LevelFormatError(Exception):
    pass

class Time:
    pass

class GameState:
    def __init__(self, time=Time()):
        self.map = None
        self.views = []
        self.time = time

    def tick(self, dt):
        self.map.tick(dt)

    def add_view(self, view):
        self.views.append(view)

    def initialize_from_file(self, filename):
        pass