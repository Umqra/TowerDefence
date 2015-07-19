import Model.bullets
from Model.game_fraction import is_warred_fractions

__author__ = 'umqra'


class GameEvent:
    pass


class CreateEvent(GameEvent):
    def __init__(self, item):
        self.item = item

    def process(self, state):
        pass


class CreateBulletEvent(CreateEvent):
    def __init__(self, bullet):
        super().__init__(bullet)

    def process(self, state):
        print("Add bullet ? {}".format(self.item))
        state.bullets.append(self.item)


class CreateTowerEvent(CreateEvent):
    def __init__(self, tower):
        super().__init__(tower)

    def process(self, state):
        print("Add tower ? {}".format(self.item))
        state.towers.append(self.item)


class CreateWarriorEvent(CreateEvent):
    def __init__(self, warrior):
        super().__init__(warrior)

    def process(self, state):
        print("Add warrior ? {}".format(self.item))
        state.warriors.append(self.item)


class CreateSpellEvent(CreateEvent):
    def __init__(self, spell):
        super().__init__(spell)

    def process(self, state):
        print("Add spell ? {}".format(self.item))
        state.spells.append(self.item)


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


class DeleteEvent(GameEvent):
    def __init__(self, item):
        self.item = item

    def process(self, state):
        pass


class DeleteBulletEvent(DeleteEvent):
    def __init__(self, item):
        super().__init__(item)

    def process(self, state):
        state.bullets.remove(self.item)


class DeleteTowerEvent(DeleteEvent):
    def __init__(self, item):
        super().__init__(item)

    def process(self, state):
        state.towers.remove(self.item)


class DeleteWarriorEvent(DeleteEvent):
    def __init__(self, item):
        super().__init__(item)

    def process(self, state):
        state.warriors.remove(self.item)


class DeleteSpellEvent(DeleteEvent):
    def __init__(self, item):
        super().__init__(item)

    def process(self, state):
        state.spells.remove(self.item)