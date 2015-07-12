from Geometry.compare_double import *
from Geometry.line import Line
from Geometry.point import Point
from Geometry.segment import Segment

__author__ = 'umqra'


class Polygon:
    def __init__(self, shape):
        self.shape = shape

    def move(self, direction):
        for index in range(len(self.shape)):
            self.shape[index] += direction

    def pull(self, k):
        for index in range(len(self.shape)):
            self.shape[index] *= k

    def rotate_around_origin(self, angle):
        for index in range(len(self.shape)):
            self.shape[index] = self.shape[index].rotate(angle)

    def rotate_around_point(self, P: Point, angle):
        self.move(P)
        self.rotate_around_origin(angle)
        self.move(-P)

    def get_side_segments(self):
        l = len(self.shape)
        for index in range(l):
            yield Segment(self.shape[index], self.shape[(index + 1) % l])

    def get_side_vectors(self):
        l = len(self.shape)
        vectors = []
        for index in range(l):
            vectors.append(self.shape[index] - self.shape[(index + 1) % l])
        return vectors

    def contain_point(self, P: Point):
        l = len(self.shape)
        count_intersections = 0
        for side in self.get_side_segments():
            l = side.based_line
            bottom_point = side.A if side.A.y < side.B.y else side.B
            if side.contain_point(P):
                return True
            intersection = l.intersect_with_line(Line(P, P + Point(1, 0)))
            if (intersection is not None and
                    side.contain_point(intersection) and
                    greater(intersection.x, P.x) and
                        intersection != bottom_point):
                count_intersections += 1
        return count_intersections % 2 == 1

    def contain_segment(self, segment: Segment):
        if not self.contain_point(segment.A) or not self.contain_point(segment.B):
            return False
        l = len(self.shape)
        for side in self.get_side_segments():
            p = side.intersect_with_segment(segment)
            if p is not None and p != side.A and p != side.B and p != segment.A and p != segment.B:
                return False
        return self.contain_point((segment.A + segment.B) / 2.)

    def intersects_with_polygon(self, other):
        for p in other.shape:
            if self.contain_point(p):
                return True
        for p in self.shape:
            if other.contain_point(p):
                return True
        self_l = len(self.shape)
        other_l = len(other.shape)
        for self_side in self.get_side_segments():
            for other_side in other.get_side_segments():
                if self_side.intersect_with_segment(other_side) is not None:
                    return True
        return False

    def distance_from_point(self, P: Point):
        if self.contain_point(P):
            return 0
        l = len(self.shape)
        distance = float('inf')
        for index in range(l):
            A = self.shape[index]
            B = self.shape[(index + 1) % l]
            s = Segment(A, B)
            distance = min(distance, s.dist_from_point(P))
        return distance

    # TODO: unittest covering
    def get_bounding_box(self):
        minX, minY = self.shape[0].x, self.shape[0].y
        maxX, maxY = self.shape[0].x, self.shape[0].y
        for p in self.shape:
            minX = min(minX, p.x)
            maxX = max(maxX, p.x)
            minY = min(minY, p.y)
            maxY = max(maxY, p.y)
        return Point(minX, minY), Point(maxX, maxY)

    # TODO: unittest covering
    def get_center_of_mass(self):
        sum_length = 0
        center_of_mass = Point()
        for side in self.get_side_segments():
            center_of_mass += side.center
            sum_length += side.length
        return center_of_mass / sum_length

    def __repr__(self):
        return 'Polygon({})'.format(repr(self.shape))

    def __str__(self):
        return str(self.shape)