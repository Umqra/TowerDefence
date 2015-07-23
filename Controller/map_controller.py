__author__ = 'umqra'
from Model import bullets, towers

items_priority = [
    towers.Tower,
    bullets.Bullet,
]


class MapController:
    def __init__(self, model):
        self.model = model
        self.selected_item = None

    def handle_event(self, event):
        pass