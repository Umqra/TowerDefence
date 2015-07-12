from Model.game_fraction import is_warred_fractions

__author__ = 'umqra'


class GameEvent:
    pass


class CreateBulletEvent(GameEvent):
    def __init__(self, bullet):
        self.bullet = bullet

    def process(self, state):
        state.bullets.append(self.bullet)


class CollisionEvent(GameEvent):
    def __init__(self, first, second):
        self.first = first
        self.second = second


class BulletHitEvent(CollisionEvent):
    def __init__(self, bullet, target):
        super().__init__(bullet, target)
        self.bullet = bullet
        self.target = target

    def process(self):
        if is_warred_fractions(self.bullet.fraction, self.target.fraction):
            pass
