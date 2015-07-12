from Geometry.point import Point
from Model.events import BulletHitEvent

__author__ = 'umqra'

import Geometry.geometry_operations


class Bullet:
    def __init__(self, shape, target, fraction, damage, speed):
        self.shape = shape
        self.target = target
        self.fraction = fraction
        self.damage = damage
        self.speed = speed
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def tick_init(self, dt):
        self.cells.clear()

    def tick(self, dt):
        direction = self.target.shape.get_center_of_mass() - self.shape.get_center_of_mass()
        if direction == Point():
            return
        direction = direction.set_length(dt * self.speed)
        self.shape.move(direction)
        return self.find_collisions()

    def find_collisions(self):
        events = []
        for cell in self.cells:
            for item in cell.items:
                if self == item:
                    continue
                if self.shape.intersects_with_polygon(item.shape):
                    events.append(BulletHitEvent(self, item))
        return events


class EnergyBullet(Bullet):
    def __init__(self, position, target, fraction, damage):
        shape = Geometry.geometry_operations.get_right_polygon(position, damage, 6)
        super().__init__(shape, target, fraction, damage, damage * 2)
