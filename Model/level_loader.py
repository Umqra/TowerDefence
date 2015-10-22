import jsonpickle
import pickle
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


def is_last_level(game_state):
    level_loader = game_state.loader
    if not hasattr(level_loader, 'level_id'):
        return True

    level_id = level_loader.level_id
    if level_id in bonus_rules and bonus_rules[level_id](game_state):
        return False
    return not level_id in next_level


def initialize_notification(game_state):
    creator = NotificationCreator(game_state)
    creator.add_event(NotificationEvent(lambda: game_state.money < 50, "Money is tight"))
    creator.add_event(NotificationEvent(lambda: game_state.map.fortress_health < 20, "Castle is in danger!"))
    creator.add_event(NotificationEvent(lambda: game_state.time.hour == 0, "New day starts!"))
    creator.add_event(
        NotificationEvent(lambda: game_state.game_result == GameResult.Win, "You win! Click 'Next level'"))
    creator.add_event(
        NotificationEvent(lambda: game_state.game_result == GameResult.Lose, "You lose! Click 'Restart'"))
    creator.add_event(
        NotificationEvent(lambda: game_state.game_result == GameResult.Win and is_last_level(game_state),
                          'You did it! You save the world!')
    )
    game_state.notification_creator = creator


def load_level_from_file(filename):
    game_state = pickle.load(open(filename, 'rb'))
    Model.warriors.random_walker = BFSWalker(game_state.map)
    game_state.store = Store([
        StoreItem("Башенка", EnergyTower, 50,
                  "Башенка - удивительное оружие света, которое защитит вас от любого типа монстров"),
        StoreItem("Светилышко", LightTower, 100,
                  "Светилышко - это чудо! Не упускай момента чтобы купить 'Светилышко'!"),
        StoreItem("Просто башня", JustTower, 10,
                  "Ты нищеброд и у тебя не хватает денег даже на Башенку?! Бери 'Просто башню'! Пусть постоит")
    ])
    game_state.set_controller(MainController(game_state))
    initialize_notification(game_state)
    return game_state


def get_level_loader(file_name, level):
    class UniversalLevelLoader(LevelLoader):
        level_id = level

        @staticmethod
        def init_game(game_state):
            new_state = load_level_from_file(file_name)
            game_state.time = new_state.time
            game_state.money = new_state.money
            game_state.map = new_state.map
            game_state.map.state = game_state

            game_state.waves = new_state.waves
            game_state.store = new_state.store
            game_state.notification_creator = new_state.notification_creator
            game_state.set_controller(MainController(game_state))
            initialize_notification(game_state)

    return UniversalLevelLoader


levels = [
    get_level_loader('level_1.tdl', 'Level 1'),
    #get_level_loader('level_2.tdl', 'Level 2'),
    get_level_loader('bonus_level_1.tdl', 'Bonus level 1')]
next_level = {
    #'Level 1': 'Level 2',
    #'Bonus level 1': 'Level 2',
}
bonus_levels = {
    'Level 1': 'Bonus level 1'
}
bonus_rules = {
    'Level 1': lambda state: state.time.day < 20
}