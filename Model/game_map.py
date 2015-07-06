__author__ = 'umqra'
import re
import logging
import logging.config
from Model.light import LightImpulse, Lighting

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class MapFormatError(Exception):
    pass


class MapCell:
    def __init__(self, state, x, y, passable, lighting=None, adjacent=None, tick=False):
        self.state = state
        self.x = x
        self.y = y
        self.passable = passable
        self.lighting = lighting if lighting is not None else Lighting()
        self.adjacent = adjacent if adjacent is not None else []
        self.tick = tick

    def add_adjacent(self, cell):
        self.adjacent.append(cell)

    def start_tick(self):
        self.tick = True

    def tick(self, dt):
        normal_light = self.state.get_normal_light()
        self.lighting.change_to_value(normal_light, dt)
        for cell in self.adjacent:
            self.lighting.apply_impulse(cell.lighting, dt)

    def end_tick(self):
        self.tick = False

    def __repr__(self):
        return 'MapCell(state, {0}, {1}, {2}, {3}, {4}, {5})'.format(
            self.x, self.y, self.passable, repr(self.lighting), repr(self.adjacent), self.tick)

    def __str__(self):
        return '?'


class ForestCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None, tick=False):
        super().__init__(state, x, y, False, lighting, adjacent, tick)

    def __repr__(self):
        return 'ForestCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick)

    def __str__(self):
        return '|'


class RoadCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None):
        super().__init__(state, x, y, True, lighting, adjacent)

    def __repr__(self):
        return 'RoadCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick)

    def __str__(self):
        return '.'


class GrassCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None):
        super().__init__(state, x, y, True, lighting, adjacent)

    def __repr__(self):
        return 'GrassCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick)

    def __str__(self):
        return ','


class WaterCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None):
        super().__init__(state, x, y, False, lighting, adjacent)

    def __repr__(self):
        return 'WaterCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick)

    def __str__(self):
        return '~'


class GameMap:
    def __init__(self, width, height, state):
        self.width = width
        self.height = height
        self.state = state
        self.views = []
        self.map = [[None for _ in range(width)] for _ in range(height)]

    def initialize_from_file(self, filename):
        logger.info('Initialize map from file {}'.format(filename))
        try:
            with open(filename) as map_file:
                lines = map_file.readlines()
                if len(lines) != self.height:
                    raise MapFormatError('Error in map-file {}. {} lines, expected {}'
                                         .format(filename, len(lines), self.height))
                for line_index, line in enumerate(lines):
                    tokens = list(filter(lambda x: len(x) > 0, re.split(r'\s', line)))
                    if len(tokens) != self.width:
                        raise MapFormatError('Error in map-file {}:{}. {} tokens, expected {}'
                                             .format(filename, line_index, len(tokens), self.width))
                    self.map[line_index] = [token for token in tokens]
        except (FileExistsError, FileNotFoundError, MapFormatError) as e:
            logger.error(e)
            raise e

    def set_state(self, state):
        logger.info('Setting new state from map')
        self.state = state

    def add_view(self, view):
        logger.info('Adding view for map')
        self.views.append(view)
