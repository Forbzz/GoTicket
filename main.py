import datetime
import sys
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtWidgets import *

import triggers
from db import *
from select_sql import *
from insert_sql import *
from update import *

conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('127.0.0.1', 8888)
db_file = 'sql1.db'


def tcp_init():
    try:
        conn_tcp.connect(server_addr)
    except socket.error:
        print('Server not responding')


def tcp_data(data: str) -> str:
    try:
        conn_tcp.send(data.encode())
        return conn_tcp.recv(2048).decode()
    except socket.error:
        print('Bad request')



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
    def __init__(self, match, event_info, country, city, street):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(400, 200))
        self.setWindowTitle("Покупка билета")

        layout = QFormLayout()
        self.setLayout(layout)

        b_buy = QPushButton('Купить', self)
        b_buy.clicked.connect(lambda: self.buy(match[0][2], match[0][0]))
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
    def buy(self, ticket_amount, id):
        print('buy', ticket_amount)
        ticket_amount -= 1
        execute_multiple_record([str(ticket_amount), str(id)], db_file, sql_update_event_tickets)
        self.close()
        self.window = OkWindow()
        self.window.show()
        app.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(700, 500))
        self.setWindowTitle("Go Ticket")

        layout = QVBoxLayout()
        self.setLayout(layout)

        tabs = QTabWidget()
        tabs.addTab(self.show_sport_ui(), "Просмот матчей")
        tabs.addTab(self.stat_user_ui(), "Статистика пользователей")
        tabs.addTab(self.create_match(), "Создать матч")
        tabs.addTab(self.show_role_ui(), "Управление ролями")
        tabs.addTab(self.show_logg_ui(), "Логгирование")
        layout.addWidget(tabs)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        w.show()

    # GUI для TAB просмотра матчей
    def show_sport_ui(self) -> QWidget:


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

        match_list = read_table(db_file,sql_select_event_all, None)

        self.t_sport.setRowCount(len (match_list))

        self.refresh()


        self.t_sport.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.t_sport.setSelectionBehavior(QAbstractItemView.SelectRows)

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
                datetime.datetime.strptime(date.text(), "%d.%m.%Y")
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
        show_role_tab = QWidget()
        layout = QFormLayout()
        list_users = QListWidget()
        items = ["user1", "user2", "user3"]
        list_users.addItems(items)
        layout.addWidget(list_users)
        admin_button = QRadioButton("Администратор")
        moder_button = QRadioButton("Модератор")
        user_button = QRadioButton("Пользователь")
        layout.addWidget(admin_button)
        layout.addWidget(moder_button)
        layout.addWidget(user_button)
        confirm_button = QPushButton("Изменить роль")
        layout.addWidget(confirm_button)
        show_role_tab.setLayout(layout)
        return show_role_tab

    def show_logg_ui(self) -> QWidget:
        show_logg_tab = QWidget()
        layout = QFormLayout()

        self.t_logg = QTableWidget()
        self.t_logg.setColumnCount(3)
        self.t_logg.setHorizontalHeaderLabels(['Пользователь', 'Время', 'Действие'])
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
        print('search')

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


        self.window = TicketWindow(match, event_info, country, city, street)
        self.window.show()
        app.exec_()

    @pyqtSlot()
    def update_ticket(self):
        print('update')
        self.refresh()


    @pyqtSlot()
    def refresh(self):
        match_list = read_table (db_file, sql_select_event_all, None)
        for index, match in enumerate (match_list):
            event_info = read_table (db_file, sql_select_event_info_id, match [3])
            address_info = read_table (db_file, sql_select_address_id, match [4])
            country = read_table (db_file, sql_select_country_id, address_info [0] [1])
            city = read_table (db_file, sql_select_city_id, address_info [0] [2])
            street = read_table (db_file, sql_select_street_id, address_info [0] [3])

            self.t_sport.setItem (index, 0, QTableWidgetItem (match [1]))
            self.t_sport.setItem (index, 1, QTableWidgetItem (str (event_info [0] [2])))
            self.t_sport.setItem (index, 2, QTableWidgetItem (str (match_list [index] [2])))
            self.t_sport.setItem (index, 3, QTableWidgetItem (event_info [0] [1]))
            self.t_sport.setItem (index, 4, QTableWidgetItem (country [0] [1] + "," + city [0] [1] + "," + street [0] [1]))


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
        pass

    # Вход через регистрацию
    @pyqtSlot()
    def on_click_sign_up(self):
        print('\nРегистрация')
        print('Логин  :', self.e_name_up.text())
        print('Пароль :', self.e_pass_up    .text())
        pass

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

    tcp_init()
    print(tcp_data('test'))

    sys.exit(app.exec_())