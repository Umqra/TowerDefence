import math

__author__ = 'umqra'
from numbers import Real

from Geometry.compare_double import *


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Point.__add__: expected Point, given {}".format(type(other)))
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Point.__sub__: expected Point, given {}".format(type(other)))
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        if not isinstance(k, Real):
            raise TypeError("Point.__mul__: expected Real, given {}".format(type(k)))
        return Point(self.x * k, self.y * k)

    def __rmul__(self, k):
        if not isinstance(k, Real):
            raise TypeError("Point.__rmul__: expected Real, given {}".format(type(k)))
        return Point(self.x * k, self.y * k)

    def __truediv__(self, k):
        if not isinstance(k, Real):
            raise TypeError("Point.__truediv__: expected Real, given {}".format(type(k)))
        if equal(k, 0):
            raise ValueError("Point.__truediv__: k must be non-zero")
        return Point(self.x / k, self.y / k)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __pos__(self):
        return Point(self.x, self.y)

    def dot_product(self, other):
        if not isinstance(other, Point):
            raise TypeError("Point.dot_product: expected Point, given {}".format(type(other)))
        return self.x * other.x + self.y * other.y

    def cross_product(self, other):
        if not isinstance(other, Point):
            raise TypeError("Point.cross_product: expected Point, given {}".format(type(other)))
        return self.x * other.y - self.y * other.x

    @property
    def length(self):
        return math.sqrt(self.dot_product(self))

    def set_length(self, new_len):
        if not isinstance(new_len, Real):
            raise TypeError("Point.set_length: expected Real, given {}".format(type(new_len)))
        if self == Point():
            if not_equal(new_len, 0):
                raise ValueError("Point.set_length: try set non-zero length to zero vector")
            return Point()
        return self / self.length * new_len

    def dist_to(self, other):
        if not isinstance(other, Point):
            raise TypeError("Point.dist_to: expected Point, given {}".format(type(other)))
        return (self - other).length

    def is_collinear(self, other):
        return equal(self.cross_product(other), 0)

    def __eq__(self, other):
        return isinstance(other, Point) and (
            equal(self.x, other.x) and equal(self.y, other.y)
        )

    def __ne__(self, other):
        return not self == other

    def rotate(self, angle):
        if not isinstance(angle, Real):
            raise TypeError("Point.rotate: expected Real, given {}".format(type(angle)))
        cosa = math.cos(angle)
        sina = math.sin(angle)
        return Point(self.x * cosa - self.y * sina, self.x * sina + self.y * cosa)

    @property
    def orthogonal(self):
        return Point(-self.y, self.x)

    def __repr__(self):
        return 'Point({:.2f}, {:.2f})'.format(self.x, self.y)

    def __str__(self):
        return '({:.2f}, {:.2f})'.format(self.x, self.y)