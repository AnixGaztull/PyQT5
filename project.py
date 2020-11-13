import sys
import random
import sqlite3

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *


class Entrence_class(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('enter.ui', self)
        self.is_ok.hide()

        self.cancel_btn.clicked.connect(self.cancel_enter)
        self.enter_btn.clicked.connect(self.check_name)

    def check_name(self):
        global names_players, cur
        self.enter_name = str(self.name_input.text())
        self.enter_password = str(self.password.text())
        if self.enter_name in names_players:
            password = str(cur.execute(f"""SELECT password FROM players_score
                            WHERE name='{self.enter_name}'""").fetchall()[0][0])
            if password == self.enter_password:
                self.player_name = self.enter_name
                self.enter_btn.hide()
                self.is_ok.show()
            else:
                self.error_w.setText('неверный пароль')
        else:
            self.error_w.setText('неверное имя')

    def eye(self):
        pass

    def cancel_enter(self):
        self.hide()

    def return_name(self):
        return self.player_name


class Registration_class(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('registr.ui', self)

        self.reg_is = False
        self.is_ok.hide()

        self.registr_btn.clicked.connect(self.registration)
        self.cancel_btn.clicked.connect(self.cancel_registr)

    def registration(self):
        global names_players
        self.reg_password = str(self.input_password_reg.text())
        self.reg_password_2 = str(self.input_password_reg_2.text())
        self.reg_name = str(self.name_input.text())
        if self.reg_name not in names_players:
            if self.reg_password == self.reg_password_2:
                self.error_name.setText('имя свободно')
                self.reg_is = True
                self.registr_btn.hide()
                self.is_ok.show()
            else:
                self.error_2_password.setText('пароли не совпадают')
        else:
            self.error_name.setText('имя занято')

    def cancel_registr(self):
        self.hide()

    def return_reg_is(self):
        return self.reg_is

    def return_inf(self):
        return self.reg_name, self.reg_password


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('проект.ui', self)
        global cur, con
        self.cur = cur
        self.con = con

        self.exit_btn.hide()
        self.stop_btn.hide()

        self.log_in = False
        self.player_name = None

        self.entrence.clicked.connect(self.enter_in_acc)
        self.registration.clicked.connect(self.regist_new_acc)

        self.buttons = QButtonGroup()
        for i in range(30):
            self.button = QPushButton(self)
            self.button.resize(15, 15)
            self.button.move(0, 0)
            self.button.setStyleSheet(
                'border-radius: 7px; background: rgb(255, 30, 0); border: 0px')
            self.button.hide()
            self.buttons.addButton(self.button)
            self.buttons.setId(self.button, i)

        self.start_btn.clicked.connect(self.start_game)

    def regist_new_acc(self):
        self.window = Registration_class()
        self.open_window()
        self.window.is_ok.clicked.connect(self.reg_is_true)

    def reg_is_true(self):
        self.player_name, self.player_password = self.window.return_inf()
        self.add_in_datebase(self.player_name, self.player_password)
        self.window.hide()

        self.entrence.hide()
        self.registration.hide()
        self.window.hide()

        self.name.show()
        #self.exit_btn.show()
        self.max_points.show()

        self.name.setText(self.player_name)
        self.max_points.setText('0')
        self.log_in_true()

    def open_window(self):
        self.window.show()

    def log_in_true(self):
        self.score_player = int(self.cur.execute(f"""SELECT score FROM players_score
                                                WHERE name='{self.player_name}'""").fetchall()[0][0])
        #self.exit_btn.clicked.connect(self.exit)


    def enter_in_true(self):
        self.player_name = self.window.return_name()
        #self.exit_btn.show()
        self.window.hide()
        self.entrence.hide()
        self.registration.hide()
        self.name.show()
        self.max_points.show()

        self.name.setText(self.player_name)
        score = self.cur.execute(f"""SELECT score FROM players_score
                                    WHERE name='{self.player_name}'""").fetchall()[0]
        self.max_points.setText(str(score[0]))
        self.log_in_true()

    def enter_in_acc(self):
        self.window = Entrence_class()
        self.open_window()
        self.window.is_ok.clicked.connect(self.enter_in_true)

    def exit(self):
        self.name.hide()
        self.max_points.hide()
        self.entrence.show()
        self.registration.show()

        self.player_name = None
        self.hits.display(0)
        self.rezult.display(0)
        self.misses.display(0)
        self.exit_btn.hide()

    def add_in_datebase(self, name, password):
        self.cur.execute(f'''INSERT INTO players_score VALUES (null, '{name}', 0, '{password}')''')
        self.con.commit()

    def restart_count(self):
        self.count_misses = 0
        self.count_hits = 0
        self.count = 0
        self.hits.display(self.count_hits)
        self.rezult.display(self.count)
        self.misses.display(self.count_misses)

    def start_game(self):
        self.entrence.hide()
        self.registration.hide()
        self.stop_btn.show()

        self.game_now = True
        self.dif_time_1 = 0
        self.restart_count()

        self.f_btn.clicked.connect(self.function_misses)
        self.coords_buttons()

        self.make_timer()
        self.start_btn.hide()
        self.stop_btn.clicked.connect(self.delete_game)

    def coords_buttons(self):
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

    def make_timer(self):
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

    def timerEvent(self):
        self.time = self.time.addSecs(1)
        self.timeForPlayer.setText(self.time.toString("hh:mm:ss"))

    def function_btn(self, this_button):
        if self.game_now:
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
                this_button.hide()
                self.finish_game()


    def function_misses(self):
        if self.game_now:
            self.count_misses += 1
            self.count -= 50
            self.misses.display(self.count_misses)
            self.rezult.display(self.count)


    def delete_game(self):
        self.timer.stop()
        self.time = QtCore.QTime(0, 0, 0)
        self.restart_count()
        self.start_btn.show()
        self.stop_btn.hide()
        self.game_now = False

    def finish_game(self):
        if self.count > int(self.score_player):
            self.cur.execute(f'''UPDATE players_score 
                                SET score = {str(self.count)}
                                WHERE name={self.player_name}''')
            self.con.commit()
            self.score_player = self.count
        self.delete_game()

    def table_liders(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    con = sqlite3.connect('score.db')
    cur = con.cursor()
    names_players = list(map(lambda x: x[0], cur.execute("SELECT name FROM players_score").fetchall()))
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
