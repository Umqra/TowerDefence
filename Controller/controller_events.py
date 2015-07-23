__author__ = 'umqra'


class ControllerEvent:
    def __init__(self, mouse_event):
        self.mouse_event = mouse_event


class MapControllerEvent(ControllerEvent):
    def __init__(self, mouse_event):
        super().__init__(mouse_event)


class StoreControllerEvent(ControllerEvent):
    def __init__(self, mouse_event, selected_item):
        super().__init__(mouse_event)
        self.selected_item = selected_item