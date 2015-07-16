import itertools
from Model.events import *

__author__ = 'umqra'

from PyQt4.QtGui import QWidget, QPainter, QColor, QGridLayout
from View.tower_view import get_tower_view
from View.bullet_view import get_bullet_view


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
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.init_details()

    def add_bullet(self, bullet_view):
        self.layout.addWidget(bullet_view, 0, 0)
        self.bullets_view.append(bullet_view)

    def add_tower(self, tower_view):
        self.layout.addWidget(tower_view, 0, 0)
        self.towers_view.append(tower_view)

    def add_warrior(self, warrior_view):
        self.layout.addWidget(warrior_view, 0, 0)
        self.warriors_view.append(warrior_view)

    def add_spell(self, spell_view):
        self.layout.addWidget(spell_view, 0, 0)
        self.spells_view.append(spell_view)

    def init_details(self):
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

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        for x in range(self.model.height):
            for y in range(self.model.width):
                value = int(self.model.map[x][y].lighting.value)
                qp.fillRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size,
                            QColor.fromRgb(value, value, value))
                qp.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

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