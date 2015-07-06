__author__ = 'umqra'
import re
import logging
import logging.config
import copy
from Model.light import LightImpulse, Lighting

logging.config.fileConfig('logging.conf')


class MapFormatError(Exception):
    pass


class MapCell:
    def __init__(self, state, x, y, passable, lighting=None, adjacent=None, tick_flag=False):
        self.state = state
        self.x = x
        self.y = y
        self.passable = passable
        self.lighting = lighting if lighting is not None else Lighting()
        self.adjacent = adjacent if adjacent is not None else []
        self.tick_flag = tick_flag

    def add_adjacent(self, cell):
        self.adjacent.append(cell)

    def start_tick(self):
        self.tick_flag = True

    def tick(self, dt):
        if not self.tick_flag:
            return
        normal_light = self.state.get_normal_light()
        self.lighting.change_to_value(normal_light, dt)
        quantum = self.lighting.emit(dt)
        for cell in self.adjacent:
            cell.lighting.light_impulse.value += quantum / len(self.adjacent)

    def end_tick(self):
        self.tick_flag = False

    def __repr__(self):
        return 'MapCell(state, {0}, {1}, {2}, {3}, {4}, {5})'.format(
            self.x, self.y, self.passable, repr(self.lighting), repr(self.adjacent), self.tick_flag)

    def __str__(self):
        return '?'


class ForestCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None, tick_flag=False):
        super().__init__(state, x, y, False, lighting, adjacent, tick_flag)

    def __repr__(self):
        return 'ForestCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick_flag)

    def __str__(self):
        return '|'


class RoadCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None):
        super().__init__(state, x, y, True, lighting, adjacent)

    def __repr__(self):
        return 'RoadCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick_flag)

    def __str__(self):
        return '.'


class GrassCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None):
        super().__init__(state, x, y, True, lighting, adjacent)

    def __repr__(self):
        return 'GrassCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick_flag)

    def __str__(self):
        return ','


class WaterCell(MapCell):
    def __init__(self, state, x, y, lighting=None, adjacent=None):
        super().__init__(state, x, y, False, lighting, adjacent)

    def __repr__(self):
        return 'WaterCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent), self.tick_flag)

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
        logging.info('Initialize map from file {}'.format(filename))
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
                    self.map[line_index] = [MapCell(self.state, line_index, column, True) for column, token in
                                            enumerate(tokens)]

        except (FileExistsError, FileNotFoundError, MapFormatError) as e:
            logging.error(e)
            raise e

        self.set_adjacent()

    def set_adjacent(self):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for x in range(self.height):
            for y in range(self.width):
                for d in directions:
                    nx, ny = x + d[0], y + d[1]
                    if 0 <= nx < self.height and 0 <= ny < self.width:
                        self.map[x][y].add_adjacent(self.map[nx][ny])

    def set_state(self, state):
        logging.info('Setting new state from map')
        self.state = state

    def add_view(self, view):
        logging.info('Adding view for map')
        self.views.append(view)
