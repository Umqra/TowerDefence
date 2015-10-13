__author__ = 'umqra'


class ControllerEvent:
    def __init__(self, mouse_event):
        self.mouse_event = mouse_event


class MapControllerEvent(ControllerEvent):
    def __init__(self, mouse_event):
        super().__init__(mouse_event)


class StoreControllerEvent(ControllerEvent):
    def __init__(self, mouse_event, factory_for_items, store_info):
        super().__init__(mouse_event)
        self.factory_for_items = factory_for_items
        self.store_info = store_info