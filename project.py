import sys
import random
import sqlite3

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('проект.ui', self)

        self.start_btn.hide()
        self.name.hide()
        self.max_points.hide()
        self.enter_window.hide()
        self.registration_window.hide()

        self.open_database()
        self.names_players = list(map(lambda x: x[0], self.cur.execute("SELECT name FROM players_score").fetchall()))

        self.entrence.clicked.connect(self.enter_window_function)
        self.registration.clicked.connect(self.regist)

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

    def regist(self):
        self.registration_window.show()
        self.registr_btn.clicked.connect(self.registration_window_function)
        self.cancel_btn_enter_2.clicked.connect(self.cancel_registration)

    def registration_window_function(self):
        self.reg_password = str(self.input_password_reg.text())
        self.reg_name = str(self.name_input_reg.text())
        if self.reg_name not in self.names_players:
            self.window_name.setText('имя свободно')
            self.player_name = self.reg_name
            self.add_in_datebase(self.reg_name, self.reg_password)
            self.registration_window.hide()
            self.show_start()
        else:
            self.window_name.setText('имя занято')

    def show_start(self):
        self.entrence.hide()
        self.registration.hide()
        self.name.show()
        self.start_btn.show()
        self.max_points.show()
        self.name.setText(self.player_name)
        score = self.cur.execute(f"""SELECT score FROM players_score
                    WHERE name='{self.player_name}'""").fetchall()[0]
        self.max_points.setText(str(score[0]))

    def cancel_registration(self):
        self.registration_window.hide()

    def enter_window_function(self):
        self.enter_window.show()
        self.enter_btn.clicked.connect(self.enter)
        self.cancel_btn_enter.clicked.connect(self.cancel_enter)

    def cancel_enter(self):
        self.enter_window.hide()

    def enter(self):
        self.enter_name = str(self.name_input.text())
        self.enter_password = str(self.password.text())
        if self.enter_name in self.names_players:
            password = str(self.cur.execute(f"""SELECT password FROM players_score
                    WHERE name='{self.enter_name}'""").fetchall()[0][0])
            if password == self.enter_password:
                self.player_name = self.enter_name
                self.enter_window.hide()
                self.show_start()
            else:
                self.error_w.setText('неверный пароль')
        else:
            self.error_w.setText('неверное имя')

    def open_database(self):
        self.con = sqlite3.connect('score.db')
        self.cur = self.con.cursor()

    def add_in_datebase(self, name, password):
        self.cur.execute(f'''INSERT INTO players_score VALUES ('{len(self.names_players) + 1}', 
'{name}', 0, '{password}')''')
        self.con.commit()

    def start_game(self):
        self.count_misses = 0
        self.count_hits = 0
        self.count = 0
        self.dif_time_1 = 0
        self.f_btn.clicked.connect(self.function_misses)
        self.make_btns()
        self.make_timer()
        self.start_btn.hide()

    def make_timer(self):
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
        self.dif_time_2 = int(self.time.toString('ss'))
        self.kof_time = self.dif_time_2 - self.dif_time_1
        if self.kof_time == 0:
            self.kof_time = 1
        this_button.hide()
        self.count_hits += 1
        self.count += 100 * 1 / self.kof_time
        self.hits.display(self.count_hits)
        self.rezult.display(self.count)
        self.dif_time_1 = self.dif_time_2
        if self.count_hits == 30:
            self.finish_game()

    def finish_game(self):
        self.timer.stop()
        self.time = QtCore.QTime(0, 0, 0)
        self.start_btn.show()

    def function_misses(self):
        self.count_misses += 1
        self.count -= 50
        self.misses.display(self.count_misses)
        self.rezult.display(self.count)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
