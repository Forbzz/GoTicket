import sys
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtWidgets import *

from create_sql import create_connection
import triggers
from db import *
from select_sql import *
from insert_sql import *
from update import *
from datetime import datetime

conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('127.0.0.1', 8888)
db_file = 'sql1.db'

# окно после покупки билета об оповещении(если можно сделать красивее, сделайте)
class OkWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize (400, 200))
        self.setWindowTitle("Покупка билета")

        layout = QFormLayout()
        self.setLayout(layout)

        self.l_test1 = QLabel("Билет успешно куплен!")
        layout.addRow(self.l_test1)

        w = QWidget ()
        w.setLayout (layout)
        self.setCentralWidget (w)
        w.show ()


class TicketWindow(QMainWindow):
    def __init__(self, match, event_info, country, city, street, user, name):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(400, 200))
        self.setWindowTitle("Покупка билета")

        layout = QFormLayout()
        self.setLayout(layout)

        b_buy = QPushButton('Купить', self)
        b_buy.clicked.connect(lambda: self.buy(match[0][2], match[0][0], user, name))
        layout.addRow(b_buy)

        self.l_test1 = QLabel(match[0][1])
        layout.addRow('Название события', self.l_test1)

        self.l_test1 = QLabel (str(match[0][2]))
        layout.addRow('Количество оставшихся билетов', self.l_test1)

        self.l_test1 = QLabel(str(event_info[0][2]) + " мин")
        layout.addRow('Длительность', self.l_test1)

        self.l_test1 = QLabel(event_info[0][1])
        layout.addRow('Дата', self.l_test1)

        self.l_test1 = QLabel (country[0][1])
        layout.addRow ('Страна', self.l_test1)

        self.l_test1 = QLabel (city[0][1])
        layout.addRow ('Город', self.l_test1)

        self.l_test1 = QLabel (street[0][1])
        layout.addRow ('Улица', self.l_test1)

        self.l_test1 = QLabel (event_info[0][3])
        layout.addRow ('Описание', self.l_test1)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        w.show()

    # покупка-обновление количества билетов
    @pyqtSlot()
    def buy(self, ticket_amount, id, user, name):
        print('Покупка', ticket_amount)
        ticket_amount -= 1
        print ("Пользователь", user)
        user_info = read_table(db_file, sqL_select_user_from_login, user)
        print("В итоге:", user_info)

        match = read_table(db_file, sql_select_event_name, name)
        time = datetime.now ().strftime ("%B %d, %Y %I:%M%p")

        execute_multiple_record([0, time, user_info[0][0], match[0][0]], db_file, sql_insert_ticket)
        execute_multiple_record([str(ticket_amount), str(id)], db_file, sql_update_event_tickets)
        self.close()
        self.window = OkWindow()
        self.window.show()
        app.exec_()


