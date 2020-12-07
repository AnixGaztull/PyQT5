    def create_combobox(self):
        self.select_mode.addItem('Стандарт')
        self.select_mode.addItem('Аркада')
        self.select_mode.activated[str].connect(self.on_activated)

    def on_activated(self, text):
        if text == 'Стандарт':
            self.standart_mode = True
        else:
            self.standart_mode = False

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
            self.coord_button_am()

        self.make_timer()
        self.start_btn.hide()
        self.stop_btn.clicked.connect(self.delete_game)

    def coord_button_am(self):
        x = random.randrange(0, 430)
        y = random.randrange(30, 570)
        self.button_game = self.buttons.button(0)
        self.button_game.show()
        self.button_game.move(x, y)

    def function_btn_am(self):
        self.button_game.hide()
        self.timeForPlayer.setText('00:00:00')
        self.coord_button_am()
        self.count_hits += 1

    def function_misses(self):
        if self.standart_mode:
            self.count_misses += 1
            self.count -= 50
            self.misses.display(self.count_misses)
            self.rezult.display(self.count)
        else:
            self.game_over()

    def delete_game(self):
        self.timeForPlayer.setText('00:00:00')
        for i in range(self.num_btns):
            self.buttons.button(i).hide()
        self.timer.stop()
        self.time = QtCore.QTime(0, 0, 0)
        self.restart_count()
        self.start_btn.show()
        self.stop_btn.hide()
        self.btn_miss.disconnect()
        self.game_now = False

    def game_over(self):
        pass

