from PyQt4.QtGui import QWidget, QGridLayout, QColor
from Model.time import Time
from View.loader_widget import LoaderWidget, LoaderStyle, LoaderType

__author__ = 'umqra'


class InfoPanelView(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state

        self.layout = QGridLayout()
        self.layout.setRowStretch(0, 1)

        self.layout.addWidget(LoaderWidget(lambda: self.state.time.day, 0, 10,
                                           LoaderStyle(LoaderType.TextOnly, 60, "Day",
                                                       QColor.fromRgb(255, 255, 255),
                                                       QColor.fromRgb(41, 171, 135),
                                                       QColor.fromRgb(0, 0, 0))),
                              1, 0)

        self.layout.addWidget(
            LoaderWidget(lambda: int(self.state.time.value // self.state.time.seconds_in_hour()), 0, 24,
                         LoaderStyle(LoaderType.TextAndLoader, 60, "Hour",
                                     QColor.fromRgb(255, 255, 255),
                                     QColor.fromRgb(41, 171, 135),
                                     QColor.fromRgb(0, 0, 0))),
            2, 0)

        self.layout.addWidget(LoaderWidget(
            lambda: (self.state.waves[0].start_time - self.state.time).total_hours if self.state.waves else 0,
            0, 10,
            LoaderStyle(LoaderType.TextOnly, 60, "Hours to wave",
                        QColor.fromRgb(255, 255, 255),
                        QColor.fromRgb(41, 171, 135),
                        QColor.fromRgb(0, 0, 0))),
                              3, 0)

        self.layout.addWidget(LoaderWidget(lambda: len(self.state.waves), 0, len(self.state.waves),
                                           LoaderStyle(LoaderType.TextAndLoader, 60, "Wave",
                                                       QColor.fromRgb(255, 255, 255),
                                                       QColor.fromRgb(255, 77, 0),
                                                       QColor.fromRgb(0, 0, 0))),
                              4, 0)

        self.layout.addWidget(LoaderWidget(lambda: self.state.money, 0, 1000,
                                           LoaderStyle(LoaderType.TextOnly, 60, "Money",
                                                       QColor.fromRgb(255, 255, 255),
                                                       QColor.fromRgb(243, 218, 11),
                                                       QColor.fromRgb(0, 0, 0))),
                              5, 0)

        self.layout.setRowStretch(6, 1)
        self.setLayout(self.layout)