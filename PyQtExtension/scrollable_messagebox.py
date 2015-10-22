from PyQt4.QtGui import QMessageBox, QLabel, QScrollArea, QVBoxLayout
from PyQt4.QtCore import Qt

__author__ = 'umqra'


class ScrollableMessageBox(QMessageBox):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.container = QLabel()
        self.container.setWordWrap(True)
        self.scroller = QScrollArea()
        self.scroller.setMinimumHeight(400)
        self.scroller.setMinimumWidth(500)
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.container)
        self.layout().addWidget(self.scroller, 0, 0)
        self.layout().setColumnStretch(1, 1)

    def setText(self, p_str):
        self.container.setText(p_str)
