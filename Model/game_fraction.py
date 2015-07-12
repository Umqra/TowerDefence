__author__ = 'umqra'

from enum import Enum


class GameFraction(Enum):
    Light = "Light"
    Dark = "Dark"
    Neutral = "Neutral"


warred_fractions = {
    (GameFraction.Light, GameFraction.Dark),
    (GameFraction.Neutral, GameFraction.Dark)
}


def is_warred_fractions(first, second):
    return ((first, second) in warred_fractions or
            (second, first) in warred_fractions)
