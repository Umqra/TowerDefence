__author__ = 'umqra'


class ControllerEvent:
    pass


class MouseControllerEvent(ControllerEvent):
    def __init__(self, mouse_event):
        self.mouse_event = mouse_event


class MapControllerEvent(MouseControllerEvent):
    def __init__(self, mouse_event):
        super().__init__(mouse_event)


class StoreControllerEvent(MouseControllerEvent):
    def __init__(self, mouse_event, factory_for_items, store_info):
        super().__init__(mouse_event)
        self.factory_for_items = factory_for_items
        self.store_info = store_info


class MapCreatorControllerEvent(MouseControllerEvent):
    def __init__(self, mouse_event):
        super().__init__(mouse_event)


class ChooseLandscapeEvent(MouseControllerEvent):
    def __init__(self, mouse_event, cell):
        super().__init__(mouse_event)
        self.cell = cell


class SelectItemControllerEvent(MouseControllerEvent):
    def __init__(self, mouse_event, item):
        super().__init__(mouse_event)
        self.item = item


class StartCreateNewWaveControllerEvent(ControllerEvent):
    def __init__(self, dialog):
        self.dialog = dialog

class GetGatesForWaveControllerEvent(ControllerEvent):
    def __init__(self, dialog):
        self.dialog = dialog