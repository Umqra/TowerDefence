from Geometry.compare_double import *
from Geometry.line import Line
from Geometry.point import Point
from Geometry.segment import Segment

__author__ = 'umqra'


def is_point_in_bounding_box(P, bbox):
    return bbox[0].x <= P.x <= bbox[1].x and bbox[0].y <= P.y <= bbox[1].y


def intersects_bounding_boxes(a, b):
    return (max(a[0].x, b[0].x) <= min(a[1].x, b[1].x) and
            max(a[0].y, b[0].y) <= min(a[1].y, b[1].y))


class Polygon:
    def __init__(self, shape):
        self.shape = shape
        self._calc_bounding_box()

    def move(self, direction):
        for index in range(len(self.shape)):
            self.shape[index] += direction
        self._calc_bounding_box()

    def pull(self, k):
        for index in range(len(self.shape)):
            self.shape[index] *= k
        self._calc_bounding_box()

    def rotate_around_origin(self, angle):
        for index in range(len(self.shape)):
            self.shape[index] = self.shape[index].rotate(angle)
        self._calc_bounding_box()

    def rotate_around_point(self, P: Point, angle):
        self.move(P)
        self.rotate_around_origin(angle)
        self.move(-P)
        self._calc_bounding_box()

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
        if not is_point_in_bounding_box(P, self.get_bounding_box()):
            return False

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
        if not intersects_bounding_boxes(self.get_bounding_box(), other.get_bounding_box()):
            return False
        for p in other.shape:
            if self.contain_point(p):
                return True
        for p in self.shape:
            if other.contain_point(p):
                return True
        for self_side in self.get_side_segments():
            for other_side in other.get_side_segments():
                if self_side.intersect_with_segment(other_side) is not None:
                    return True
        return False

    def intersects_bounding_boxes(self, other):
        self_l, self_r = self.get_bounding_box()
        other_l, other_r = other.get_bounding_box()
        return (max(self_l.x, other_l.x) <= min(self_r.x, other_r.x) and
                max(self_l.y, other_l.y) <= min(self_r.y, other_r.y))

    def intersects_with_polygon_approximately(self, other):
        for p in other.shape:
            if self.contain_point(p):
                return True
        for p in self.shape:
            if other.contain_point(p):
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

    def _calc_bounding_box(self):
        minX, minY = self.shape[0].x, self.shape[0].y
        maxX, maxY = self.shape[0].x, self.shape[0].y
        for p in self.shape:
            minX = min(minX, p.x)
            maxX = max(maxX, p.x)

            minY = min(minY, p.y)
            maxY = max(maxY, p.y)
        self._bounding_box = (Point(minX, minY), Point(maxX, maxY))

    def get_bounding_box(self):
        return self._bounding_box

    def get_center_of_mass(self):
        sum_length = 0
        center_of_mass = Point()
        for side in self.get_side_segments():
            center_of_mass += side.center * side.length
            sum_length += side.length
        return center_of_mass / sum_length

    def __repr__(self):
        return 'Polygon({})'.format(repr(self.shape))

    def __str__(self):
        return str(self.shape)


class ConvexPolygon(Polygon):
    def __init__(self, shape):
        super().__init__(shape)

    def ccw_order_start_with_point(self, p):
        pos = self.shape.index(p)
        return self.ccw_order_start_with_index(pos)

    def ccw_order_start_with_index(self, pos):
        count_vertices = len(self.shape)
        direction = 1
        if less((self.shape[1] - self.shape[0]).cross_product(self.shape[2] - self.shape[0]), 0):
            direction = -1
        for i in range(count_vertices):
            yield self.shape[pos]
            pos = (pos + direction) % count_vertices

    def get_index_of_vertex(self, better):
        pos = 0
        count_vertices = len(self.shape)
        for i in range(1, count_vertices):
            if better(self.shape[i], self.shape[pos]):
                pos = i
        return pos

    def get_index_of_left_bottom(self):
        return self.get_index_of_vertex(lambda p1, p2: p1.x <= p2.x or (p1.x == p2.x and p1.y <= p2.y))

    def intersects_with_convex_polygon(self, other):
        pass


    def intersects_with_polygon(self, other):
        if isinstance(other, ConvexPolygon):
            return self.intersects_with_convex_polygon(other)
        return other.intersects_with_polygon(self)
