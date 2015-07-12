__author__ = 'umqra'

from Geometry.compare_double import *
from Geometry.line import Line
from Geometry.point import Point


class Segment:
    def __init__(self, A: Point, B: Point):
        self.A = A
        self.B = B

    @property
    def length(self):
        return self.A.dist_to(self.B)

    @property
    def direction(self):
        return self.B - self.A

    @property
    def normal(self):
        return self.direction.orthogonal

    @property
    def based_line(self):
        return Line(self.A, self.B)

    @property
    def center(self):
        return (self.A + self.B) / 2

    def contain_point(self, P: Point):
        return (self.based_line.contain_point(P) and
                less_or_equal((P - self.A).dot_product(P - self.B), 0))

    def intersect_with_segment(self, other):
        line_intersection = self.based_line.intersect_with_line(other.based_line)
        if line_intersection is not None:
            return line_intersection if (self.contain_point(line_intersection) and
                                         other.contain_point(line_intersection)) else None
        return None

    def dist_from_point(self, P: Point):
        H = self.based_line.project_point(P)
        if self.contain_point(H):
            return P.dist_to(H)
        return min(P.dist_to(self.A), P.dist_to(self.B))

    def __eq__(self, other):
        return isinstance(other, Segment) and (
            (self.A == other.A and self.B == other.B) or
            (self.A == other.B and self.B == other.A)
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Segment({}, {})'.format(repr(self.A), repr(self.B))

    def __str__(self):
        return '[{}; {}]'.format(str(self.A), str(self.B))