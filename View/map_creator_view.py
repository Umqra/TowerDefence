from PyQt4.QtGui import QWidget
from Controller.controller_events import MapCreatorControllerEvent
from Infrastructure.pyqt_helpers import clear_layout
from Model.events import CreatePreviewEvent, CreateEvent, DeletePreviewEvent
from Model.events import CreateTowerEvent
from View.cells_view import LightView, CellsView
from View.custom_layout import CustomLayout
from View.tower_view import get_tower_view
from PyQt4 import QtGui, QtCore

__author__ = 'umqra'


class MapCreatorView(QWidget):
    interval = 100
    def __init__(self, model, cell_size=50):
        super().__init__()
        model.views.append(self)
        self.setMaximumWidth(cell_size * model.width)
        self.setMaximumHeight(cell_size * model.height)

        self.model = model
        self.model.add_view(self)
        self.cell_size = cell_size
        self.towers_view = []
        self.previews = []

        self.layout = CustomLayout()
        self.setLayout(self.layout)

        self.init_details()

        self.timer = QtCore.QBasicTimer()
        self.timer.start(MapCreatorView.interval, self)

    def timerEvent(self, e):
        self.repaint()

    def get_cell_coordinates(self, x, y):
        return x // self.cell_size, y // self.cell_size

    def add_bullet(self, bullet_view):
        self.layout.add_on_top(bullet_view)
        self.bullets_view.append(bullet_view)

    def add_tower(self, tower_view):
        self.layout.add_on_top(tower_view)
        self.towers_view.append(tower_view)

    def add_warrior(self, warrior_view):
        self.layout.add_on_top(warrior_view)
        self.warriors_view.append(warrior_view)

    def add_spell(self, spell_view):
        self.layout.add_on_top(spell_view)
        self.spells_view.append(spell_view)

    def add_preview(self, preview):
        self.layout.add_on_top(preview)
        self.previews.append(preview)

    def update(self):
        self.light_view.update()
        self.cells_view.update()

    def reset_map(self):
        clear_layout(self.layout)

    def init_details(self):
        self.light_view = LightView(self.model, self.cell_size)
        self.cells_view = CellsView(self.model, self.cell_size)

        self.layout.add_on_top(self.light_view)
        self.layout.add_on_bottom(self.cells_view)
        for tower in self.model.towers:
            view = get_tower_view(tower)
            self.add_tower(view)
#        for spell in self.model.spells:
#            self.add_spell(spell)

    def create_view_from_event(self, event):
        if isinstance(event, CreateTowerEvent):
            self.add_tower(get_tower_view(event.item))
        elif isinstance(event, CreatePreviewEvent):
            self.add_preview(get_tower_view(event.item))

    def process_events(self, events):
        for event in events:
            if isinstance(event, CreateEvent):
                self.create_view_from_event(event)
            elif isinstance(event, DeletePreviewEvent):
                for preview in self.previews:
                    if preview.model == event.item:
                        preview.close()
                        self.previews.remove(preview)
                        break

    def mousePressEvent(self, e):
        self.model.controller.handle_event(MapCreatorControllerEvent(e))
