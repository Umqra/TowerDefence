from PyQt4 import Qt
from PyQt4.QtGui import QPixmap, QImage, QPicture, QColor, QPen, QFont, QFontDatabase
from PyQt4.QtGui import QPainter

__author__ = 'umqra'

path_to_images = "Resources/Images/"
QFontDatabase.addApplicationFont('Resources/Fonts/BACKTO1982.TTF')

def get_default_image(text, width=50, height=50):
    picture = QImage(width, height, QImage.Format_RGB32)
    picture.fill(QColor.fromRgb(200, 200, 200))
    painter = QPainter()
    painter.begin(picture)
    pen = QPen()
    pen.setWidth(1)
    painter.setPen(pen)
    for i in range(0, len(text), 6):
        painter.drawText(3, 13 * (i // 6 + 1), text[i:i+6])
    painter.end()
    return picture


def load_image(image_name, scale_width):
    path = path_to_images + image_name
    image = QImage(path)
    if image.isNull():
        return get_default_image(image_name, scale_width, scale_width)
    return image.scaledToWidth(scale_width)

def load_animation(prefix_name, scale_width, states):
    images = []
    for number in states:
        name = prefix_name + str(number)
        images.append(load_image(name, scale_width))
    return images
