__author__ = 'umqra'

from Geometry.point import Point


class Segment:
    def __init__(self, A: Point, B: Point):
        self.A = A
        self.B = B

    @property
    def length(self):
        return self.A.dist_to(self.B)