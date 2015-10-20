from PyQt4.QtGui import QWidget, QPixmap
from Infrastructure.get_resources import load_image
from View.static_view import StaticObjectView

__author__ = 'umqra'


class GateView(StaticObjectView):
    image = load_image("gate.png", 50)

    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.pixmap = QPixmap(GateView.image)
