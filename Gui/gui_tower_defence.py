from Controller.creator_controller import CreatorController
from Gui import start_gui
from Infrastructure.pyqt_helpers import clear_layout
from View.creator_view import CreatorView

__author__ = 'umqra'
from PyQt4.QtGui import QGridLayout
from Model.game_state import GameState
from View.state_view import StateView
from PyQt4 import QtGui, QtCore


class Game(QtGui.QWidget):
    fps = 40
    interval = 1000. / fps

    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 800)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.state = None
        self.state_view = None
        # self.load_level(Level1)
        self.load_level_creator()

        self.timer = QtCore.QBasicTimer()
        self.timer.start(Game.interval, self)

    def load_level(self, level_loader):
        self.reset_game()
        self.state = GameState(self)
        self.state.initialize_with_loader(level_loader)
        self.state_view = StateView(self.state)
        self.layout.addWidget(self.state_view)

        self.setMouseTracking(True)

    def load_level_creator(self):
        self.reset_game()
        self.state = GameState(self)
        self.state.initialize_empty_level()
        self.state.set_controller(CreatorController(self.state))
        self.state_view = CreatorView(self.state)
        self.layout.addWidget(self.state_view)

        self.setMouseTracking(True)

    def reset_game(self):
        clear_layout(self.layout)

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QtCore.QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QtGui.QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def timerEvent(self, e):
        if self.state.pause:
            return
        self.state.tick(Game.interval / 1000)
        self.repaint()


def run():
    widget = Game()
    widget.show()
    start_gui.app.exec_()