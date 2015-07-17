from PyQt4.QtGui import QLayout, QWidget, QStackedLayout

__author__ = 'umqra'


class _WidgetForLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QStackedLayout()
        self.layout.setStackingMode(QStackedLayout.StackAll)
        self.setLayout(self.layout)


class CustomLayout(QStackedLayout):
    def __init__(self):
        super().__init__()
        self.setStackingMode(QStackedLayout.StackAll)
        self.insertWidget(0, _WidgetForLayout())

    def add_on_top(self, widget):
        self.widget(0).layout.insertWidget(-1, widget)

    def add_on_bottom(self, widget):
        self.insertWidget(-1, widget)