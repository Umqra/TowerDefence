from PyQt4.QtGui import QWidget, QSlider, QGridLayout, QColor

from PyQt4.QtCore import Qt
from PyQtExtension.custom_button import CustomButton
from PyQtExtension.custom_label import CustomLambdaLabel
from PyQtExtension.loader_widget import LoaderWidget, LoaderType, LoaderStyle
from View.waves_info_view import WavesInfoView


__author__ = 'umqra'


class CreatorControlPanelView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.layout = QGridLayout()
        self.money_slider = QSlider(Qt.Horizontal, self)
        self.money_slider.valueChanged.connect(self.change_money)
        self.money_label = CustomLambdaLabel(lambda: "Money: {}".format(self.model.money))

        self.waves_info = WavesInfoView(model)

        self.setLayout(self.layout)
        self.layout.addWidget(self.money_label, 0, 0)
        self.layout.addWidget(self.money_slider, 1, 0)
        self.layout.addWidget(self.waves_info, 3, 0)

        self.layout.setRowStretch(10, 1)

    def change_money(self, value):
        value = int(value) * 50
        self.model.money = value
        self.money_label.update()

