from PyQt4.QtGui import QWidget, QPainter, QColor, QGridLayout, QImage, QPixmap
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
    "F1": QImage('Resources/Images/F1.png').scaledToWidth(50),
    "F2": QImage('Resources/Images/F2.png').scaledToWidth(50),
    "F3": QImage('Resources/Images/F3.png').scaledToWidth(50),
    "F4": QImage('Resources/Images/F4.png').scaledToWidth(50),
    "F5": QImage('Resources/Images/F5.png').scaledToWidth(50),
    "F6": QImage('Resources/Images/F6.png').scaledToWidth(50),
    "F7": QImage('Resources/Images/F7.png').scaledToWidth(50),
    "F8": QImage('Resources/Images/F8.png').scaledToWidth(50),
    "F9": QImage('Resources/Images/F9.png').scaledToWidth(50),

    "FA": QImage('Resources/Images/FA.png').scaledToWidth(50),
    "FB": QImage('Resources/Images/FB.png').scaledToWidth(50),
    "FC": QImage('Resources/Images/FC.png').scaledToWidth(50),
    "FD": QImage('Resources/Images/FD.png').scaledToWidth(50),


    "G1": QImage('Resources/Images/G1.png').scaledToWidth(50),
    "G2": QImage('Resources/Images/G2.png').scaledToWidth(50),
    "G3": QImage('Resources/Images/G3.png').scaledToWidth(50),
    "G4": QImage('Resources/Images/G4.png').scaledToWidth(50),
    "G5": QImage('Resources/Images/G5.png').scaledToWidth(50),
    "G6": QImage('Resources/Images/G6.png').scaledToWidth(50),
    "G7": QImage('Resources/Images/G7.png').scaledToWidth(50),
    "G8": QImage('Resources/Images/G8.png').scaledToWidth(50),
    "G9": QImage('Resources/Images/G9.png').scaledToWidth(50),

    "GA": QImage('Resources/Images/GA.png').scaledToWidth(50),
    "GB": QImage('Resources/Images/GB.png').scaledToWidth(50),
    "GC": QImage('Resources/Images/GC.png').scaledToWidth(50),
    "GD": QImage('Resources/Images/GD.png').scaledToWidth(50),

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