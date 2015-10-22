import copy
from Geometry.point import Point
from Geometry.polygon import Polygon
from Model.events import DeleteGateEvent
from Model.game_fraction import GameFraction

__author__ = 'umqra'
import random


class Gate:
    _default_shape = Polygon([Point(0, 0), Point(50, 0), Point(50, 50), Point(0, 50)])

    def __init__(self, map, position=None):
        if position is None:
            position = Point(0, 0)
        self.map = map
        self.shape = copy.deepcopy(Gate._default_shape)
        self.shape.move(position - self.shape.get_center_of_mass())
        self.target = None
        self.fraction = GameFraction.Dark
        self.health = 100
        self.occupied_cells = []
        self.selected = False

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def switch(self):
        self.selected = not self.selected

    def move_to(self, destination):
        direction = destination - self.shape.get_center_of_mass()
        self.shape.move(direction)

    def move_by(self, direction):
        self.shape.move(direction)

    @property
    def is_alive(self):
        return self.health > 0

    @is_alive.setter
    def is_alive(self, value):
        if not value:
            self.health = 0

    def tick_init(self, dt):
        self.occupied_cells.clear()

    def add_cell(self, cell):
        self.occupied_cells.append(cell)

    def tick(self, dt):
        if not self.is_alive:
            return [DeleteGateEvent(self)]

    def damaged(self, damage):
        self.health -= damage

    def is_valid_position_on_map(self):
        if self in self.map.gates:
            return True
        return self.map.can_put_item(self)

    def get_center(self):
        return self.shape.get_center_of_mass()


class Wave:
    def __init__(self, state, start_time, warriors, gates):
        self.state = state
        self.start_time = start_time
        self.warriors = warriors
        self.gates = gates

    def empty(self):
        return len(self.warriors) == 0

    def tick(self, dt):
        if self.state.time >= self.start_time:
            self.run_warriors()

    def run_warriors(self):
        random.shuffle(self.warriors)
        random.shuffle(self.gates)

        for gate in filter(lambda g: g.is_alive, self.gates):
            for creator in self.warriors:
                warrior = creator(gate.get_center())
                if self.state.map.can_put_item(warrior):
                    self.state.map.add_warrior(warrior)
                    self.warriors.remove(creator)
                    return

    def __getstate__(self):
        print(self.gates)
        return self.__dict__.copy()