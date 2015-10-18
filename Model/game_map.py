from Geometry.point import Point
from Geometry.polygon import Polygon
from Model.bullets import Bullet
from Model.light import LightImpulse
from Model.towers import Tower, Fortress
from Model.warriors import Warrior, AdamantWarrior

__author__ = 'umqra'
import re
import logging
import logging.config
import itertools

from Model.events import *
from Model.map_cell import create_cell, MapCell


logging.config.fileConfig('logging.conf')

# 8 neighbors and center point
# 1 2 3
# 8 0 4
# 7 6 5
# using ? if cell type may be any

cell_repr_config = {
    'GGGGGGGGG': 'G1',
    'GGGGG?R?G': 'G2',
    'GGGGGRGGG': 'G3',
    'GGGGGGGRG': 'G4',
    'G?GGGGG?R': 'G5',
    'GRGGGGGGG': 'G6',
    'G?R?GGGGG': 'G7',
    'GGGRGGGGG': 'G8',
    'GGG?R?GGG': 'G9',
    'GRR??G??R': 'GA',
    'G?RRR??G?': 'GB',
    'G??G??RRR': 'GC',
    'GG??RRR??': 'GD',

    'R????????': 'R1',
}


def match_pattern(pattern, s):
    if len(pattern) != len(s):
        return False
    for i in range(len(s)):
        if pattern[i] == '?':
            continue
        if pattern[i] != s[i]:
            return False
    return True


def get_cell_repr(adj_types):
    s = ''.join(adj_types)
    for k in cell_repr_config.keys():
        if match_pattern(k, s):
            return cell_repr_config[k]
    print(s)

class MapFormatError(Exception):
    pass


def _get_adjacent_by_point(x, y):
    order = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    for i in range(9):
        for dx in range(3):
            for dy in range(3):
                if order[dx][dy] == i:
                    yield x + dx - 1, y + dy - 1


