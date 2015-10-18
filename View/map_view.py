import itertools
from Controller.controller_events import MapControllerEvent
from Model.events import *
from View.custom_layout import CustomLayout
from View.gate_view import GateView
from View.warrior_view import get_warrior_view

__author__ = 'umqra'

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QPainter, QColor, QGridLayout, QStackedLayout, QPen, QGraphicsScene
from View.tower_view import get_tower_view
from View.bullet_view import get_bullet_view
from View.cells_view import LightView, CellsView


class MapView(QWidget):
    def __init__(self, model, cell_size=50):
        super().__init__()
        model.views.append(self)
        self.setMaximumWidth(cell_size * model.width)
        self.setMaximumHeight(cell_size * model.height)

        self.model = model
        self.cell_size = cell_size
        self.bullets_view = []
        self.warriors_view = []
        self.towers_view = []
        self.spells_view = []
        self.gates_view = []
        self.previews = []
        self.layout = CustomLayout()
        self.setLayout(self.layout)

        self.init_details()

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

    def add_gate(self, gate):
        self.layout.add_on_top(gate)
        self.gates_view.append(gate)

    def init_details(self):
        light_view = LightView(self.model, self.cell_size)
        cells_view = CellsView(self.model, self.cell_size)

        self.layout.add_on_top(light_view)
        self.layout.add_on_bottom(cells_view)
        for tower in self.model.towers:
            view = get_tower_view(tower)
            self.add_tower(view)
        for warrior in self.model.warriors:
            view = get_warrior_view(warrior)
            print(view)
            self.add_warrior(view)
        for bullet in self.model.bullets:
            view = get_bullet_view(bullet)
            self.add_bullet(view)
        for gate in self.model.gates:
            view = GateView(gate)
            self.add_gate(view)
#        for spell in self.model.spells:
#            self.add_spell(spell)

    def create_view_from_event(self, event):
        if isinstance(event, CreateTowerEvent):
            self.add_tower(get_tower_view(event.item))
        elif isinstance(event, CreateBulletEvent):
            self.add_bullet(get_bullet_view(event.item))
        elif isinstance(event, CreateWarriorEvent):
            self.add_warrior(get_warrior_view(event.item))
        elif isinstance(event, CreateSpellEvent):
            pass
        elif isinstance(event, CreatePreviewEvent):
            self.add_preview(get_tower_view(event.item))
        elif isinstance(event, CreateGateEvent):
            self.add_gate(GateView(event.item))

    def process_events(self, events):
        for event in events:
            if isinstance(event, CreateEvent):
                self.create_view_from_event(event)
            elif isinstance(event, DeleteWarriorEvent):
                for warrior in self.warriors_view:
                    if warrior.model == event.item:
                        warrior.close()
                        self.warriors_view.remove(warrior)
                        break
            elif isinstance(event, DeletePreviewEvent):
                for preview in self.previews:
                    if preview.model == event.item:
                        preview.close()
                        self.previews.remove(preview)
                        break

    def mousePressEvent(self, e):
        self.model.controller.handle_event(MapControllerEvent(e))

    def mouseMoveEvent(self, e):
        self.model.controller.handle_event(MapControllerEvent(e))
