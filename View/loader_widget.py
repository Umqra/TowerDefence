from PyQt4.QtGui import QWidget, QPainter, QGridLayout, QLabel

__author__ = 'umqra'


class LoaderStyle:
    def __init__(self, height, title, background_color, foreground_color, border_color):
        self.height = height
        self.title = title
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.border_color = border_color

    def apply_to_loader(self, loader):
        stylesheet = "QLabel#parent {{border: 1px solid rgb{}; background-color: rgb{};}}". \
            format(self.border_color.getRgb(), self.background_color.getRgb())
        print(stylesheet)
        loader.setStyleSheet(stylesheet)


class LoaderWidget(QLabel):
    def __init__(self, getter, min_value, max_value, style_info):
        super().__init__()
        self.setObjectName("parent")
        self.setFixedHeight(style_info.height)
        style_info.apply_to_loader(self)
        self.layout = QGridLayout()
        self.layout.setVerticalSpacing(0)

        label_widget = LoaderLabel("{} : {{}} / {}".format(style_info.title, max_value), getter)
        strip_widget = LoaderStrip(getter, min_value, max_value, style_info.foreground_color)

        self.layout.addWidget(label_widget, 0, 0)
        self.layout.addWidget(strip_widget, 1, 0)
        self.setLayout(self.layout)


class LoaderLabel(QLabel):
    def __init__(self, format, getter):
        super().__init__()
        self.format = format
        self.getter = getter

    def paintEvent(self, QPaintEvent):
        self.setText(self.format.format(self.getter()))
        super().paintEvent(QPaintEvent)


class LoaderStrip(QWidget):
    def __init__(self, getter, min_value, max_value, color):
        super().__init__()
        self.getter = getter
        self.min_value = min_value
        self.max_value = max_value
        self.color = color

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        percentage = (self.getter() - self.min_value) / self.max_value
        qp.fillRect(0, 0, int(self.width() * percentage), self.height(), self.color)


