import Model.bullets
from Model.game_fraction import is_warred_fractions

__author__ = 'umqra'


class GameEvent:
    pass


class CreateBulletEvent(GameEvent):
    def __init__(self, bullet):
        self.bullet = bullet

    def process(self, state):
        print("Add bullet ? {}".format(self.bullet))
        state.bullets.append(self.bullet)


class CollisionEvent(GameEvent):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def process(self, state):
        pass


class BulletHitEvent(CollisionEvent):
    def __init__(self, bullet, target):
        super().__init__(bullet, target)
        self.bullet = bullet
        self.target = target

    def process(self, state):
        if is_warred_fractions(self.bullet.fraction, self.target.fraction):
            if isinstance(self.target, Model.bullets.Bullet):
                self.target.is_alive = False
            else:
                self.target.damaged(self.bullet.damage)
            self.bullet.is_alive = False


class DieEvent(GameEvent):
    def __init__(self, item):
        self.item = item

    def process(self, state):
        pass


class BulletDieEvent(DieEvent):
    def __init__(self, item):
        super().__init__(item)

    def process(self, state):
        state.delete_bullet(self.item)


class TowerDieEvent(DieEvent):
    def __init__(self, item):
        super().__init__(item)

    def process(self, state):
        state.delete_tower(self.item)