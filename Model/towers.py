import itertools
from Model.bullets import Bullet, EnergyBullet

__author__ = 'umqra'
from Model.events import CreateBulletEvent, DeleteTowerEvent
from Model.game_fraction import is_warred_fractions


class SimpleChooser:
    def __init__(self, state):
        self.state = state
        self.towers = []

    def add_tower(self, tower):
        self.towers.append(tower)

    def remove_tower(self, tower):
        self.towers.remove(tower)

    def choose(self, tower):
        for item in itertools.chain(self.state.towers, self.state.bullets, self.state.warriors):
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
        target_chooser.add_tower(self)

    @property
    def is_alive(self):
        return self.health > 0

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
            return [TowerDeleteEvent(self)]
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
        self.time_to_attack -= dt
        if self.time_to_attack > 0:
            return
        self.choose_target()
        self.time_to_attack = self.recharge_time
        return self.attack()


class EnergyTower(RechargeTower):
    def __init__(self, shape, target_chooser, fraction, health=10, damage=10, recharge_time=5):
        super().__init__(shape, target_chooser, fraction, health, damage, recharge_time)

    def attack(self):
        if self.target is None:
            return
        return [CreateBulletEvent(
            EnergyBullet(self.gun_position, self.target, self.fraction, self.damage))]