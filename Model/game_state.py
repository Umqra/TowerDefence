import re
from Model.store import Store

__author__ = 'umqra'

import logging
from Model.time import Time

logger = logging.getLogger(__name__)


class NotificationEvent:
    def __init__(self, predicat, notification):
        self.predicat = predicat
        self.notification = notification

    def can_run(self):
        return self.predicat()


class NotificationCreator:
    def __init__(self, state):
        self.state = state
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def tick(self, dt):
        for event in self.events:
            if event.can_run():
                self.state.push_notification(event.notification)
                continue


class LevelFormatError(Exception):
    pass


class GameState:
    def __init__(self, game):
        self.game = game

        self.map = None
        self.views = []
        self.waves = []
        self.time = Time()
        self.store = Store()
        self.money = 0
        self.controller = None
        self.notification = "New game starts!"
        self.notification_creator = None
        self.pause = False

    def restart(self):
        self.game.load_level(self.loader)

    def push_notification(self, text):
        self.notification = text
        for view in self.views:
            view.update()

    def get_normal_light(self):
        max_value = Time.max_total_seconds() / 2
        mid_value = max_value
        return 255 - abs(mid_value - self.time.value) / max_value * 255

    def tick(self, dt):
        if self.pause:
            return
        if self.waves:
            self.waves[0].tick(dt)
            if self.waves[0].empty():
                self.waves = self.waves[1:]
        self.map.tick(dt)
        self.time.tick(dt)
        if self.notification_creator:
            self.notification_creator.tick(dt)

    def add_view(self, view):
        self.views.append(view)

    def initialize_with_loader(self, loader):
        self.loader = loader
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