from enum import Enum
import re
from Controller.creator_controller import CreatorController
from Geometry.point import Point
from Model import level_loader
from Model.game_map import GameMap
from Model.game_result import GameResult
from Model.store import Store, StoreItem
from Model.towers import EnergyTower, JustTower, Fortress
from Model.towers import LightTower
from Model.warriors import SimpleWarrior, AdamantWarrior
from Model.wave import Gate, Wave

__author__ = 'umqra'

import logging
from Model.time import Time

logger = logging.getLogger(__name__)

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

    def stop(self):
        self.pause = True

    def resume(self):
        self.pause = False

    def restart(self):
        self.game.load_level(self.loader)

    def next_level(self):
        current_level_id = self.loader.level_id
        next_level_id = None
        if current_level_id in level_loader.bonus_levels.keys():
            rule = level_loader.bonus_rules[current_level_id]
            if rule(self):
                next_level_id = level_loader.bonus_levels[current_level_id]
        else:
            try:
                next_level_id = level_loader.next_level[self.loader.level_id]
            except:
                return
        if next_level_id is None:
            return
        new_level_loader = list(filter(lambda x: x.level_id == next_level_id, level_loader.levels))[0]
        self.game.load_level(new_level_loader)

    def push_notification(self, text):
        self.notification = text
        for view in self.views:
            view.update()

    @property
    def game_result(self):
        if self.map.fortress_health == 0:
            return GameResult.Lose
        if not self.map.warriors and not self.waves:
            return GameResult.Win
        if self.pause:
            return GameResult.Pause
        return GameResult.Running

    def get_normal_light(self):
        max_value = Time.max_total_seconds() / 2
        mid_value = max_value
        return 255 - abs(mid_value - self.time.value) / max_value * 255

    def tick(self, dt):
        if self.game_result != GameResult.Running:
            self.pause = True
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
        self.notification = loader.level_id
        loader.init_game(self)

    def set_controller(self, controller):
        self.map.set_controller(controller)
        self.store.set_controller(controller)
        self.controller = controller

    def try_buy_item(self, item, store_info):
        if self.money < store_info.cost:
            return False
        if not self.map.can_put_item(item):
            return False
        self.money -= store_info.cost
        self.map.add_item(item)
        return True

    def initialize_empty_level(self):
        self.time = Time.fromDHMS(0, 12, 0, 0)
        self.map = GameMap(10, 10, self)
        self.map.initialize_empty_map()

        self.store = Store([
            StoreItem("Башенка", EnergyTower, 0,
                      "Башенка - удивительное оружие света, которое защитит вас от любого типа монстров"),
            StoreItem("Светилышко", LightTower, 0,
                      "Светилышко - это чудо! Не упускай момента чтобы купить 'Светилышко'!"),
            StoreItem("Просто башня", JustTower, 0,
                      "Ты нищеброд и у тебя не хватает денег даже на Башенку?! Бери 'Просто башню'! Пусть постоит"),
            StoreItem("Врата ада", Gate, 0,
                      "Из этих ворот вылезают создания тьмы"),
            StoreItem("Замок света", Fortress, 0,
                      "Защити башню света - спаси мир от беспроглядной тьмы!")
        ])

    def __getstate__(self):
        state = self.__dict__.copy()
        state['views'] = []
        state['game'] = None
        state['controller'] = None
        state['pause'] = False
        state['store'] = None
        return state
