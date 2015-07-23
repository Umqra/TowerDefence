from Controller.main_controller import MainController
from Model.game_map import GameMap
from Model.store import StoreItem, Store
from Model.time import Time
from Model.towers import EnergyTower, LightTower, SimpleChooser, simple_chooser
import Model

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

        Model.towers.simple_chooser = SimpleChooser(game_state.map)

        game_state.store = Store([
            StoreItem("Башенка", EnergyTower, 50,
                      "Башенка - удивительное оружие света, которое защитит вас от любого типа монстров"),
            StoreItem("Светилышко", LightTower, 100,
                      "Светилышко - это чудо! Не упускай момента чтобы купить 'Светилышко'!"),
        ])
        controller = MainController(game_state)
        game_state.set_controller(controller)