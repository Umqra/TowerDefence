__author__ = 'umqra'
from Model.light import Lighting


class MapCell:
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    cell_size = 50

    def __init__(self, state, x, y, passable, cell_repr, lighting=None, adjacent=None):
        self.state = state
        self.x = x
        self.y = y
        self.passable = passable
        self.cell_repr = cell_repr
        self.lighting = lighting if lighting is not None else Lighting()
        self.adjacent = adjacent if adjacent is not None else []
        self.items = []

    def add_impulse(self, impulse):
        self.lighting.add_impulse(impulse)

    def add_adjacent(self, cell):
        self.adjacent.append(cell)

    def tick_init(self, dt):
        self.items.clear()

    def add_item(self, item):
        self.items.append(item)

    def tick(self, dt):
        normal_light = self.state.get_normal_light()
        self.lighting.change_to_value(normal_light, dt)
        quantum = self.lighting.emit(dt)
        for cell in self.adjacent:
            cell.lighting.light_impulse.value += quantum / len(self.adjacent)

    def __repr__(self):
        return 'MapCell(state, {0}, {1}, {2}, {3}, {4})'.format(
            self.x, self.y, self.passable, repr(self.lighting), repr(self.adjacent))

    def __str__(self):
        return '?'


class ForestCell(MapCell):
    def __init__(self, state, x, y, cell_repr, lighting=None, adjacent=None):
        super().__init__(state, x, y, False, cell_repr, lighting, adjacent)

    def __repr__(self):
        return 'ForestCell(state, {0}, {1}, {2}, {3})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent))

    def __str__(self):
        return '|'


class RoadCell(MapCell):
    def __init__(self, state, x, y, cell_repr, lighting=None, adjacent=None):
        super().__init__(state, x, y, True, cell_repr, lighting, adjacent)

    def __repr__(self):
        return 'RoadCell(state, {0}, {1}, {2}, {3})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent))

    def __str__(self):
        return '.'


class GrassCell(MapCell):
    def __init__(self, state, x, y, cell_repr, lighting=None, adjacent=None):
        super().__init__(state, x, y, True, cell_repr, lighting, adjacent)

    def __repr__(self):
        return 'GrassCell(state, {0}, {1}, {2}, {3})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent))

    def __str__(self):
        return ','


class WaterCell(MapCell):
    def __init__(self, state, x, y, cell_repr, lighting=None, adjacent=None):
        super().__init__(state, x, y, False, cell_repr, lighting, adjacent)

    def __repr__(self):
        return 'WaterCell(state, {0}, {1}, {2}, {3})'.format(
            self.x, self.y, repr(self.lighting), repr(self.adjacent))

    def __str__(self):
        return '~'


cells_dict = {
    "W": WaterCell,
    "~": WaterCell,
    'F': ForestCell,
    '|': ForestCell,
    'R': RoadCell,
    '.': RoadCell,
    'G': GrassCell,
    ',': GrassCell,
}


def create_cell(state, x, y, cell_repr):
    return cells_dict[cell_repr[0]](state, x, y, cell_repr)