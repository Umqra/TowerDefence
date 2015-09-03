import copy
import random
import itertools
from Geometry.point import Point
from Geometry.polygon import Polygon
from Model.events import DeleteWarriorEvent
from Model.game_fraction import GameFraction
from Model.map_cell import MapCell

__author__ = 'umqra'


class Warrior:
    def __init__(self, shape, manipulator, fraction, health, speed, damage, damage_radius, direction):
        self.shape = shape
        self.manipulator = manipulator
        if manipulator is not None:
            manipulator.add_warrior(self)

        self.fraction = fraction
        self.health = health
        self.speed = speed
        self.damage = damage
        self.damage_radius = damage_radius
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
        self.manipulator.attack(self)
        self.manipulator.run(self, dt)

    def attack(self, item):
        item.damaged(self.damage)


def restore_path(start, end, parents):
    path = [end]
    while end != start:
        end = parents[end]
        path.append(end)
    return list(reversed(path))


class BFSWalker:
    def __init__(self, map):
        self.map = map
        self.warriors = []
        self.paths = {}

    def add_warrior(self, warrior):
        self.warriors.append(warrior)
        center = warrior.shape.get_center_of_mass()
        row = int(center.y // MapCell.cell_size)
        col = int(center.x // MapCell.cell_size)

        self.paths[warrior] = self.path_between_cells((row, col), (self.map.height - 1, 0))

    def remove_warrior(self, warrior):
        self.warriors.remove(warrior)

    def run(self, warrior, dt):
        center = warrior.shape.get_center_of_mass()
        row = int(center.y // MapCell.cell_size)
        col = int(center.x // MapCell.cell_size)
        path = self.paths[warrior]
        if path[0] == (row, col):
            path.pop(0)
        if path:
            next_cell = path[0]
            goal = self.map.get_cell_shape(*next_cell).get_center_of_mass()
            direction = goal - center
        else:
            direction = Point(0, 0)
            while direction == Point(0, 0):
                direction = Point(random.randint(-10, 10), random.randint(-10, 10))
        warrior.move_by(direction, dt)
        if not self.map.can_put_item(warrior):
            warrior.move_by(-direction, dt)
            if path:
                self.paths[warrior] = self.path_between_cells((row, col), (self.map.height - 1, 0), {path[0]})

    def path_between_cells(self, start, end, blocked=None):
        q = [start]
        used = {start}
        parents = {}
        q_size = 1
        it = 0
        if blocked is None:
            blocked = {}
        while it < q_size:
            x, y = q[it]
            it += 1
            for d in MapCell.directions:
                nx, ny = x + d[0], y + d[1]
                if (0 <= nx < self.map.height and 0 <= ny < self.map.width and
                        self.map.map[nx][ny].passable and not (nx, ny) in used and (nx, ny) not in blocked):
                    parents[(nx, ny)] = (x, y)
                    used.add((nx, ny))
                    q.append((nx, ny))
                    q_size += 1
        if end not in parents:
            return None
        return restore_path(start, end, parents)

    def get_nearest_item_to_point(self, point):
        nearest_item = None
        minimal_distance = None
        for item in itertools.chain(self.map.towers):
            shape = item.shape
            cur_distance = shape.distance_from_point(point)
            if minimal_distance is None or cur_distance < minimal_distance:
                minimal_distance = cur_distance
                nearest_item = item
        return nearest_item

    def attack(self, warrior):
        center = warrior.shape.get_center_of_mass()
        item = self.get_nearest_item_to_point(center)
        if item is None:
            return
        distance = item.shape.distance_from_point(center)
        if distance < warrior.damage_radius:
            warrior.attack(item)

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
        super().__init__(shape, random_walker, GameFraction.Dark, 100, 20, 0.05, 25, direction)
