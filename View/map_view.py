import itertools
from Model.events import *

__author__ = 'umqra'

from PyQt4.QtGui import QWidget, QPainter, QColor, QGridLayout, QStackedLayout
from View.tower_view import get_tower_view
from View.bullet_view import get_bullet_view
from View.cells_view import LightView, CellsView


class MapView(QWidget):
    def __init__(self, model, cell_size=50):
        super().__init__()
        model.views.append(self)
        self.model = model
        self.cell_size = cell_size
        self.bullets_view = []
        self.warriors_view = []
        self.towers_view = []
        self.spells_view = []
        self.layout = QStackedLayout()
        self.layout.setStackingMode(QStackedLayout.StackAll)
        self.setLayout(self.layout)

        self.init_details()

    def add_bullet(self, bullet_view):
        self.layout.insertWidget(0, bullet_view)
        self.bullets_view.append(bullet_view)

    def add_tower(self, tower_view):
        print(self.layout.insertWidget(2, tower_view))
        self.towers_view.append(tower_view)

    def add_warrior(self, warrior_view):
        self.layout.insertWidget(0, warrior_view)
        self.warriors_view.append(warrior_view)

    def add_spell(self, spell_view):
        self.layout.insertWidget(0, spell_view)
        self.spells_view.append(spell_view)

    def init_details(self):
        self.light_view = LightView(self.model, self.cell_size)
        self.cells_view = CellsView(self.model, self.cell_size)

        self.layout.insertWidget(0, self.light_view)
        for tower in self.model.towers:
            view = get_tower_view(tower)
            self.add_tower(view)
        for warrior in self.model.warriors:
            self.add_warrior(warrior)
        for bullet in self.model.bullets:
            view = get_bullet_view(bullet)
            self.add_bullet(view)
        for spell in self.model.spells:
            self.add_spell(spell)
        self.layout.insertWidget(0, self.cells_view)


    def create_view_from_event(self, event):
        if isinstance(event, CreateTowerEvent):
            self.add_tower(get_tower_view(event.item))
        elif isinstance(event, CreateBulletEvent):
            self.add_bullet(get_bullet_view(event.item))
        elif isinstance(event, CreateWarriorEvent):
            pass
        elif isinstance(event, CreateSpellEvent):
            pass

    def process_events(self, events):
        for event in events:
            if isinstance(event, CreateEvent):
                self.create_view_from_event(event)