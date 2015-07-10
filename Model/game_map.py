__author__ = 'umqra'
import re
import logging
import logging.config
import itertools

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
        self.spells = []
        self.map = [[None for _ in range(width)] for _ in range(height)]

        self.events = []

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

    def set_state(self, state):
        logging.info('Setting new state from map')
        self.state = state

    def add_view(self, view):
        logging.info('Adding view for map')
        self.views.append(view)

    def add_tower(self, tower):
        self.towers.append(tower)

    def add_warrior(self, warrior):
        self.warriors.append(warrior)

    def tick(self, dt):
        self.events.clear()
        for item in itertools.chain(self.warriors, self.towers):
            self.assign_cells(item)

        for item in itertools.chain(self.warriors, self.towers):
            self.events += item.tick(dt)

        for x in range(self.height):
            for y in range(self.width):
                new_events = self.map[x][y].tick(dt)
                if new_events is not None:
                    self.events += new_events

        self.process_events()

    def assign_cells(self, item):
        pass

    def process_events(self):
        pass