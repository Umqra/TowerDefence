import re
from Model.store import Store

__author__ = 'umqra'

import logging
from Model.time import Time

logger = logging.getLogger(__name__)


class LevelFormatError(Exception):
    pass


class GameState:
    def __init__(self):
        self.map = None
        self.views = []
        self.waves = []
        self.time = Time()
        self.store = Store()
        self.money = 0
        self.controller = None

    def get_normal_light(self):
        max_value = Time.hours * Time.minutes * Time.seconds / 2
        mid_value = max_value
        return 255 - abs(mid_value - self.time.value) / max_value * 255

    def tick(self, dt):
        if self.waves:
            self.waves[0].tick(dt)
            if self.waves[0].empty():
                self.waves = self.waves[1:]
        self.map.tick(dt)
        self.time.tick(dt)

    def add_view(self, view):
        self.views.append(view)

    def initialize_with_loader(self, loader):
        loader.init_game(self)

    def set_controller(self, controller):
        self.map.set_controller(controller)
        self.store.set_controller(controller)
        self.controller = controller

    def buy_item(self, item, store_info):
        if self.money < store_info.cost:
            return False
        if not self.map.can_put_item(item):
            return False
        self.money -= store_info.cost
        self.map.add_item(item)
        return True