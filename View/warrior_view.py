from PyQt4.QtGui import QWidget, QPainter, QImage, QPixmap, QPen, QColor, QBrush
from PyQt4.QtCore import QRect
from Infrastructure.get_resources import load_image, load_animation
from Model.warriors import SimpleWarrior, AdamantWarrior

__author__ = 'umqra'


def get_warrior_view(model):
    if isinstance(model, SimpleWarrior):
        return SimpleWarriorView(model)
    if isinstance(model, AdamantWarrior):
        return AdamantWarriorView(model)
    raise ValueError

def get_color_depends_on_damage(damage):
    red_factor = 1
    green_factor = 10 ** damage
    blue_factor = 100 ** (10 * damage)
    print(red_factor, green_factor, blue_factor)
    return QColor.fromRgb(255 / red_factor, 255 / green_factor, 255 / blue_factor)

def draw_info_arc(qp, model):
    bbox = model.shape.get_bounding_box()
    spacing = 2
    arc_rectangle = QRect(bbox[0].x - spacing, bbox[0].y - spacing,
                          bbox[1].x - bbox[0].x + 2 * spacing, bbox[1].y - bbox[0].y + 2 * spacing)
    ratio = model.health / 100.

    # NOTE: 16 because of 16-th part of degrees in PyQt::drawArc
    left_arc = int((90 - 180 * ratio) * 16)
    len_arc = int(360 * ratio * 16)
    damage_color = get_color_depends_on_damage(model.damage)
    pen = QPen(QBrush(damage_color), 3)
    qp.setPen(pen)
    qp.drawArc(arc_rectangle, left_arc, len_arc)

class WarriorView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.state = 0
        self.model = model

    def paintEvent(self, QPaintEvent):
        if not self.model.is_alive:
            self.close()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)

        pixmap = QPixmap(self.images[self.state])
        bbox = self.model.shape.get_bounding_box()
        qp.drawPixmap(bbox[0].x, bbox[0].y, pixmap)

        draw_info_arc(qp, self.model)


class SimpleWarriorView(WarriorView):
    images = load_animation("warrior_", 30, [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
    count_states = 12

    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        self.state = (self.state + 1) % SimpleWarriorView.count_states


class AdamantWarriorView(WarriorView):
    images = [load_image("adamant_warrior", 30)]
    count_states = 1

    def __init__(self, model):
        super().__init__(model)

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        self.state = (self.state + 1) % AdamantWarriorView.count_states