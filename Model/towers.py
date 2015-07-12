from Model.bullets import Bullet, EnergyBullet

__author__ = 'umqra'
from Model.events import CreateBulletEvent


class Tower:
    def __init__(self, figure, target_chooser, fraction):
        self.figure = figure
        self.target_chooser = target_chooser
        self.target = None
        self.fraction = fraction
        self.gun_position = figure.get_center_of_mass()
        self.occupied_cells = []

    def set_gun_position(self, pos):
        self.gun_position = pos

    def choose_target(self):
        self.target = self.target_chooser(self)

    def tick_init(self, dt):
        self.occupied_cells.clear()

    def add_cells(self, cell):
        self.occupied_cells.append(cell)

    def tick(self, dt):
        self.choose_target()
        self.attack()

    def attack(self):
        pass


class RechargeTower(Tower):
    def __init__(self, figure, target_chooser, fraction, damage, recharge_time):
        super().__init__(figure, target_chooser, fraction)
        self.recharge_time = recharge_time
        self.time_to_attack = 0
        self.damage = damage

    def tick(self, dt):
        self.time_to_attack -= dt
        if self.time_to_attack > 0:
            return
        self.choose_target()
        self.attack()
        self.time_to_attack = self.recharge_time


class EnergyTower(RechargeTower):
    def __init__(self, figure, target_chooser, fraction, damage, recharge_time):
        super().__init__(figure, target_chooser, fraction, damage, recharge_time)

    def attack(self):
        return CreateBulletEvent(EnergyBullet(self.gun_position, self.target.position, self.fraction, self.damage))