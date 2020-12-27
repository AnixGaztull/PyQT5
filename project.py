import sys, random, sqlite3

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import *


class Entrence_class(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('enter.ui', self)
        self.setWindowTitle("Вход")
        self.is_ok.hide()
        self.hide_password()
        self.cancel_btn.clicked.connect(self.cancel_enter)
        self.enter_btn.clicked.connect(self.check_name)
        self.eye_show.clicked.connect(self.show_password)
        self.eye_hide.clicked.connect(self.hide_password)

    def check_name(self):
        global cur

        names_players = list(map(lambda x: x[0], cur.execute("SELECT name FROM players_score").fetchall()))
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

    def show_password(self):
        self.eye_hide.show()
        self.eye_show.hide()
        self.password.setEchoMode(QLineEdit.Normal)

    def hide_password(self):
        self.eye_hide.hide()
        self.eye_show.show()
        self.password.setEchoMode(QLineEdit.Password)

    def cancel_enter(self):
        self.hide()

    def return_name(self):
        return self.player_name


class Registration_class(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('registr.ui', self)
        self.setWindowTitle("Регистрация")

        self.hide_password_1()
        self.hide_password_2()
        self.reg_is = False
        self.is_ok.hide()
        self.registr_btn.clicked.connect(self.registration)
        self.cancel_btn.clicked.connect(self.cancel_registr)
        self.eye_s1.clicked.connect(self.show_password_1)
        self.eye_s2.clicked.connect(self.show_password_2)
        self.eye_h1.clicked.connect(self.hide_password_1)
        self.eye_h2.clicked.connect(self.hide_password_2)

    def registration(self):
        names_players = list(map(lambda x: x[0], cur.execute("SELECT name FROM players_score").fetchall()))
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

    def show_password_1(self):
        self.input_password_reg.setEchoMode(QLineEdit.Normal)
        self.eye_s1.hide()
        self.eye_h1.show()

    def show_password_2(self):
        self.input_password_reg_2.setEchoMode(QLineEdit.Normal)
        self.eye_s2.hide()
        self.eye_h2.show()

    def hide_password_1(self):
        self.input_password_reg.setEchoMode(QLineEdit.Password)
        self.eye_h1.hide()
        self.eye_s1.show()

    def hide_password_2(self):
        self.input_password_reg_2.setEchoMode(QLineEdit.Password)
        self.eye_h2.hide()
        self.eye_s2.show()

    def return_reg_is(self):
        return self.reg_is

    def return_inf(self):
        return self.reg_name, self.reg_password


class Rezult_w(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('rezult_window.ui', self)
        self.setWindowTitle("Результат")
        self.ok.clicked.connect(self.ok_f)

    def print_rez(self, score):
        self.rezult.setText(f'Твой результат - {score}')

    def ok_f(self):
        self.hide()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('проект.ui', self)
        self.setWindowTitle("Trainer")

        global cur, con
        self.cur = cur
        self.con = con
        self.exit_btn.hide()
        self.stop_btn.hide()
        self.select_sm_table.hide()
        self.select_am_table.hide()
        self.standart_mode = True
        self.standart_mode_table = True
        self.log_in = False
        self.game_now = False
        self.player_name = None
        self.player_id = None
        self.score_player = None
        self.entrence.clicked.connect(self.enter_in_acc)
        self.registration.clicked.connect(self.regist_new_acc)
        self.create_table_liders()
        self.create_combobox()
        self.btn_miss.clicked.connect(self.function_misses)
        self.start_btn.clicked.connect(self.start_game)

    def regist_new_acc(self):
        self.window = Registration_class()
        self.open_window()
        self.window.is_ok.clicked.connect(self.reg_is_true)

    def reg_is_true(self):
        self.player_name, self.player_password = self.window.return_inf()
        self.add_in_datebase(self.player_name, self.player_password)
        self.log_in_true()

    def open_window(self):
        self.window.show()

    def log_in_true(self):
        self.log_in = True
        self.window.hide()
        self.entrence.hide()
        self.registration.hide()
        self.exit_btn.show()
        self.name.show()
        self.max_points_sm.show()
        self.max_points_am.show()
        self.score_player_sm, self.score_player_am = self.cur.execute(f"""SELECT standart_score, arcada_score 
                                                FROM players_score
                                                WHERE name='{self.player_name}'""").fetchall()[0]
        self.max_points_sm.setText(f'стандарт - {self.score_player_sm}')
        self.max_points_am.setText(f'аркада - {self.score_player_am}')
        self.name.setText(f'Имя игрока - {self.player_name}')
        self.load_liders_inf(True)
        self.load_liders_inf(False)
        self.exit_btn.clicked.connect(self.exit)

    def enter_in_true(self):
        self.player_name = self.window.return_name()
        self.log_in_true()

    def enter_in_acc(self):
        self.window = Entrence_class()
        self.open_window()
        self.window.is_ok.clicked.connect(self.enter_in_true)

    def exit(self):
        self.name.hide()
        self.max_points_am.hide()
        self.max_points_sm.hide()
        self.entrence.show()
        self.registration.show()
        if self.game_now:
            self.delete_game()
        self.player_name = None
        self.log_in = False
        self.hits.display(0)
        self.rezult.display(0)
        self.misses.display(0)
        self.exit_btn.hide()
        self.del_u_from_table(self.player_id_in_table_sm, self.tableLiders_sm)
        self.del_u_from_table(self.player_id_in_table_am, self.tableLiders_am)

    def create_combobox(self):
        self.select_mode.addItem('Стандарт')
        self.select_mode.addItem('Аркада')
        self.select_mode.activated.connect(self.on_activated)

    def on_activated(self, text):
        if text == 0:
            self.standart_mode = True
            self.label_5.show()
            self.misses.show()
        else:
            self.standart_mode = False
            self.label_5.hide()
            self.misses.hide()

    def add_in_datebase(self, name, password):
        self.cur.execute(f'''INSERT INTO players_score VALUES (null, '{name}', 0, 0, '{password}')''')
        self.con.commit()

    def restart_count(self):
        self.count_misses = 0
        self.count_hits = 0
        self.count = 0
        self.hits.display(self.count_hits)
        self.rezult.display(self.count)
        self.misses.display(self.count_misses)

    def start_game(self):
        model = self.select_mode.model()
        model.item(0).setEnabled(False)
        model.item(1).setEnabled(False)
        if self.standart_mode:
            self.num_btns = 30
        else:
            self.num_btns = 1
        self.game_now = True
        self.buttons = QButtonGroup()
        for i in range(self.num_btns):
            self.button = QPushButton(self)
            self.button.resize(15, 15)
            self.button.move(0, 0)
            self.button.setStyleSheet(
                'border-radius: 7px; background: rgb(255, 30, 0); border: 0px')
            self.button.hide()
            self.buttons.addButton(self.button)
            self.buttons.setId(self.button, i)
        if self.log_in:
            self.entrence.hide()
            self.registration.hide()
        self.stop_btn.show()
        self.game_now = True
        self.dif_time_1 = 0
        self.restart_count()
        if self.standart_mode:
            self.coords_buttons_sm()
        else:
            self.button_game = self.buttons.button(0)
            self.button_game.show()
            self.coord_button_am()
            self.button_game.clicked.connect(self.function_btn_am)
        self.make_timer()
        self.start_btn.hide()
        self.stop_btn.clicked.connect(self.delete_game)

    def coords_buttons_sm(self):
        coords = []
        for i in range(self.num_btns):
            x = random.randrange(0, 430, 16)
            y = random.randrange(30, 560, 16)
            coord = (x, y)
            if coord not in coords:
                coords.append(coord)
            self.buttons.button(i).show()
            self.buttons.button(i).move(x, y)
        self.buttons.buttonClicked.connect(self.function_btn_sm)

    def coord_button_am(self):
        x = random.randrange(0, 430)
        y = random.randrange(30, 540)
        self.button_game.move(x, y)

    def make_timer(self):
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

    def timerEvent(self):
        self.time = self.time.addSecs(1)
        self.timeForPlayer.setText(self.time.toString("hh:mm:ss"))
        if self.game_now and not self.standart_mode:
            if int(self.time.toString('ss')) > 2:
                self.game_over()

    def function_btn_sm(self, this_button):
        if self.game_now:
            self.dif_time_2 = int(self.time.toString('ss'))
            self.kof_time = self.dif_time_2 - self.dif_time_1
            if self.kof_time == 0:
                self.kof_time = 1
            this_button.hide()
            self.count_hits += 1
            self.count += int(100 * 1 / self.kof_time)
            self.hits.display(self.count_hits)
            self.rezult.display(self.count)
            self.dif_time_1 = self.dif_time_2
            if self.count_hits == self.num_btns:
                this_button.hide()
                self.finish_game()

    def function_btn_am(self):
        self.timer.stop()
        self.timeForPlayer.setText('00:00:00')
        self.make_timer()
        self.count_hits += 1
        self.coord_button_am()
        self.hits.display(self.count_hits)

    def function_misses(self):
        if self.game_now:
            if self.standart_mode:
                self.count_misses += 1
                self.count -= 50
                self.misses.display(self.count_misses)
                self.rezult.display(self.count)
            else:
                self.game_over()

    def delete_game(self):
        model = self.select_mode.model()
        model.item(0).setEnabled(True)
        model.item(1).setEnabled(True)
        self.timeForPlayer.setText('00:00:00')
        self.timer.stop()
        self.time = QtCore.QTime(0, 0, 0)
        for i in range(self.num_btns):
            self.buttons.button(i).hide()
        if self.standart_mode:
            self.load_liders_inf(True)
        else:
            self.load_liders_inf(False)
        self.restart_count()
        self.start_btn.show()
        self.stop_btn.hide()
        self.game_now = False

    def finish_game(self):
        if self.log_in:
            if self.count > int(self.score_player_sm):
                self.cur.execute(f'''UPDATE players_score 
                                        SET standart_score = {int(self.count)}
                                        WHERE name={self.player_name}''')
                self.con.commit()
                self.score_player_sm = self.count
                self.max_points_sm.setText(str(self.score_player_sm))
                self.load_liders_inf(True)
        self.window = Rezult_w()
        self.window.print_rez(self.count)
        self.open_window()
        self.delete_game()

    def game_over(self):
        if self.log_in:
            if self.count_hits > int(self.score_player_am):
                self.cur.execute(f'''UPDATE players_score 
                                    SET arcada_score = {int(self.count_hits)}
                                    WHERE name={self.player_name}''')
                self.con.commit()
                self.score_player_am = self.count_hits
                self.max_points_am.setText(str(self.score_player_am))
                self.load_liders_inf(True)
        self.window = Rezult_w()
        self.window.print_rez(self.count_hits)
        self.open_window()
        self.delete_game()

    def create_table_liders(self):
        self.tableLiders_sm.setColumnCount(2)
        self.tableLiders_sm.setColumnWidth(0, 115)
        self.tableLiders_sm.setColumnWidth(1, 115)
        self.tableLiders_am.setColumnCount(2)
        self.tableLiders_am.setColumnWidth(0, 115)
        self.tableLiders_am.setColumnWidth(1, 115)
        self.tableLiders_sm.setHorizontalHeaderLabels(["Имя", "Счет"])
        self.tableLiders_am.setHorizontalHeaderLabels(["Имя", "Счет"])
        self.load_liders_inf(True)
        self.load_liders_inf(False)
        self.select_sm_table.show()
        self.select_am_table.show()
        self.select_sm_table.setEnabled(False)
        self.select_am_table.clicked.connect(self.change_table_am)
        self.select_sm_table.clicked.connect(self.change_table_sm)

    def load_liders_inf(self, standart):
        self.scroll_btn.hide()
        if standart:
            self.liders_inf = list(map(lambda x: (x[0], x[1]),
                                       cur.execute("SELECT name, standart_score FROM players_score").fetchall()))
        else:
            self.liders_inf = list(map(lambda x: (x[0], x[1]),
                                       cur.execute("SELECT name, arcada_score FROM players_score").fetchall()))
        self.scores = list(map(lambda x: x[1], self.liders_inf))
        self.scores = set(self.scores)
        self.scores = list(self.scores)
        self.scores.sort()
        self.scores.reverse()

        self.scores_liders = []
        for score in self.scores:
            list_name_w_scores = list(filter(lambda x: x[1] == score, self.liders_inf))
            self.scores_liders.extend(list_name_w_scores)

        if self.log_in:
            if standart:
                self.player_id_in_table_sm = self.scores_liders.index((self.player_name, self.score_player_sm))
            else:
                self.player_id_in_table_am = self.scores_liders.index((self.player_name, self.score_player_am))
            self.scroll_btn.show()
        self.scroll_btn.clicked.connect(self.scroll_table)
        self.fill_table_liders(standart)

    def fill_table_liders(self, standart):
        self.count_row = len(self.liders_inf)
        if standart:
            self.tableLiders_sm.setRowCount(self.count_row)
        else:
            self.tableLiders_am.setRowCount(self.count_row)
        for id in range(self.count_row):
            self.add_toTableLiders(id, self.scores_liders[id], standart)
        if self.log_in:
            if standart:
                self.show_u_score_in_table(self.player_id_in_table_sm, self.tableLiders_sm)
            else:
                self.show_u_score_in_table(self.player_id_in_table_am, self.tableLiders_am)

    def add_toTableLiders(self, id, inf, standart):
        item_name = QTableWidgetItem(inf[0])
        item_score = QTableWidgetItem(str(inf[1]))
        item_name.setFlags(QtCore.Qt.ItemIsEnabled)
        item_score.setFlags(QtCore.Qt.ItemIsEnabled)
        item_name.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item_score.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if standart:
            self.tableLiders_sm.setItem(id, 0, item_name)
            self.tableLiders_sm.setItem(id, 1, item_score)
        else:
            self.tableLiders_am.setItem(id, 0, item_name)
            self.tableLiders_am.setItem(id, 1, item_score)

    def change_table_am(self):
        self.select_am_table.setEnabled(False)
        self.select_sm_table.setEnabled(True)
        self.tableLiders_sm.hide()
        self.tableLiders_am.show()
        self.standart_mode_table = False
        self.load_liders_inf(self.standart_mode_table)

        if self.log_in:
            self.scroll_label.setText(f'Вы - #{self.player_id_in_table_am + 1}')

    def change_table_sm(self):
        self.select_sm_table.setEnabled(False)
        self.select_am_table.setEnabled(True)
        self.tableLiders_am.hide()
        self.tableLiders_sm.show()
        self.standart_mode_table = True
        self.load_liders_inf(self.standart_mode_table)

        if self.log_in:
            self.scroll_label.setText(f'Вы - #{self.player_id_in_table_sm + 1}')

    def show_u_score_in_table(self, id, table):
        table.item(id, 0).setBackground(QtGui.QColor(190, 190, 255))
        table.item(id, 1).setBackground(QtGui.QColor(190, 190, 255))
        self.scroll_label.show()
        self.scroll_label.setText(f'Вы - #{self.player_id_in_table_sm + 1}')

    def del_u_from_table(self, id, table):
        table.item(id, 0).setBackground(QtGui.QColor(255, 255, 255))
        table.item(id, 1).setBackground(QtGui.QColor(255, 255, 255))
        self.scroll_label.hide()

    def scroll_table(self):
        if self.standart_mode_table:
            player_id_in_table = self.player_id_in_table_sm
        else:
            player_id_in_table = self.player_id_in_table_am
        scroll_id = player_id_in_table
        if len(self.scores_liders) - player_id_in_table > 4:
            scroll_id = player_id_in_table + 4
        if self.standart_mode_table:
            self.tableLiders_sm.scrollToItem(self.tableLiders_sm.item(player_id_in_table, 0))
        else:
            self.tableLiders_am.scrollToItem(self.tableLiders_am.item(player_id_in_table, 0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    con = sqlite3.connect('score.db')
    cur = con.cursor()
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
