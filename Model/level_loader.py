from Controller.main_controller import MainController
from Geometry.point import Point
from Model.game_map import GameMap
from Model.game_result import GameResult
from Model.level_notifications import NotificationCreator
from Model.level_notifications import NotificationEvent
from Model.store import StoreItem, Store
from Model.time import Time
from Model.towers import EnergyTower, LightTower, SimpleChooser, JustTower, Fortress
import Model
from Model.warriors import BFSWalker, SimpleWarrior, AdamantWarrior
from Model.wave import Wave, Gate

__author__ = 'umqra'


class LevelLoader:
    pass


class Level1(LevelLoader):
    level_id = 0

    @staticmethod
    def init_game(game_state):
        game_state.money = 300
        game_state.time = Time.fromHMS(12, 0, 0)

        game_state.map = GameMap(10, 10, game_state)

        game_state.map.initialize_from_file('map1.txt')

        Model.warriors.random_walker = BFSWalker(game_state.map)
        g1 = Gate(game_state.map, Point(400, 100))
        g2 = Gate(game_state.map, Point(300, 100))
        g3 = Gate(game_state.map, Point(350, 60))
        game_state.map.add_gate(g1)
        game_state.map.add_gate(g2)
        game_state.map.add_gate(g3)
        game_state.waves.append(Wave(
            game_state, Time.fromDHMS(0, 14, 0, 0),
            [SimpleWarrior, SimpleWarrior, SimpleWarrior, SimpleWarrior, SimpleWarrior],
            [g1, g2, g3]
        ))

        game_state.store = Store([
            StoreItem("Башенка", EnergyTower, 50,
                      "Башенка - удивительное оружие света, которое защитит вас от любого типа монстров"),
            StoreItem("Светилышко", LightTower, 100,
                      "Светилышко - это чудо! Не упускай момента чтобы купить 'Светилышко'!"),
            StoreItem("Просто башня", JustTower, 10,
                      "Ты нищеброд и у тебя не хватает денег даже на Башенку?! Бери 'Просто башню'! Пусть постоит")
        ])

        creator = NotificationCreator(game_state)
        creator.add_event(NotificationEvent(lambda: True, "Nothing happens..."))
        creator.add_event(NotificationEvent(lambda: game_state.money < 50, "Money is tight"))
        creator.add_event(NotificationEvent(lambda: game_state.map.fortress_health < 20, "Castle is in danger!"))
        creator.add_event(NotificationEvent(lambda: game_state.time.hour == 0, "New day starts!"))
        creator.add_event(NotificationEvent(lambda: game_state.time.hour == 12, "It is noon"))
        creator.add_event(
            NotificationEvent(lambda: game_state.game_result == GameResult.Win, "You win! Click 'Next level'"))
        creator.add_event(
            NotificationEvent(lambda: game_state.game_result == GameResult.Lose, "You lose! Click 'Restart'"))


        game_state.notification_creator = creator

        controller = MainController(game_state)
        game_state.set_controller(controller)

        fortress_position = game_state.map.get_cell_shape(game_state.map.height - 1,
                                                          0).get_center_of_mass()
        fortress = Fortress(game_state.map)
        fortress.move_to(fortress_position + Point(0, -10))
        game_state.map.add_tower(fortress)


class Level2(LevelLoader):
    level_id = 0

    @staticmethod
    def init_game(game_state):
        game_state.money = 250
        game_state.time = Time.fromHMS(12, 0, 0)

        game_state.map = GameMap(10, 10, game_state)

        game_state.map.initialize_from_file('map1.txt')

        Model.warriors.random_walker = BFSWalker(game_state.map)
        game_state.waves.append(Wave(
            game_state, Time.fromDHMS(0, 16, 0, 0),
            [SimpleWarrior, SimpleWarrior, SimpleWarrior, SimpleWarrior],
            [Point(400, 100), Point(300, 30), Point(350, 20)]
        ))

        game_state.waves.append(Wave(
            game_state, Time.fromDHMS(0, 23, 0, 0),
            [SimpleWarrior, SimpleWarrior, SimpleWarrior, SimpleWarrior, AdamantWarrior],
            [Point(400, 100), Point(350, 50)]
        ))

        game_state.waves.append(Wave(
            game_state, Time.fromDHMS(1, 5, 0, 0),
            [AdamantWarrior, SimpleWarrior],
            [Point(400, 100), Point(350, 50)]
        ))
        game_state.store = Store([
            StoreItem("Башенка", EnergyTower, 50,
                      "Башенка - удивительное оружие света, которое защитит вас от любого типа монстров"),
            StoreItem("Светилышко", LightTower, 100,
                      "Светилышко - это чудо! Не упускай момента чтобы купить 'Светилышко'!"),
            StoreItem("Просто башня", JustTower, 10,
                      "Ты нищеброд и у тебя не хватает денег даже на Башенку?! Бери 'Просто башню'! Пусть постоит")
        ])

        creator = NotificationCreator(game_state)
        creator.add_event(NotificationEvent(lambda: True, "Nothing happens..."))
        creator.add_event(NotificationEvent(lambda: game_state.money < 50, "Money is tight"))
        creator.add_event(NotificationEvent(lambda: game_state.map.fortress_health < 20, "Castle is in danger!"))
        creator.add_event(NotificationEvent(lambda: game_state.time.hour == 0, "New day starts!"))
        creator.add_event(NotificationEvent(lambda: game_state.time.hour == 12, "It is noon"))
        creator.add_event(
            NotificationEvent(lambda: game_state.map.adamant_is_coming, "Adamant is coming! Run away! Run away!")
        )
        creator.add_event(
            NotificationEvent(lambda: game_state.game_result == GameResult.Win, "You win! Click 'Next level'"))
        creator.add_event(
            NotificationEvent(lambda: game_state.game_result == GameResult.Lose, "You lose! Click 'Restart'"))

        game_state.notification_creator = creator

        controller = MainController(game_state)
        game_state.set_controller(controller)

        fortress_position = game_state.map.get_cell_shape(game_state.map.height - 1,
                                                          0).get_center_of_mass()
        fortress = Fortress(game_state.map)
        fortress.move_to(fortress_position + Point(0, -10))
        game_state.map.add_tower(fortress)


levels = [Level1, Level2]