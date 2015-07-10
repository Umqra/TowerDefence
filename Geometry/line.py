__author__ = 'umqra'

from Geometry.compare_double import *
from Geometry.point import Point


class Line:
    def __init__(self, A: Point, B: Point):
        self.A = A
        self.B = B

    @property
    def direction(self):
        return self.B - self.A

    @property
    def normal(self):
        return self.direction.orthogonal

    def contain_point(self, P: Point):
        return equal((self.A - P).cross_product(self.direction), 0)

    def project_point(self, P: Point):
        return self.A + self.direction * (P - self.A).dot_product(self.direction) / self.direction.length**2

    def dist_from_point(self, P: Point):
        return self.project_point(P).dist_to(P)

    def intersect_with_line(self, other):
        if equal(self.direction.cross_product(other.direction), 0):
            return None
        v = self.direction
        u = other.direction
        k = (self.A.cross_product(v) - other.A.cross_product(v)) / (u.cross_product(v))
        return other.A + u * k

    def __eq__(self, other):
        return isinstance(other, Line) and (
            self.direction.is_collinear(other.direction) and
            equal(self.direction.cross_product(other.A - self.A), 0)
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Line({}, {})'.format(repr(self.A), repr(self.B))

    def __str__(self):
        return '({}; {})'.format(str(self.A), str(self.B))