__author__ = 'umqra'

from Geometry.point import Point
from Geometry.polygon import Polygon
from Geometry.segment import Segment
from Geometry.line import Line
from Geometry.compare_double import *
import math


def get_right_polygon(center, radius, count_corners):
    angle = 2 * math.pi / count_corners
    p = Point(radius, 0)
    corners = [center + p]
    for i in range(1, count_corners):
        p = p.rotate(angle)
        corners.append(center + p)
    return Polygon(corners)