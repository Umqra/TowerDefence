from Controller.controller_events import MapCreatorControllerEvent, StoreControllerEvent, ChooseLandscapeEvent
from PyQt4 import QtCore
from Geometry.point import Point
from Model.map_cell import MapCell

__author__ = 'umqra'


class CreatorController:
    def __init__(self, state):
        self.state = state
        self.selected_item = None

    def try_put_selected_item_on_map(self, x, y):
        y, x = self.state.map.get_cell_coordinates(x, y)
        print("try {} {}".format(x, y))
        if self.selected_item is not None and isinstance(self.selected_item, MapCell):
            self.state.map.set_cell_type(x, y, self.selected_item.get_view_repr() + "1")
            print(self.selected_item.get_view_repr())


    def handle_map_event(self, event):
        if event.mouse_event.type() == QtCore.QEvent.MouseButtonPress:
            if event.mouse_event.buttons() == QtCore.Qt.LeftButton:
                self.try_put_selected_item_on_map(event.mouse_event.x(), event.mouse_event.y())

    def handle_store_event(self, event):
        pass

    def handle_choose_landscape_event(self, event):
        self.selected_item = event.cell
        print("select {}".format(event.cell))

    def handle_event(self, event):
        if isinstance(event, MapCreatorControllerEvent):
            self.handle_map_event(event)
        if isinstance(event, ChooseLandscapeEvent):
            self.handle_choose_landscape_event(event)