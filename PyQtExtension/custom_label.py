from PyQt4.QtGui import QLabel, QFontDatabase, QFont

__author__ = 'umqra'


class CustomLambdaLabel(QLabel):
    def __init__(self, getter):
        super().__init__()
        self.setFont(QFont('BACKTO1982'))
        self.setMargin(5)
        self.getter = getter

    def paintEvent(self, QPaintEvent):
        self.setText(self.getter())
        super().paintEvent(QPaintEvent)


class CustomLabel(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFont(QFont('BACKTO1982'))
        self.setMargin(5)