__author__ = 'umqra'


class GameEvent:
    pass


class CreateBulletEvent(GameEvent):
    def __init__(self, bullet):
        self.bullet = bullet
