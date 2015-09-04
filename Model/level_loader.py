from Controller.main_controller import MainController
from Geometry.point import Point
from Model.game_map import GameMap
from Model.store import StoreItem, Store
from Model.time import Time
from Model.towers import EnergyTower, LightTower, SimpleChooser, simple_chooser, JustTower, Fortress
import Model
from Model.warriors import BFSWalker, SimpleWarrior

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
        fortress_position = game_state.map.get_cell_shape(game_state.map.height - 1,
                                                          0).get_center_of_mass()
        fortress = Fortress()
        fortress.move_to(fortress_position + Point(0, -10))
        game_state.map.add_tower(fortress)

        Model.warriors.random_walker = BFSWalker(game_state.map)
        Model.towers.simple_chooser = SimpleChooser(game_state.map)

        # game_state.map.add_warrior(SimpleWarrior(Point(380, 80)))
        game_state.map.add_warrior(SimpleWarrior(Point(400, 100)))
        # game_state.map.add_warrior(SimpleWarrior(Point(420, 120)))

        game_state.store = Store([
            StoreItem("Башенка", EnergyTower, 50,
                      "Башенка - удивительное оружие света, которое защитит вас от любого типа монстров"),
            StoreItem("Светилышко", LightTower, 100,
                      "Светилышко - это чудо! Не упускай момента чтобы купить 'Светилышко'!"),
            StoreItem("Просто башня", JustTower, 10,
                      "Ты нищеброд и у тебя не хватает денег даже на Башенку?! Бери 'Просто башню'! Пусть постоит")
        ])
        controller = MainController(game_state)
        game_state.set_controller(controller)