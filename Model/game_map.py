from Geometry.point import Point
from Geometry.polygon import Polygon
from Model.light import LightImpulse

__author__ = 'umqra'
import re
import logging
import logging.config
import itertools

from Model.events import *
from Model.map_cell import create_cell, MapCell


logging.config.fileConfig('logging.conf')


class MapFormatError(Exception):
    pass


class GameMap:
    def __init__(self, width, height, state):
        self.width = width
        self.height = height
        self.state = state
        self.views = []

        self.towers = []
        self.warriors = []
        self.bullets = []
        self.spells = []

        self.preview_items = []

        self.map = [[None for _ in range(width)] for _ in range(height)]

        self.events = []
        self.controller = None

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

    def add_tower(self, tower):
        if self.can_put_item(tower):
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