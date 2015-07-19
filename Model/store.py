__author__ = 'umqra'


class Store:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def add_items(self, new_items):
        self.items += new_items

    def remove_item(self, item):
        self.items.remove(item)


class StoreItem:
    def __init__(self, title, item_type, cost, description):
        self.title = title
        self.item_type = item_type
        self.cost = cost
        self.description = description