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

    def unselect(self):
        self.selected_item = None

    def select(self, x, y):
        if self.selected_item is not None:
            pass
        else:
            items = self.model.get_items_at_position(x, y)
            for priority_class in items_priority:
                for item in items:
                    if isinstance(item, priority_class):
                        self.selected_item = item
                        item.select()
                        return