class GameMap:
    def __init__(self, width, height, state):
        self.width = width
        self.height = height
        self.state = state
        self.views = []

        self.towers = []
        self.fortress = None

        self.warriors = []
        self.bullets = []
        self.spells = []

        self.preview_items = []

        self.map = [[None for _ in range(width)] for _ in range(height)]

        self.events = []
        self.controller = None

    def get_cell_coordinates(self, x, y):
        return x // MapCell.cell_size, y // MapCell.cell_size

    @property
    def adamant_is_coming(self):
        for warrior in self.warriors:
            if isinstance(warrior, AdamantWarrior):
                return True
        return False

    @property
    def fortress_health(self):
        return max(self.fortress.health, 0) if self.fortress else 0

    @property
    def fortress_cell(self):
        cell = self.get_occupied_cells(self.fortress)[0]
        return (cell.x, cell.y) if self.fortress else (self.height - 1, 0)

    def get_random_item_cell(self, item):
        cell = self.get_occupied_cells(item)[0]
        return (cell.x, cell.y)

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
                    self.map[line_index] = [create_cell(self.state, line_index, column, token) for column, token in
                                            enumerate(tokens)]

        except (FileExistsError, FileNotFoundError, MapFormatError) as e:
            logging.error(e)
            raise e

        self.set_adjacent()

    def initialize_empty_map(self):
        for x in range(self.height):
            self.map[x] = [create_cell(self.state, x, y, 'G') for y in range(self.width)]
        self.assign_cell_types()

    def _get_cell_view_repr(self, x, y):
        if x < 0 or y < 0 or x >= self.height or y >= self.width:
            return 'G'
        return self.map[x][y].get_view_repr()

    def assign_cell_types(self):
        for x in range(self.height):
            for y in range(self.width):
                self.map[x][y].cell_repr = get_cell_repr(
                    map(
                        lambda pos: self._get_cell_view_repr(pos[0], pos[1]),
                        _get_adjacent_by_point(x, y)
                    )
                )

    def set_cell_type(self, x, y, t):
        self.map[x][y] = create_cell(self.state, x, y, t)
        print(t, self.map[x][y])
        self.assign_cell_types()
        self.update_views()

    def set_adjacent(self):
        for x in range(self.height):
            for y in range(self.width):
                for d in MapCell.directions:
                    nx, ny = x + d[0], y + d[1]
                    if 0 <= nx < self.height and 0 <= ny < self.width:
                        self.map[x][y].add_adjacent(self.map[nx][ny])

    def get_cell_shape(self, row, col):
        size = MapCell.cell_size
        center = Point(size * col + size / 2, size * row + size / 2)
        v = Point(size / 2, size / 2)
        u = Point(size / 2, -size / 2)
        return Polygon([
            center - v,
            center + u,
            center + v,
            center - u
        ])

    def set_state(self, state):
        logging.info('Setting new state from map')
        self.state = state

    def add_view(self, view):
        logging.info('Adding view for map')
        self.views.append(view)

    def can_put_item(self, item):
        for cell in self.get_occupied_cells(item):
            if not cell.passable:
                return False
        for map_item in itertools.chain(self.warriors, self.towers):
            if map_item != item and item.shape.intersects_with_polygon(map_item.shape):
                return False
        return True

    def add_item(self, item):
        if isinstance(item, Tower):
            self.add_tower(item)
        elif isinstance(item, Bullet):
            self.add_bullet(item)
        elif isinstance(item, Warrior):
            self.add_warrior(item)

    def add_tower(self, tower):
        if self.can_put_item(tower):
            if isinstance(tower, Fortress):
                self.fortress = tower
            self.process_events([CreateTowerEvent(tower)])
            return True
        return False

    def delete_tower(self, tower):
        self.process_events([DeleteTowerEvent(tower)])

    def add_warrior(self, warrior):
        self.process_events([CreateWarriorEvent(warrior)])

    def delete_warrior(self, warrior):
        self.process_events([DeleteWarriorEvent(warrior)])

    def add_bullet(self, bullet):
        self.process_events([CreateBulletEvent(bullet)])

    def delete_bullet(self, bullet):
        self.process_events([DeleteBulletEvent(bullet)])

    def tick_init(self, dt):
        for row in range(self.height):
            for col in range(self.width):
                self.map[row][col].tick_init(dt)
        for item in itertools.chain(self.warriors, self.towers, self.preview_items):
            item.tick_init(dt)

    def tick(self, dt):
        self.tick_init(dt)
        events = []
        for item in itertools.chain(self.warriors, self.towers, self.bullets):
            item.tick_init(dt)
            self.assign_cells(item)

        for item in itertools.chain(self.warriors, self.towers, self.bullets):
            new_events = item.tick(dt)
            if new_events is not None:
                events += new_events

        for x in range(self.height):
            for y in range(self.width):
                new_events = self.map[x][y].tick(dt)
                if new_events is not None:
                    events += new_events

        self.process_events(events)

    def get_occupied_cells(self, item):
        cells = []
        shape = item.shape
        bounding_box = shape.get_bounding_box()
        x_l = max(int(bounding_box[0].x // MapCell.cell_size), 0)
        x_r = min(int(bounding_box[1].x // MapCell.cell_size) + 1, self.width)
        y_l = max(int(bounding_box[0].y // MapCell.cell_size), 0)
        y_r = min(int(bounding_box[1].y // MapCell.cell_size) + 1, self.height)
        for row in range(y_l, y_r):
            for col in range(x_l, x_r):
                cell_polygon = self.get_cell_shape(row, col)
                if cell_polygon.intersects_with_polygon(shape):
                    cells.append(self.map[row][col])
        return cells

    def assign_cells(self, item):
        for cell in self.get_occupied_cells(item):
            item.add_cell(cell)
            cell.add_item(item)

    def process_events(self, events):
        for event in events:
            event.process(self)
        for view in self.views:
            view.process_events(events)

    def get_items_at_position(self, x, y):
        row = x // MapCell.cell_size
        col = y // MapCell.cell_size
        return self.map[row][col].items

    def add_preview_item(self, preview_item):
        self.process_events([CreatePreviewEvent(preview_item)])

    def remove_preview_item(self, preview_item):
        self.process_events([DeletePreviewEvent(preview_item)])

    def set_controller(self, controller):
        self.controller = controller

    def update_views(self):
        for x in range(self.height):
            for y in range(self.width):
                print(self.map[x][y], end='')
            print("")
        for view in self.views:
            view.update()