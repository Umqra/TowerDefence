import copy
import itertools
from Geometry.point import Point
from Geometry.polygon import Polygon
from Model.bullets import Bullet, EnergyBullet
from Model.light import Lighting, LightImpulse

__author__ = 'umqra'
from Model.events import CreateBulletEvent, DeleteTowerEvent
from Model.game_fraction import is_warred_fractions, GameFraction


class SimpleChooser:
    def __init__(self, map):
        self.map = map
        self.towers = []

    def add_tower(self, tower):
        self.towers.append(tower)

    def remove_tower(self, tower):
        self.towers.remove(tower)

    def choose(self, tower):
        for item in itertools.chain(self.map.towers, self.map.bullets, self.map.warriors):
            if is_warred_fractions(item.fraction, tower.fraction):
                return item


class Tower:
    def __init__(self, shape, target_chooser, fraction, health):
        self.shape = shape
        self.target = None
        self.fraction = fraction
        self.health = health
        self.gun_position = shape.get_center_of_mass()
        self.occupied_cells = []

        self.target_chooser = target_chooser
        if target_chooser is not None:
            target_chooser.add_tower(self)

        self.selected = False

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

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def set_gun_position(self, pos):
        self.gun_position = pos

    def choose_target(self):
        self.target = self.target_chooser.choose(self)

    def tick_init(self, dt):
        self.occupied_cells.clear()

    def add_cell(self, cell):
        self.occupied_cells.append(cell)

    def tick(self, dt):
        if not self.is_alive:
            return [DeleteTowerEvent(self)]
        self.choose_target()
        self.attack()

    def attack(self):
        pass

    def damaged(self, damage):
        self.health -= damage


class RechargeTower(Tower):
    def __init__(self, shape, target_chooser, fraction, health, damage, recharge_time):
        super().__init__(shape, target_chooser, fraction, health)
        self.recharge_time = recharge_time
        self.time_to_attack = 0
        self.damage = damage

    def tick(self, dt):
        if not self.is_alive:
            return [DeleteTowerEvent(self)]
        self.time_to_attack = max(0, self.time_to_attack - dt)
        if self.time_to_attack > 0:
            return
        self.choose_target()
        if self.target is not None:
            self.time_to_attack = self.recharge_time
        return self.attack()


energy_tower_default_shape = Polygon([
    Point(0, 0),
    Point(50, 0),
    Point(50, 50),
    Point(0, 50)
])

simple_chooser = None


class EnergyTower(RechargeTower):
    def __init__(self, shape=None, target_chooser=None, fraction=GameFraction.Light, health=100,
                 damage=20, recharge_time=5):
        if shape is None:
            shape = copy.deepcopy(energy_tower_default_shape)
        if target_chooser is None:
            target_chooser = simple_chooser
        super().__init__(shape, target_chooser, fraction, health, damage, recharge_time)

    def attack(self):
        if self.target is None:
            return
        average_impulse = 0
        for cell in self.occupied_cells:
            average_impulse += cell.lighting.value
        average_impulse /= len(self.occupied_cells)
        cur_damage = self.damage * (average_impulse / 100)
        return [CreateBulletEvent(
            EnergyBullet(self.gun_position, self.target, self.fraction, cur_damage))]


light_tower_default_shape = Polygon([
    Point(0, 0),
    Point(50, 0),
    Point(50, 50),
    Point(0, 50)
])


class LightTower(RechargeTower):
    def __init__(self, shape=None, fraction=GameFraction.Light, health=100, impulse_force=200,
                 recharge_time=5):
        if shape is None:
            shape = copy.deepcopy(light_tower_default_shape)
        super().__init__(shape, None, fraction, health, None, recharge_time)
        self.impulse_force = impulse_force

    def tick(self, dt):
        if not self.is_alive:
            return [DeleteTowerEvent(self)]
        self.time_to_attack = max(0, self.time_to_attack - dt)
        if self.time_to_attack > 0:
            return
        for cell in self.occupied_cells:
            cell.add_impulse(LightImpulse(self.impulse_force))
        self.time_to_attack = self.recharge_time


class Fortress(Tower):
    pass