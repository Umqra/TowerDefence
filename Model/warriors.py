import copy
import random
from Geometry.point import Point
from Geometry.polygon import Polygon
from Model.events import DeleteWarriorEvent
from Model.game_fraction import GameFraction

__author__ = 'umqra'


class Warrior:
    def __init__(self, shape, manipulator, target_chooser, fraction, health, speed, direction):
        self.shape = shape
        self.manipulator = manipulator
        if manipulator is not None:
            manipulator.add_warrior(self)

        self.target_chooser = target_chooser
        if target_chooser is not None:
            target_chooser.add_warrior(self)

        self.fraction = fraction
        self.health = health
        self.speed = speed
        self.direction = direction
        self.occupied_cells = []
        self.target = None

        self.selected = False

    def move_to(self, destination, dt):
        self.direction = destination - self.shape.get_center_of_mass()
        self.direction = self.direction.set_length(dt * self.speed)
        self.shape.move(self.direction)

    def move_by(self, direction, dt):
        self.direction = direction.set_length(dt * self.speed)
        self.shape.move(self.direction)

    @property
    def is_alive(self):
        return self.health > 0

    @is_alive.setter
    def is_alive(self, value):
        if not value:
            self.health = 0

    def damaged(self, damage):
        self.health -= damage

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def tick_init(self, dt):
        self.occupied_cells.clear()

    def add_cell(self, cell):
        self.occupied_cells.append(cell)

    def tick(self, dt):
        if not self.is_alive:
            return [DeleteWarriorEvent(self)]
        self.choose_target()
        self.attack()
        self.manipulator.run(self, dt)

    def choose_target(self):
        if self.target_chooser is not None:
            self.target = self.target_chooser.choose(self)

    def attack(self):
        pass


class RandomWalker:
    def __init__(self, map):
        self.map = map
        self.warriors = []

    def add_warrior(self, warrior):
        self.warriors.append(warrior)

    def remove_warrior(self, warrior):
        self.warriors.remove(warrior)

    def run(self, warrior, dt):
        direction = Point(random.randint(1, 10), random.randint(1, 10))

        warrior.move_by(direction, dt)
        if not self.map.can_put_item(warrior):
            warrior.move_by(-direction, dt)


random_walker = None

simple_warrior_shape = Polygon([
    Point(0, 0),
    Point(20, 0),
    Point(20, 20),
    Point(0, 20)
])


class SimpleWarrior(Warrior):
    def __init__(self, position, direction=None):
        shape = copy.deepcopy(simple_warrior_shape)
        shape.move(position)
        if direction is None:
            direction = Point(-1, 1)
        super().__init__(shape, random_walker, None, GameFraction.Dark, 100, 10, direction)
