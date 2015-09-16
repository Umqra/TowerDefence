from PyQt4.QtGui import QLabel, QFontDatabase, QFont

__author__ = 'umqra'


class CustomLabel(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFont(QFont('BACKTO1982'))
        self.setMargin(5)