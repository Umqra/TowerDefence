from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QGridLayout, QWidget, QLabel, QLineEdit, QPixmap, QSpinBox
from Controller.controller_events import GetGatesForWaveControllerEvent
from Geometry.point import Point
from Model.time import Time
from Model.warriors import list_warriors
from Model.wave import Wave, Gate
from PyQtExtension.custom_button import CustomButton
from PyQtExtension.custom_label import CustomLambdaLabel, CustomLabel
from View.warrior_view import get_warrior_view

__author__ = 'umqra'


class ChooseTimeView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.day_edit = QSpinBox()

        self.hour_edit = QSpinBox()
        self.hour_edit.setRange(0, 23)

        self.minute_edit = QSpinBox()
        self.minute_edit.setRange(0, 59)

        self.second_edit = QSpinBox()
        self.second_edit.setRange(0, 59)

        self.layout.addWidget(CustomLabel("Day"), 0, 0)
        self.layout.addWidget(CustomLabel("Hour"), 0, 1)
        self.layout.addWidget(CustomLabel("Minutes"), 0, 2)
        self.layout.addWidget(CustomLabel("Seconds"), 0, 3)

        self.layout.addWidget(self.day_edit, 1, 0)
        self.layout.addWidget(self.hour_edit, 1, 1)
        self.layout.addWidget(self.minute_edit, 1, 2)
        self.layout.addWidget(self.second_edit, 1, 3)

        self.setLayout(self.layout)

    def get_time(self):
        return Time.fromDHMS(self.day_edit.value(),
                             self.hour_edit.value(),
                             self.minute_edit.value(),
                             self.second_edit.value())


class ChooseWarriorsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.order = []
        self.count_warriors = []
        for index, warrior in enumerate(list_warriors):
            self.order.append(warrior)
            view = get_warrior_view(warrior(Point(0, 0))).images[0]
            view_label = QLabel()
            view_label.setPixmap(QPixmap(view))
            self.layout.addWidget(view_label, 0, index)
            count_warrior = QSpinBox()
            count_warrior.setRange(0, 5)
            self.count_warriors.append(count_warrior)
            self.layout.addWidget(count_warrior, 1, index)
        self.layout.setColumnStretch(10, 1)
        self.setLayout(self.layout)

    def get_warriors(self):
        warriors = []
        for warrior, count_warrior in zip(self.order, self.count_warriors):
            cnt = count_warrior.value()
            warriors.extend([warrior] * cnt)
        return warriors


class CreateNewWaveDialog(QDialog):
    def __init__(self, model, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.wave = Wave(model, None, [], [])
        self.model = model
        self.setWindowModality(Qt.WindowModal)

        self.step_id = 0
        self.layout = QGridLayout()
        self.header_text = "Step 1: Choose gates for warriors"
        self.header_label = CustomLambdaLabel(lambda: self.header_text)

        self.next_step_button = CustomButton("Next step")
        self.next_step_button.clicked.connect(self.next_step)

        self.support_widget = CustomLabel("Just choose it on map")

        self.layout.addWidget(self.header_label, 0, 0)
        self.layout.addWidget(self.support_widget, 1, 0)
        self.layout.addWidget(self.next_step_button, 2, 0)
        self.setLayout(self.layout)

    def grad_step_info(self):
        if self.step_id == 0:
            self.model.controller.handle_event(GetGatesForWaveControllerEvent(self))
            return self.wave.gates
        elif self.step_id == 1:
            self.wave.warriors = self.support_widget.get_warriors()
            return self.wave.warriors
        elif self.step_id == 2:
            self.wave.start_time = self.support_widget.get_time()
            self.parent_window.add_wave(self.wave)
        return True

    def next_step(self):
        if not self.grad_step_info():
            return
        self.layout.removeWidget(self.support_widget)
        self.support_widget.close()
        if self.step_id == 0:
            self.support_widget = ChooseWarriorsView()
            self.layout.addWidget(self.support_widget, 1, 0)
            self.header_text = "Step 2: Fix count of warriors"
            self.header_label.update()
        elif self.step_id == 1:
            self.support_widget = ChooseTimeView()
            self.layout.addWidget(self.support_widget, 1, 0)
            self.header_text = "Step 3: Choose time"
            self.header_label.update()
            self.next_step_button.setText("Add new wave")
        elif self.step_id == 2:
            self.close()
        self.step_id += 1

    def accept_gates(self, list_items):
        for gate in filter(lambda x: isinstance(x, Gate), list_items):
            self.wave.gates.append(gate)

