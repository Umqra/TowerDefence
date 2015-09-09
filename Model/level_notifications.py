__author__ = 'umqra'


class NotificationEvent:
    def __init__(self, predicat, notification):
        self.predicat = predicat
        self.notification = notification

    def can_run(self):
        return self.predicat()


class NotificationCreator:
    def __init__(self, state):
        self.state = state
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def tick(self, dt):
        for event in self.events:
            if event.can_run():
                self.state.push_notification(event.notification)
                continue