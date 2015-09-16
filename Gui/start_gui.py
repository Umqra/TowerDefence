from PyQt4.QtGui import QApplication
import sys

__author__ = 'umqra'

app = None


def start():
    global app
    app = QApplication(sys.argv)