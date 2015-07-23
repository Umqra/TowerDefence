__author__ = 'umqra'


class Store:
    def __init__(self, items=None):
        self.items = items if items is not None else []
        self.controller = None

    def add_item(self, item):
        self.items.append(item)

    def add_items(self, new_items):
        self.items += new_items

    def remove_item(self, item):
        self.items.remove(item)

    def set_controller(self, controller):
        for item in self.items:
            item.set_controller(controller)
        self.controller = controller


class StoreItem:
    def __init__(self, title, item_type, cost, description):
        self.title = title
        self.item_type = item_type
        self.cost = cost
        self.description = description

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller