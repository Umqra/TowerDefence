from PyQt4.QtGui import QWidget, QPainter, QImage, QPixmap
from Model.warriors import SimpleWarrior, AdamantWarrior

__author__ = 'umqra'


def get_warrior_view(model):
    if isinstance(model, SimpleWarrior):
        return SimpleWarriorView(model)
    if isinstance(model, AdamantWarrior):
        return AdamantWarriorView(model)
    raise ValueError


class WarriorView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.state = 0
        self.model = model

    def paintEvent(self, QPaintEvent):
        pass


class SimpleWarriorView(WarriorView):
    images = [
        QImage('Resources/Images/warrior_0').scaledToWidth(30),
        QImage('Resources/Images/warrior_0').scaledToWidth(30),
        QImage('Resources/Images/warrior_0').scaledToWidth(30),
        QImage('Resources/Images/warrior_1').scaledToWidth(30),
        QImage('Resources/Images/warrior_1').scaledToWidth(30),
        QImage('Resources/Images/warrior_1').scaledToWidth(30),
        QImage('Resources/Images/warrior_2').scaledToWidth(30),
        QImage('Resources/Images/warrior_2').scaledToWidth(30),
        QImage('Resources/Images/warrior_2').scaledToWidth(30),
        QImage('Resources/Images/warrior_3').scaledToWidth(30),
        QImage('Resources/Images/warrior_3').scaledToWidth(30),
        QImage('Resources/Images/warrior_3').scaledToWidth(30),
    ]
    count_states = 12

    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        if not self.model.is_alive:
            self.close()
        qp = QPainter()
        qp.begin(self)
        pixmap = QPixmap(SimpleWarriorView.images[self.state])
        bbox = self.model.shape.get_bounding_box()
        qp.drawPixmap(bbox[0].x, bbox[0].y, pixmap)
        self.state = (self.state + 1) % SimpleWarriorView.count_states


class AdamantWarriorView(WarriorView):
    images = [
        QImage('Resources/Images/adamant_warrior').scaledToWidth(30),
    ]
    count_states = 1

    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        if not self.model.is_alive:
            self.close()
        qp = QPainter()
        qp.begin(self)
        pixmap = QPixmap(AdamantWarriorView.images[self.state])
        bbox = self.model.shape.get_bounding_box()
        qp.drawPixmap(bbox[0].x, bbox[0].y, pixmap)
        self.state = (self.state + 1) % AdamantWarriorView.count_states