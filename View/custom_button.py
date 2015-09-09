from PyQt4.QtGui import QPushButton, QFontDatabase, QFont
from PyQt4 import QtCore

__author__ = 'umqra'


class CustomButton(QPushButton):
    stylesheet = """
    QPushButton {border: 2px solid gray; background-color:white; padding: 8px;}
    QPushButton:hover {border: 2px solid black; background-color:white; padding: 8px;}
    """

    def __init__(self, text):
        super().__init__(text)
        print(CustomButton.stylesheet)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet(CustomButton.stylesheet)
        QFontDatabase.addApplicationFont('Resources/Fonts/BACKTO1982.TTF')
        self.setFont(QFont('BACKTO1982'))



