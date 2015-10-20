from PyQt4.QtGui import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QPixmap, QLabel, QDialog, QMainWindow
from PyQt4.QtCore import Qt
from Controller.controller_events import StartCreateNewWaveControllerEvent, GetGatesForWaveControllerEvent
from Geometry.point import Point
from Model.time import Time
from Model.warriors import AdamantWarrior
from Model.wave import Gate, Wave
from PyQtExtension.custom_button import CustomButton
from PyQtExtension.custom_label import CustomLambdaLabel, CustomLabel
from View.create_new_wave_view import CreateNewWaveDialog
from View.warrior_view import get_warrior_view

__author__ = 'umqra'


class WarriorWaveInfoView(QWidget):
    def __init__(self, warrior, cnt):
        super().__init__()
        self.warrior = warrior
        self.cnt = cnt
        self.layout = QGridLayout()
        view = get_warrior_view(warrior(Point(0, 0))).images[0]
        self.pixmap = QPixmap(view)
        self.pixmap_label = QLabel()
        self.pixmap_label.setPixmap(self.pixmap)
        self.count_label = CustomLabel("x{}".format(self.cnt))
        self.layout.addWidget(self.pixmap_label)
        self.layout.addWidget(self.count_label, 0, 1)
        self.setLayout(self.layout)


class WaveInfoView(QWidget):
    def __init__(self, wave):
        super().__init__()
        self.wave = wave
        self.setFixedHeight(100)
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.time_label = CustomLabel(str(wave.start_time))

        self.layout.addWidget(self.time_label, 0, 0, 1, 0)
        compressed_warriors = map(lambda x: (x[1], wave.warriors.count(x[1])),
                                  filter(lambda x: wave.warriors.index(x[1]) == x[0],
                                         enumerate(wave.warriors)))
        for idx, warrior in enumerate(compressed_warriors):
            self.layout.addWidget(WarriorWaveInfoView(warrior[0], warrior[1]), 1, idx)
        self.layout.setColumnStretch(10, 1)
        self.setLayout(self.layout)


class WavesInfoView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.setFixedHeight(400)
        self.waves = model.waves
        self.model = model

        self.delete_button = CustomButton("Delete last")
        self.delete_button.clicked.connect(self.delete_last)

        self.create_button = CustomButton("Create wave")
        self.create_button.clicked.connect(self.create_wave)

        self.count_label = CustomLambdaLabel(lambda: "Waves: {}".format(len(self.waves)))

        self.container_inner = []
        self.container = QWidget()
        self.container_layout = QGridLayout()

        self.container_layout.setRowStretch(10, 1)
        self.container.setLayout(self.container_layout)
        self.scroller = QScrollArea()
        for wave in self.waves:
            self.add_wave_view(wave)

        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.container)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.count_label)
        self.layout.addWidget(self.scroller)

        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.create_button)
        self.setLayout(self.layout)

    def delete_last(self):
        if not self.waves:
            return
        self.waves.pop()
        widget = self.container_inner.pop()
        widget.close()
        self.container_layout.removeWidget(widget)
        self.count_label.update()

    def create_wave(self):
        dialog = CreateNewWaveDialog(self.model, self)
        self.model.controller.handle_event(StartCreateNewWaveControllerEvent(dialog))
        dialog.exec_()

    def add_wave_view(self, wave):
        widget = WaveInfoView(wave)
        self.container_layout.addWidget(widget, len(self.container_inner), 0)
        self.container_inner.append(widget)

    def add_wave(self, wave):
        self.waves.append(wave)
        self.add_wave_view(wave)