__author__ = 'umqra'

import math

default_epsilon = 1e-8


def equal(a, b, eps=default_epsilon):
    return math.fabs(a - b) < eps


def not_equal(a, b, eps=default_epsilon):
    return not equal(a, b, eps)


def less(a, b, eps=default_epsilon):
    return a < b and not equal(a, b, eps)


def less_or_equal(a, b, eps=default_epsilon):
    return a < b or equal(a, b, eps)


def greater(a, b, eps=default_epsilon):
    return a > b and not equal(a, b, eps)


def greater_or_equal(a, b, eps=default_epsilon):
    return a > b or equal(a, b, eps)