class MainWindow(QMainWindow):

    def __init__(self, user=None):
        QMainWindow.__init__(self)
        self.role = 0
        self.user = user
        self.list_roles = []
        if user is not None:
            print("незареганный")
            conn = create_connection(db_file)
            c = conn.cursor()
            role_query = c.execute(sql_select_users_role, (user,))
            role = c.fetchall()
            role = [i[0] for i in role]
            self.role = role[0]  # текущая роль челикаа
            c.execute(sql_select_list_roles, (self.role,))
            role = c.fetchall()
            role = [i[0] for i in role]
            self.list_roles = role
            print(role)
        self.setMinimumSize(QSize(700, 500))
        self.setWindowTitle("Go Ticket")

        layout = QVBoxLayout()
        self.setLayout(layout)
        print("ROLE", self.role)
        tabs = QTabWidget()
        tabs.addTab (self.show_sport_ui (self.list_roles), "Просмот матчей")

        if 'MODERATOR' in self.list_roles:
            tabs.addTab (self.stat_user_ui (), "Статистика пользователей")
            tabs.addTab (self.create_match (), "Создать матч")
        #tabs.addTab (self.stat_user_ui (), "Статистика пользователей")
        if 'ADMIN' in self.list_roles:
            tabs.addTab (self.show_role_ui (), "Управление ролями")
            tabs.addTab (self.show_logg_ui (), "Логгирование")



        tabs.tabBarClicked.connect(self.onTabBarClicked)
        layout.addWidget(tabs)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        w.show()

    def onTabBarClicked(self, index):
        if index == 1:
            self.update_stat ()
        if index == 4 or index == 3:
            self.update_log()
        if index == 0:
            self.update_ticket()

    def update_stat (self):
        stat_list = triggers.sql_execute ("sql1.db", """SELECT user.login, COUNT(*), user.registration_date FROM user
                                                        JOIN ticket ON ticket.user_id = user.id
                                                        GROUP BY user.id;""")
        self.t_user.setRowCount (len (stat_list))
        for i in range (len (stat_list)):
            self.t_user.setItem (i, 0, QTableWidgetItem (str (stat_list [i] [0])))
            self.t_user.setItem (i, 1, QTableWidgetItem (str (stat_list [i] [1])))
            self.t_user.setItem (i, 2, QTableWidgetItem (str (stat_list [i] [2])))



    # GUI для TAB просмотра матчей
    def show_sport_ui(self, list_roles) -> QWidget:

        create_sport_tab = QWidget()
        layout = QFormLayout()

        self.e_search = QLineEdit()
        self.e_search.setPlaceholderText('Введите для поиска')
        layout.addWidget(self.e_search)

        b_search = QPushButton('Найти', self)
        b_search.clicked.connect(self.search_ticket)
        layout.addWidget(b_search)

        self.t_sport = QTableWidget()
        self.t_sport.setColumnCount(5)
        self.t_sport.setHorizontalHeaderLabels(['Название', 'Длительность', 'Кол-во билетов', 'Дата', 'Адрес'])

        match_list = read_table(db_file, sql_select_event_all, None)

        self.t_sport.setRowCount(len (match_list))

        self.refresh()


        self.t_sport.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.t_sport.setSelectionBehavior(QAbstractItemView.SelectRows)

        if "USER" in list_roles:
            self.t_sport.itemDoubleClicked.connect(self.buy_ticket)
        self.t_sport.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        header = self.t_sport.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.t_sport.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.t_sport)

        b_search = QPushButton('Обновить', self)
        b_search.clicked.connect(self.update_ticket)
        layout.addWidget(b_search)

        create_sport_tab.setLayout(layout)

        return create_sport_tab

    # GUI для TAB просмотра статистики
    def stat_user_ui(self) -> QWidget:
        stat_user_tab = QWidget()
        layout = QFormLayout()

        self.t_user = QTableWidget()
        self.t_user.setColumnCount(3)
        self.t_user.setHorizontalHeaderLabels(['Пользователь', 'Купленные билеты', 'Дата регистрации'])
        self.t_user.setRowCount(1)
        self.t_user.setItem(0, 0, QTableWidgetItem("SAMPLE"))
        self.t_user.setItem(0, 1, QTableWidgetItem("SAMPLE"))
        self.t_user.setItem(0, 2, QTableWidgetItem("SAMPLE"))
        self.t_user.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.t_user.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.t_user.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        header = self.t_user.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.t_user.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.t_user)

        stat_user_tab.setLayout(layout)
        return stat_user_tab

    def create_sport_ui(self) -> QWidget:
        pass

    def create_match(self) -> QWidget:
        def on_click_add_match():
            print('\nСоздание матча')

            try:
                datetime.strptime(date.text(), "%d.%m.%Y")
            except ValueError:
                QMessageBox.information (self, 'Внимание', 'Неверный формат даты')
                return

            if name.text() == "" or ticket_num.text() == "" or description.text() == "" or duration.text() == ""\
                or date.text() == "" or country.text() == "" or city.text() == "" or street.text() == "":
                QMessageBox.information(self, 'Внимание', 'Введите все поля')
                return

            country_list = read_table(db_file, sql_select_country_name, country.text())
            city_list = read_table(db_file, sql_select_city_name, city.text())
            street_list = read_table(db_file, sql_select_street_name, street.text())

            if len(country_list) == 0:
                execute_single_record(country.text(), db_file, sql_insert_country)
            if len(city_list) == 0:
                execute_single_record(city.text(), db_file, sql_insert_city)
            if len(street_list) == 0:
                execute_single_record(street.text(), db_file, sql_insert_street)
            print("========")

            country_list = read_table(db_file, sql_select_country_name, country.text())
            city_list = read_table(db_file, sql_select_city_name, city.text())
            street_list = read_table(db_file, sql_select_street_name, street.text())

            address_list = read_table(db_file, sql_select_address_street_id, street_list[0][0])
            if len(address_list) == 0:
                execute_multiple_record([country_list[0][0], city_list[0][0], street_list[0][0]], db_file,
                                        sql_insert_address)
            address_list = read_table(db_file, sql_select_address_street_id, street_list[0][0])

            execute_multiple_record([description.text(), duration.text(), date.text()], db_file, sql_insert_event_info)
            event_info_list = read_table(db_file, sql_select_event_info_description, description.text())
            execute_multiple_record([name.text(), ticket_num.text(), event_info_list[0][0], address_list[0][0]],
                                    db_file,
                                    sql_insert_event)

        show_sport_tab = QWidget()
        layout = QFormLayout()
        name = QLineEdit()
        ticket_num = QLineEdit()
        description = QLineEdit()
        duration = QLineEdit()
        date = QLineEdit()
        country = QLineEdit()
        city = QLineEdit()
        street = QLineEdit()
        b_si_up = QPushButton('Добавить матч', self)
        b_si_up.clicked.connect(on_click_add_match)


        layout.addRow('Название', name)
        layout.addRow('Количество билетов', ticket_num)
        layout.addRow('Описание', description)
        layout.addRow('Длительность', duration)
        layout.addRow('Дата матча', date)
        layout.addRow('Страна', country)
        layout.addRow('Город', city)
        layout.addRow('Улица', street)
        layout.addRow(b_si_up)

        int_validator = QIntValidator(self)
        int_validator.setRange(1, 100000)

        ticket_num.setValidator(int_validator)
        duration.setValidator(int_validator)

        show_sport_tab.setLayout(layout)
        return show_sport_tab

    def show_role_ui(self) -> QWidget:
        #pass
        self.selected_login = ""  # создание для выбранного пользователя
        show_role_tab = QWidget()
        layout = QFormLayout()
        list_users = QListWidget()
        conn = create_connection(db_file)  # ставим связь с базой
        c = conn.cursor()
        login_query = c.execute(sql_select_users_login)
        list_logins = c.fetchall()

        list_logins = [i[0] for i in list_logins] # получаем список всех логинов

        personal_info_ids = c.execute(sql_select_users_all)
        list_personal_info_ids = c.fetchall()  # получаем idшники чтобы получить фио
        print(list_personal_info_ids)
        list_fio = []
        for id in list_personal_info_ids:
            fio_query = c.execute(sql_select_personal_info_fio, id)
            list_fio.append(c.fetchall()[0])
        list_fio = [i[0] for i in list_fio]  # все ФИО
        for i in range(len(list_logins)):
            list_fio[i] = f"{list_logins[i]} ({list_fio[i]})"  # формат по вашему заказу
        list_users.addItems(list_fio)  # добавляем в список для экрана
        list_users.itemDoubleClicked.connect(self.getRole)  # если челик тапнет 2 раза, то идем в метод
        layout.addWidget(list_users)
        self.admin_button = QRadioButton("Администратор")
        self.moder_button = QRadioButton("Модератор")
        self.user_button = QRadioButton("Пользователь")  # кнопочки
        layout.addWidget(self.admin_button)
        layout.addWidget(self.moder_button)
        layout.addWidget(self.user_button)
        confirm_button = QPushButton("Изменить роль")  # кнопка подтверждений
        confirm_button.clicked.connect(self.changeRole)  # меняем роль если кликнул
        layout.addWidget(confirm_button)
        show_role_tab.setLayout(layout)
        return show_role_tab

    def changeRole(self):
        # какую роль ставим?
        if self.admin_button.isChecked():
            role = 1
        elif self.moder_button.isChecked():
            role = 2
        elif self.user_button.isChecked():
            role = 3
        else:
            message = QErrorMessage()
            message.showMessage("Роль не выбрана!")
            message.exec_()
            return
        if len(self.selected_login) == 0:
            message = QErrorMessage()
            message.showMessage("Пользователь не выбран!")
            message.exec_()
            return
        # обновляем роль
        conn = create_connection(db_file)
        c = conn.cursor()
        sql_update_user_role = '''
        update user
        set role_id = ?
        where login = ?;
        '''
        role_query = c.execute(sql_update_user_role, (role, self.selected_login,))
        conn.commit()

    def getRole(self, item):
        login = item.text().split()[0]
        self.selected_login = login  # для будушего чтобы засунуть в логин роль
        conn = create_connection(db_file)
        c = conn.cursor()
        role_query = c.execute(sql_select_users_role, (login,))
        role = c.fetchall()
        role = [i[0] for i in role]
        role = role[0]  # текущая роль челикаа
        if role == 'ADMIN':
            self.admin_button.setChecked(True)
            self.admin_button.setChecked(False)
        if role == 'MODERATOR':
            self.moder_button.setChecked(True)
            self.moder_button.setChecked(False)
        if role == 'USER':
            self.user_button.setChecked(True)
            self.user_button.setChecked(False)
        # обновляем кнопку от роли, почему так? потому что если оставить её чекнутой, то сколько ткать не будешь, кнопка не от лочится.

    def show_logg_ui(self) -> QWidget:
        show_logg_tab = QWidget()
        layout = QFormLayout()

        self.t_logg = QTableWidget()
        self.t_logg.setColumnCount(3)
        self.t_logg.setHorizontalHeaderLabels(['Информация', 'Время', 'Действие'])
        self.update_log()
        self.t_logg.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.t_logg.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.t_logg.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        header = self.t_logg.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.t_logg.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.t_logg)

        show_logg_tab.setLayout(layout)
        return show_logg_tab

    @pyqtSlot()
    def update_log(self):
        log_list = triggers.sql_execute("sql1.db", triggers.sql_select_logg_info)
        self.t_logg.setRowCount(len(log_list))
        for i in range(len(log_list)):
            if log_list[i][0] != -1:
                self.t_logg.setItem(i, 0, QTableWidgetItem('Пользователь (ID: ' + str(log_list[i][0]) + ')'))
            elif log_list[i][1] != -1:
                self.t_logg.setItem(i, 0, QTableWidgetItem('Билет (ID: ' + str(log_list[i][1]) + ')'))
            else:
                self.t_logg.setItem(i, 0, QTableWidgetItem('Событие (ID: ' + str(log_list[i][2]) + ')'))
            self.t_logg.setItem(i, 1, QTableWidgetItem(str(log_list[i][3])))
            self.t_logg.setItem(i, 2, QTableWidgetItem(str(log_list[i][4])))


    @pyqtSlot()
    def search_ticket(self):
        print (self.e_search.text ())
        event_list = search_record(self.e_search.text(), db_file, sql_select_event_like_name)
        desc_list = search_record(self.e_search.text(), db_file, sql_select_event_info_description_like)
        event_desc_list = []
        event_from_list = []
        for item in desc_list:
            event_from_list.append (read_table (db_file, sql_select_event_from_event_info_id, item [0]))
        for item in event_from_list:
            if item:
                event_desc_list.append(item[0])
        matches_list = event_list + event_desc_list
        self.refresh (list (set (matches_list)))
        print ('search')

    # берётся выделенный матч и подгружаются все нужные данные
    @pyqtSlot()
    def buy_ticket(self):

        name = self.t_sport.selectedItems()[0].text()
        match = read_table(db_file, sql_select_event_name, name)

        event_info = read_table (db_file, sql_select_event_info_id, match[0][3])
        address_info = read_table (db_file, sql_select_address_id, match[0][4])
        country = read_table (db_file, sql_select_country_id, address_info[0][1])
        city = read_table (db_file, sql_select_city_id, address_info[0][2])
        street = read_table (db_file, sql_select_street_id, address_info[0][3])

        self.window = TicketWindow(match, event_info, country, city, street, self.user, name)
        self.window.show()
        app.exec_()

    @pyqtSlot()
    def update_ticket(self):
        print('update')
        self.refresh()


    @pyqtSlot()
    def refresh(self, match_list=None):

        if match_list is None:
            match_list = read_table(db_file, sql_select_event_all, None)
        count_row = 0
        for i in match_list:
            if i[2] < 1:
                continue
            if i[2] > 0:
                count_row+=1
        self.t_sport.setRowCount(count_row)

        index = 0
        item = 0
        for match in match_list:
            if match[2] < 1:
                item+=1
            if match[2] > 0:
                event_info = read_table(db_file, sql_select_event_info_id, match [3])
                address_info = read_table(db_file, sql_select_address_id, match [4])
                country = read_table(db_file, sql_select_country_id, address_info [0] [1])
                city = read_table(db_file, sql_select_city_id, address_info [0] [2])
                street = read_table(db_file, sql_select_street_id, address_info [0] [3])

                self.t_sport.setItem(index, 0, QTableWidgetItem(match[1]))
                self.t_sport.setItem(index, 1, QTableWidgetItem(str(event_info[0] [2])))
                self.t_sport.setItem(index, 2, QTableWidgetItem(str(match_list[item][2])))
                self.t_sport.setItem(index, 3, QTableWidgetItem(event_info [0] [1]))
                self.t_sport.setItem(index, 4, QTableWidgetItem(country [0] [1] + "," + city [0] [1] + "," + street [0] [1]))
                index+=1
                item+=1
        # self.t_sport.setRowCount(index)

class AuthWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(70, 70))
        self.setWindowTitle("Авторизация")

        layout = QVBoxLayout()
        self.setLayout(layout)

        tabs = QTabWidget()
        tabs.addTab(self.sign_in_ui(), "Войти")
        tabs.addTab(self.sign_up_ui(), "Регистрация")
        layout.addWidget(tabs)

        b_si_none = QPushButton('Войти без авторизации', self)
        b_si_none.clicked.connect(self.on_click_sign_none)
        layout.addWidget(b_si_none)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        w.show()

    # GUI для TAB входа
    def sign_in_ui(self) -> QWidget:
        sign_in_tab = QWidget()
        layout = QFormLayout()

        self.e_name_in = QLineEdit()
        self.e_pass_in = QLineEdit()
        b_si_in = QPushButton('Войти', self)
        b_si_in.clicked.connect(self.on_click_sign_in)

        layout.addRow('Логин', self.e_name_in)
        layout.addRow('Пароль', self.e_pass_in)
        layout.addRow(b_si_in)

        sign_in_tab.setLayout(layout)
        return sign_in_tab

    # GUI для TAB регистрации
    def sign_up_ui(self) -> QWidget:
        sign_up_tab = QWidget()
        layout = QFormLayout()

        self.e_name_up = QLineEdit()
        self.e_pass_up = QLineEdit()
        self.e_pass_up_check = QLineEdit()
        b_si_up = QPushButton('Регистрация', self)
        b_si_up.clicked.connect(self.on_click_sign_up)

        layout.addRow('Логин', self.e_name_up)
        layout.addRow('Пароль', self.e_pass_up)
        layout.addRow('Повт. пароль', self.e_pass_up_check)
        layout.addRow(b_si_up)

        sign_up_tab.setLayout(layout)
        return sign_up_tab

    # GUI Показать окно с ошибкой
    def show_error_msg(self, title: str, msg: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Error")
        msg_box.setInformativeText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    # Вход через существующего пользователя
    @pyqtSlot()
    def on_click_sign_in(self):
        print('\nВход')
        print('Логин  :', self.e_name_in.text())
        print('Пароль :', self.e_pass_in.text())
        conn = create_connection(db_file)
        c = conn.cursor()
        login_query = c.execute(sql_select_users_login_pass, (self.e_name_in.text(),))
        password = c.fetchall()
        if len(password) == 0:
            msgBox = QMessageBox()
            msgBox.setText("Неверный логин")
            msgBox.exec()
            return
        password = password[0][0]
        if password != self.e_pass_in.text():
            msgBox = QMessageBox()
            msgBox.setText("Неверный пароль")
            msgBox.exec()
            return
        self.close()
        self.window = MainWindow(self.e_name_in.text())
        self.window.show()

    # Вход через регистрацию
    @pyqtSlot()
    def on_click_sign_up(self):
        print('\nРегистрация')
        print('Логин  :', self.e_name_up.text())
        print('Пароль :', self.e_pass_up.text())
        if self.e_pass_up.text() != self.e_pass_up_check.text():
            msgBox = QMessageBox()
            msgBox.setText("Введенные пароли не совпадают")
            msgBox.exec()
            return
        conn = create_connection(db_file)
        c = conn.cursor()
        role_query = c.execute(sql_select_users_role, (self.e_name_up.text(),))
        role = c.fetchall()
        if len(role) > 0:
            msgBox = QMessageBox()
            msgBox.setText("Пользователь с таким именем уже существует")
            msgBox.exec()
            return
        if len(self.e_pass_up.text()) < 8:
            msgBox = QMessageBox()
            msgBox.setText("Пароль должен содержать хотя бы 8 символов")
            msgBox.exec()
            return
        conn = create_connection(db_file)

        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        execute_multiple_record(["",0], db_file, sql_insert_personal_info)
        conn = create_connection(db_file)
        last_personal_info_id_query = c.execute(sql_select_last_personal_info)
        last_personal_info_id = c.fetchall()
        last_personal_info_id = last_personal_info_id[0][0]

        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        execute_multiple_record([self.e_pass_up.text(), self.e_name_up.text(),time, 0, 3, last_personal_info_id], db_file, sql_insert_user)
        self.close()
        self.window = MainWindow(user = self.e_name_up.text())
        self.window.show()


    # Вход без авторизации
    @pyqtSlot()
    def on_click_sign_none(self):
        print('\nВход без регистрации')
        self.close()
        self.window = MainWindow()
        self.window.show()
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = AuthWindow()
    mainWin.show()

    sys.exit(app.exec_())
