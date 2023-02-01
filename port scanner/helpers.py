from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget,QLabel,QGridLayout,QVBoxLayout


class Color(QWidget):
    def __init__(self,color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor(color))
        self.setPalette(palette)
        self.setMaximumSize(QSize(200,20))

class Label(QLabel):
    def __init__(self,text = ""):
        super().__init__(text)
        self.setMaximumSize(QSize(200,20))
        self.setAutoFillBackground(True)
        plt = self.palette()
        plt.setColor(QPalette.ColorRole.Window,QColor("gray"))
        self.setPalette(plt)

