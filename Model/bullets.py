from Geometry.point import Point
from Model.events import BulletHitEvent, DeleteBulletEvent

__author__ = 'umqra'

import Geometry.geometry_operations


class Bullet:
    def __init__(self, shape, target, fraction, damage, speed):
        self.is_alive = True
        self.shape = shape
        self.target = target
        self.fraction = fraction
        self.damage = damage
        self.direction = self.target.shape.get_center_of_mass() - self.shape.get_center_of_mass()
        self.speed = speed
        self.occupied_cells = []

        self.selected = False

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def add_cell(self, cell):
        self.occupied_cells.append(cell)

    def tick_init(self, dt):
        self.occupied_cells.clear()

    def tick(self, dt):
        if not self.is_alive:
            return [DeleteBulletEvent(self)]
        if self.target is not None and not self.target.is_alive:
            self.target = None
        if self.target is not None:
            self.direction = self.target.shape.get_center_of_mass() - self.shape.get_center_of_mass()
        if self.direction == Point():
            return
        delta = self.direction.set_length(dt * self.speed)
        self.shape.move(delta)
        return self.find_collisions()

    def find_collisions(self):
        events = []
        for cell in self.occupied_cells:
            for item in cell.items:
                if self == item:
                    continue
                if self.shape.intersects_bounding_boxes(item.shape):
                    events.append(BulletHitEvent(self, item))
        return events


class EnergyBullet(Bullet):
    bounding_box = 25
    def __init__(self, position, target, fraction, damage):
        shape = Geometry.geometry_operations.get_right_polygon(position, EnergyBullet.bounding_box / 2, 6)
        super().__init__(shape, target, fraction, damage, 100)
