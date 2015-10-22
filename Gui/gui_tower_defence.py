import jsonpickle
import pickle
from PyQt4.QtCore import Qt
from Controller.creator_controller import CreatorController
from Controller.main_controller import MainController
from Gui import start_gui
from Infrastructure.pyqt_helpers import clear_layout
from Model.level_loader import load_level_from_file, get_level_loader, levels
from Model.time import Time
from Model.warriors import BFSWalker
from PyQtExtension.scrollable_messagebox import ScrollableMessageBox
from View.creator_view import CreatorView

__author__ = 'umqra'
from PyQt4.QtGui import QGridLayout, QMenuBar, QVBoxLayout, QMenu, QShortcut, QKeySequence, QMessageBox, QFileDialog
from Model.game_state import GameState
from View.state_view import StateView
from PyQt4 import QtGui, QtCore

markdown_exist = False
try:
    import markdown
    markdown_exist = True
except ImportError:
    markdown_exist = False


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
        # self.load_level_from_file('level_1.tdl')
        self.last_level = levels[0]
        self.load_level(levels[0])

        # self.load_level_creator()

        self.timer = QtCore.QBasicTimer()
        self.timer.start(Game.interval, self)

        self.menu_bar = QMenuBar(self)
        self.menu_bar.setMinimumWidth(self.width())
        game_menu = self.menu_bar.addMenu("Game")
        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction("Help topics", self.load_help)
        help_menu.addAction("About", self.show_about)

        game_menu.addAction('Create level', self.load_level_creator)
        game_menu.addAction('Load from file', self.load_level_from_file_dialog)
        game_menu.addAction('Start game', lambda: self.load_level(self.last_level))
        game_menu.addAction('Pause game', lambda: self.state.stop())
        game_menu.addAction('Run game', lambda: self.state.resume())
        game_menu.addAction('Exit', lambda: self.close())

        self.layout.setRowMinimumHeight(0, 20)

    def load_level_from_file_dialog(self):
        file_name = QFileDialog().getOpenFileName(self, 'Load level', '~')
        self.load_level_from_file(file_name)

    def show_about(self):
        about = QMessageBox.about(self, 'About game', 'Tower defence\nUrFU 2015')

    def load_help(self):
        help_info = 'Help info unavailable'
        with open('README.md') as f:
            help_info = f.read()
            if markdown_exist:
                help_info = markdown.markdown(help_info)
            else:
                help_info = 'Markdown unavailable.\nYou can install it with command: pip install markdown\n' + help_info
        x = ScrollableMessageBox(self)
        x.setText(help_info)
        x.setWindowTitle('Help')
        x.show()
        # help = QMessageBox.about(self, 'Help', help_info)

    def load_level_from_file(self, file_name):
        self.reset_game()
        self.state = load_level_from_file(file_name)
        self.state_view = StateView(self.state)
        self.layout.addWidget(self.state_view, 1, 0)

        self.setMouseTracking(True)

    def load_level(self, level_loader):
        self.last_level = level_loader
        self.reset_game()
        self.state = GameState(self)
        self.state.initialize_with_loader(level_loader)
        self.state_view = StateView(self.state)
        self.layout.addWidget(self.state_view, 1, 0)

        self.setMouseTracking(True)

    def load_level_creator(self):
        self.reset_game()
        self.state = GameState(self)
        self.state.initialize_empty_level()
        self.state.set_controller(CreatorController(self.state))
        self.state_view = CreatorView(self.state)
        self.layout.addWidget(self.state_view, 1, 0)

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