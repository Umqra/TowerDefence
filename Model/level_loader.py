from Model.game_map import GameMap
from Model.store import StoreItem
from Model.time import Time
from Model.towers import EnergyTower

__author__ = 'umqra'


class LevelLoader:
    pass


class Level1(LevelLoader):
    @staticmethod
    def init_game(game_state):
        game_state.money = 100
        game_state.time = Time.fromHMS(12, 0, 0)
        game_state.map = GameMap(10, 10, game_state)
        game_state.map.initialize_from_file('map1.txt')
        game_state.store.add_items([
            StoreItem("Башенка", EnergyTower, 50,
                      "Башенка - удивительное оружие света,\n которое защитит вас от любого типа монстров"),
        ])