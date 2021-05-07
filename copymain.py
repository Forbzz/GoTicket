import sys
import socket
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('127.0.0.1', 8888)


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
        return 'Bad request'


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(700, 500))
        self.setWindowTitle("Go Ticket")

        layout = QVBoxLayout()
        self.setLayout(layout)

        tabs = QTabWidget()
        tabs.addTab(self.create_sport_ui(), "Просмот матчей")
        tabs.addTab(self.show_sport_ui(), "Статистика пользователей")
        tabs.addTab(self.show_sport_ui(), "Создать матч")
        tabs.addTab(self.show_sport_ui(), "Управление ролями")
        tabs.addTab(self.show_sport_ui(), "Логгирование")
        layout.addWidget(tabs)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        w.show()

    # GUI для TAB Создания матчей
    def create_sport_ui(self) -> QWidget:
        create_sport_tab = QWidget()
        layout = QFormLayout()

        self.e_search = QLineEdit();

        self.t_user = QTableWidget()
        self.t_user.setColumnCount(6)
        self.t_user.setHorizontalHeaderLabels(
            ['Название', 'Адрес', 'Кол-во билетов', 'Дата проведения', 'Длительность'])
        self.t_user.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.t_user.setRowCount(1)
        self.t_user.setItem(0, 0, QTableWidgetItem("SAMPLE TEXT"))
        self.t_user.setItem(0, 1, QTableWidgetItem("SAMPLE TEXT"))
        self.t_user.setItem(0, 2, QTableWidgetItem("SAMPLE TEXT"))
        self.t_user.setItem(0, 3, QTableWidgetItem("SAMPLE TEXT"))
        self.t_user.setItem(0, 4, QTableWidgetItem("SAMPLE TEXT"))

        b_user_update = QPushButton('Обновить', self)
        # b_user_update.clicked.connect(self.on_click_user_update)

        layout.addRow(self.e_search)
        layout.addWidget(self.t_user)
        layout.addWidget(b_user_update)

        create_sport_tab.setLayout(layout)
        return create_sport_tab

    # GUI для TAB Просмотра матчей
    def show_sport_ui(self) -> QWidget:
        show_sport_tab = QWidget()
        layout = QFormLayout()

        self.e_name_up = QLineEdit()
        self.e_pass_up = QLineEdit()
        self.e_pass_up_check = QLineEdit()
        b_si_up = QPushButton('Регистрация', self)
        # b_si_up.clicked.connect(self.on_click_sign_up)

        layout.addRow('Логин', self.e_name_up)
        layout.addRow('Пароль', self.e_pass_up)
        layout.addRow('Повт. пароль', self.e_pass_up_check)
        layout.addRow(b_si_up)

        show_sport_tab.setLayout(layout)
        return show_sport_tab


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
        print('Пароль :', self.e_pass_up.text())
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

