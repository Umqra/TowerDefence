__author__ = 'umqra'

from Geometry.compare_double import *
from Geometry.point import Point
from Geometry.line import Line
from Geometry.segment import Segment
from Geometry.polygon import Polygon
import unittest


class TestPointMethods(unittest.TestCase):
    def test_add_points(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(Point(-1, 7), A + B)
        self.assertEqual(Point(1, 2), A + O)
        self.assertEqual(Point(-2, 5), B + O)

    def test_subtract_points(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(Point(3, -3), A - B)
        self.assertEqual(Point(1, 2), A - O)
        self.assertEqual(Point(2, -5), O - B)

    def test_multiply_points(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(Point(0.5, 1), A * 0.5)
        self.assertEqual(Point(6, -15), (-3) * B)
        self.assertEqual(Point(), O * 102)

    def test_dividing_points(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(Point(-2, -4), A / (-0.5))
        self.assertEqual(Point(-2 / 3, 5 / 3), B / 3)
        self.assertEqual(Point(), O / 102)

    def test_unary_operators(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(Point(-1, -2), -A)
        self.assertEqual(Point(-2, 5), +B)
        self.assertEqual(Point(), -O)

    def test_dot_product(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(8, A.dot_product(B))
        self.assertEqual(8, B.dot_product(A))
        self.assertEqual(3, A.dot_product(B - A))

    def test_cross_product(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertEqual(9, A.cross_product(B))
        self.assertEqual(-9, B.cross_product(A))
        self.assertEqual(9, A.cross_product(B - A))

    def test_length(self):
        A, B, O = Point(1, 2), Point(-2, 5), Point()
        self.assertTrue(equal(math.sqrt(5), A.length))
        self.assertTrue(equal(math.sqrt(29), B.length))
        self.assertTrue(equal(3 * math.sqrt(2), (B - A).length))
        self.assertTrue(equal(0, O.length))

    def test_setting_length(self):
        A, B, O = Point(3, 3), Point(-2, 5), Point()
        self.assertEqual(Point(1 / math.sqrt(2), 1 / math.sqrt(2)), A.set_length(1))
        self.assertEqual(Point(), B.set_length(0))
        with self.assertRaises(ValueError):
            O.set_length(1)
        self.assertEqual(Point(), O.set_length(0))

    def test_dist_to(self):
        A, B = Point(1, 2), Point(-2, 5)
        self.assertTrue(equal(3 * math.sqrt(2), A.dist_to(B)))

    def test_collinear(self):
        A, B, C = Point(1, 2), Point(-2, 5), Point(-2, -4)
        self.assertFalse(A.is_collinear(B))
        self.assertTrue(A.is_collinear(C))
        self.assertFalse(B.is_collinear(C))

    def test_rotate(self):
        A, B, C = Point(1, 2), Point(-2, 5), Point(1, 0)
        self.assertEqual(Point(-2, 1), A.rotate(math.pi / 2))
        self.assertEqual(Point(2, -5), B.rotate(math.pi))
        angle = math.pi / 3
        self.assertEqual(Point(math.cos(angle), math.sin(angle)), C.rotate(angle))

    def test_orthogonal(self):
        A, B = Point(1, 2), Point(-2, 5)
        self.assertTrue(equal(0, A.dot_product(A.orthogonal)))
        self.assertTrue(equal(0, B.dot_product(B.orthogonal)))


class TestLineMethods(unittest.TestCase):
    def test_direction(self):
        A, B = Point(1, 2), Point(-2, 5)
        direction = Point(1, -1)
        self.assertTrue(Line(A, B).direction.is_collinear(direction))

    def test_normal(self):
        A, B = Point(1, 2), Point(-2, 5)
        normal = Point(1, 1)
        self.assertTrue(Line(A, B).normal.is_collinear(normal))

    def test_contain_point(self):
        A, B = Point(1, 2), Point(-2, 5)
        P1 = Point(3, 0)
        P2 = Point(2, 2)
        self.assertTrue(Line(A, B).contain_point(P1))
        self.assertFalse(Line(A, B).contain_point(P2))

    def test_project_points(self):
        A, B = Point(1, 2), Point(-2, 5)
        P1 = Point(3, 0)
        P2 = Point(-1, 3)
        P3 = Point(-1, 2)
        self.assertEqual(Point(3, 0), Line(A, B).project_point(P1))
        self.assertEqual(Point(-0.5, 3.5), Line(A, B).project_point(P2))
        self.assertEqual(Point(0, 3), Line(A, B).project_point(P3))

    def test_dist_from_point(self):
        A, B = Point(1, 2), Point(-2, 5)
        P1 = Point(3, 0)
        P2 = Point(-1, 3)
        P3 = Point(-1, 2)
        self.assertTrue(equal(0, Line(A, B).dist_from_point(P1)))
        self.assertTrue(equal(math.sqrt(2) / 2, Line(A, B).dist_from_point(P2)))
        self.assertTrue(equal(math.sqrt(2), Line(A, B).dist_from_point(P3)))

    def test_intersect_lines(self):
        A1 = Point()
        A2 = Point(3, 2)
        B1 = Point(0, 7)
        B2 = Point(7, 0)
        C1 = Point(2, 5)
        C2 = Point(1, 6)
        D1 = Point(1, 5)
        D2 = Point(0, 6)
        self.assertEqual(Point(21 / 5, 14 / 5), Line(A1, A2).intersect_with_line(Line(B1, B2)))
        self.assertEqual(None, Line(B1, B2).intersect_with_line(Line(C1, C2)))
        self.assertEqual(None, Line(B1, B2).intersect_with_line(Line(D1, D2)))


class TestSegmentMethods(unittest.TestCase):
    def test_length(self):
        A, B = Point(1, 2), Point(22, 5)
        self.assertTrue(equal(A.dist_to(B), Segment(A, B).length))

    def test_direction(self):
        A, B = Point(1, 2), Point(-2, 5)
        self.assertTrue(Segment(A, B).direction.is_collinear(Point(-1, 1)))

    def test_normal(self):
        A, B = Point(1, 2), Point(-2, 5)
        self.assertTrue(Segment(A, B).normal.is_collinear(Point(-1, -1)))

    def test_based_line(self):
        A, B = Point(1, 2), Point(-2, 5)
        self.assertEqual(Line(Point(2, 1), Point(3, 0)), Segment(A, B).based_line)

    def test_contain_point(self):
        A, B = Point(1, 2), Point(-2, 5)
        P1 = Point(3, 0)
        P2 = Point(-1, 4)
        P3 = Point(-1, 2)
        self.assertFalse(Segment(A, B).contain_point(P1))
        self.assertTrue(Segment(A, B).contain_point(P2))
        self.assertFalse(Segment(A, B).contain_point(P3))

    def test_intersect_segments(self):
        A1 = Point()
        A2 = Point(3, 2)
        B1 = Point(3, 2)
        B2 = Point(6, 4)
        C1 = Point(0, 7)
        C2 = Point(7, 0)
        self.assertEqual(None, Segment(A1, A2).intersect_with_segment(Segment(B1, B2)))
        self.assertEqual(None, Segment(A1, A2).intersect_with_segment(Segment(C1, C2)))
        self.assertEqual(Point(21 / 5, 14 / 5), Segment(B1, B2).intersect_with_segment(Segment(C1, C2)))

    def test_dist_from_point(self):
        A, B = Point(1, 2), Point(-2, 5)
        P1 = Point(3, 0)
        P2 = Point(-1, 4)
        P3 = Point(-1, 2)
        self.assertTrue(equal(2 * math.sqrt(2), Segment(A, B).dist_from_point(P1)))
        self.assertTrue(equal(0, Segment(A, B).dist_from_point(P2)))
        self.assertTrue(equal(math.sqrt(2), Segment(A, B).dist_from_point(P3)))


class TestPolygonMethods(unittest.TestCase):
    def get_sample_polygon_1(self):
        return Polygon([
            Point(3, 2),
            Point(2, 5),
            Point(-1, 2),
            Point(-3, 5),
            Point(-3, -3),
            Point(-1, -1),
            Point(7, -4),
            Point(7, 1),
            Point(7, 2)])

    def get_sample_polygon_2(self):
        return Polygon([
            Point(4, 4),
            Point(5, 4),
            Point(5, 5),
            Point(4, 5)
        ])

    def get_sample_polygon_3(self):
        return Polygon([
            Point(7, -3),
            Point(9, -3),
            Point(9, -1),
            Point(7, -1)
        ])

    def get_sample_polygon_4(self):
        return Polygon([
            Point(4, -5),
            Point(5, -5),
            Point(5, 3),
            Point(4, 3)
        ])

    def test_contain_points(self):
        polygon = self.get_sample_polygon_1()
        P1 = Point(1, -4)
        P2 = Point(1, 1)
        P3 = Point(-2, 2)
        P4 = Point(-1, -1)
        self.assertFalse(polygon.contain_point(P1))
        self.assertTrue(polygon.contain_point(P2))
        self.assertTrue(polygon.contain_point(P3))
        self.assertTrue(polygon.contain_point(P4))

    def test_contain_segment(self):
        polygon = self.get_sample_polygon_1()
        S1 = Segment(Point(-1, 2), Point(-1, -1))
        S2 = Segment(Point(-2, 2), Point(3, 2))
        S3 = Segment(Point(1, 1), Point(4, -2))
        S4 = Segment(Point(-2, 3), Point(3, 0))
        S5 = Segment(Point(-3, -3), Point(7, -4))
        self.assertTrue(polygon.contain_segment(S1))
        self.assertTrue(polygon.contain_segment(S2))
        self.assertTrue(polygon.contain_segment(S3))
        self.assertFalse(polygon.contain_segment(S4))
        self.assertFalse(polygon.contain_segment(S5))

    def test_intersects_with_polygon(self):
        polygon1 = self.get_sample_polygon_1()
        polygon2 = self.get_sample_polygon_2()
        polygon3 = self.get_sample_polygon_3()
        polygon4 = self.get_sample_polygon_4()
        self.assertTrue(polygon1.intersects_with_polygon(polygon1))
        self.assertFalse(polygon1.intersects_with_polygon(polygon2))
        self.assertTrue(polygon1.intersects_with_polygon(polygon3))
        self.assertTrue(polygon1.intersects_with_polygon(polygon4))

    def test_distance_from_point(self):
        polygon = self.get_sample_polygon_1()
        P1 = Point(1, 1)
        P2 = Point(-1, 3)
        P3 = Point(2, 6)
        self.assertTrue(equal(0, polygon.distance_from_point(P1)))
        self.assertTrue(equal(math.sqrt(4 / 13), polygon.distance_from_point(P2)))
        self.assertTrue(equal(1, polygon.distance_from_point(P3)))

if __name__ == "__main__":
    unittest.main()