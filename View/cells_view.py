from PyQt4.QtGui import QWidget, QPainter, QColor, QGridLayout, QImage, QPixmap
from Model.map_cell import *

__author__ = 'umqra'


class LightView(QWidget):
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

                qp.fillRect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size,
                            QColor.fromRgbF(0, 0, 0, (1 - value / 255) / 2))


images = {
    "F1": QImage('Resources/Images/F1.png').scaledToWidth(50),
    "G1": QImage('Resources/Images/G1.png').scaledToWidth(50),
    "R1": QImage('Resources/Images/R1.png').scaledToWidth(50),
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