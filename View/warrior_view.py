from PyQt4.QtGui import QWidget, QPainter
from Model.warriors import SimpleWarrior

__author__ = 'umqra'

def get_warrior_view(model):
    if isinstance(model, SimpleWarrior):
        return SimpleWarriorView(model)
    raise ValueError

class WarriorView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def paintEvent(self, QPaintEvent):
        pass


class SimpleWarriorView(WarriorView):
    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        center = self.model.shape.get_center_of_mass()
        size = 20
        x = int(center.x - size / 2)
        y = int(center.y - size / 2)
        qp.drawEllipse(x, y, size, size)