from PyQt4.QtGui import QWidget, QPainter, QColor, QGridLayout, QImage, QPixmap
from Infrastructure.get_resources import load_image
from Model.map_cell import *

__author__ = 'umqra'


class LightView(QWidget):
    view_fading = 0.8

    def __init__(self, model, cell_size=50):
        super().__init__()
        self.model = model
        self.cell_size = cell_size

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        for row in range(self.model.height):
            for col in range(self.model.width):
                value = int(self.model.map[row][col].lighting.value)

                qp.fillRect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size,
                            QColor.fromRgbF(0, 0, 0, (1 - value / 255) * LightView.view_fading))


images = {
    "F1": load_image('F1.png', 50),
    "F2": load_image('F2.png', 50),
    "F3": load_image('F3.png', 50),
    "F4": load_image('F4.png', 50),
    "F5": load_image('F5.png', 50),
    "F6": load_image('F6.png', 50),
    "F7": load_image('F7.png', 50),
    "F8": load_image('F8.png', 50),
    "F9": load_image('F9.png', 50),

    "FA": load_image('FA.png', 50),
    "FB": load_image('FB.png', 50),
    "FC": load_image('FC.png', 50),
    "FD": load_image('FD.png', 50),

    "G1": load_image('G1.png', 50),
    "G2": load_image('G2.png', 50),
    "G3": load_image('G3.png', 50),
    "G4": load_image('G4.png', 50),
    "G5": load_image('G5.png', 50),
    "G6": load_image('G6.png', 50),
    "G7": load_image('G7.png', 50),
    "G8": load_image('G8.png', 50),
    "G9": load_image('G9.png', 50),

    "GA": load_image('GA.png', 50),
    "GB": load_image('GB.png', 50),
    "GC": load_image('GC.png', 50),
    "GD": load_image('GD.png', 50),

    "R1": load_image('R1.png', 50),
}


class CellsView(QWidget):
    def __init__(self, model, cell_size=50):
        super().__init__()
        self.model = model
        self.cell_size = cell_size
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.setMaximumWidth(500)
        self.setMaximumHeight(500)
        self.setLayout(self.layout)
        self.init_cells()

    def init_cells(self):
        for row in range(self.model.height):
            self.layout.setRowMinimumHeight(row, self.cell_size)
        for col in range(self.model.width):
            self.layout.setColumnMinimumWidth(col, self.cell_size)
        for row in range(self.model.height):
            for col in range(self.model.width):
                self.layout.addWidget(create_cell_view(self.model.map[row][col]), row, col)


class CellView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model


class ForestCellView(CellView):
    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(0, 0, QPixmap(images[self.model.cell_repr]))


class RoadCellView(CellView):
    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(0, 0, QPixmap(images[self.model.cell_repr]))


class GrassCellView(CellView):
    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(0, 0, QPixmap(images[self.model.cell_repr]))


class WaterCellView(CellView):
    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(0, 0, QPixmap(images[self.model.cell_repr]))


def create_cell_view(cell):
    if isinstance(cell, ForestCell):
        return ForestCellView(cell)
    elif isinstance(cell, RoadCell):
        return RoadCellView(cell)
    elif isinstance(cell, GrassCell):
        return GrassCellView(cell)
    elif isinstance(cell, WaterCell):
        return WaterCellView(cell)
    raise TypeError
