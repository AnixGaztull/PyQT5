import sys
import random

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('проект.ui', self)

        self.count_misses = 0
        self.count_hits = 0

        self.name_player = str(self.input_name.text())
        self.add_datebase()

        self.buttons = QButtonGroup()
        for i in range(30):
            self.button = QPushButton(self)
            self.button.resize(15, 15)
            self.button.move(0, 0)
            self.button.setStyleSheet(
                'border-radius: 7px; background: rgb(255, 30, 0); border: 2px solid rgb(255, 0, 0)')
            self.button.hide()
            self.buttons.addButton(self.button)
            self.buttons.setId(self.button, i)

        self.start_btn.clicked.connect(self.start_game)
        self.f_btn.setStyleSheet('background: rgb(255, 255, 255); border: 2px solid rgb(255, 255, 255)')
        self.f_btn.clicked.connect(self.function_misses)

    def add_datebase(self):
        pass

    def start_game(self):
        self.count = 0
        self.make_btns()
        self.timer()

    def timer(self):
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

    def timerEvent(self):
        self.time = self.time.addSecs(1)
        self.timeForPlayer.setText(self.time.toString("hh:mm:ss"))

    def make_btns(self):
        coords = []
        for i in range(30):
            x = random.randrange(0, 430, 16)
            y = random.randrange(30, 570, 16)
            coord = (x, y)
            if coord not in coords:
                coords.append(coord)
            self.buttons.button(i).show()
            self.buttons.button(i).move(x, y)
        self.buttons.buttonClicked.connect(self.function_btn)

    def function_btn(self, this_button):
        this_button.hide()
        self.count_hits += 1
        self.count += 100
        self.hits.display(self.count_hits)
        self.rezult.display(self.count)

    def function_misses(self):
        self.count_misses += 1
        self.count -= 150
        self.misses.display(self.count_misses)
        self.rezult.display(self.count)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
