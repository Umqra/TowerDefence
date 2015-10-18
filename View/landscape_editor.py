from PyQt4.QtGui import QWidget, QGridLayout, QLabel
from Controller.controller_events import ChooseLandscapeEvent
from Model.map_cell import cells_dict
from View.cells_view import create_cell_view

__author__ = 'umqra'

cell_names = {
    'W': "Water",
    "R": "Road",
    "G": "Grass",
    "F": "Forest"
}


class LandscapeCellView(QWidget):
    def __init__(self, state, cell):
        super().__init__()
        self.layout = QGridLayout()
        self.model = cells_dict[cell](state, 0, 0, cell + "1")
        self.cell_view = create_cell_view(self.model)
        self.layout.addWidget(self.cell_view, 0, 0)
        self.layout.addWidget(QLabel(cell_names[cell]), 1, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

    def mousePressEvent(self, e):
        self.model.state.controller.handle_event(ChooseLandscapeEvent(e, self.model))


class LandscapeEditorView(QWidget):
    def __init__(self, state, cells):
        super().__init__()
        self.state = state
        self.cells = cells
        self.layout = QGridLayout()
        for i, cell in enumerate(cells):
            self.layout.addWidget(LandscapeCellView(state, cell), 0, i)
        self.layout.setRowStretch(1, 1)
        self.setLayout(self.layout)
