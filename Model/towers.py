__author__ = 'umqra'
from Model.events import CreateBulletEvent


class Tower:
    def __init__(self, figure, target_chooser):
        self.figure = figure
        self.target_chooser = target_chooser
        self.target = None

    def choose_target(self):
        self.target = self.target_chooser(self)

    def tick(self, dt):
        self.choose_target()
        self.attack()

    def attack(self):
        pass


class EnergyTower(Tower):
    def __init__(self, figure, target_chooser, damage):
        super().__init__(figure, target_chooser)
        self.damage = damage

    def attack(self):
        return CreateBulletEvent(Bullet(figure.position, self.target.position, self.damage))
