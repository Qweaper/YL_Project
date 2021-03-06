import sys
from PyQt5 import QtGui
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from menu import Ui_Menu


# ну это костыль :D
def get_coords(i, j, maxi, maxj):
    if i == 0 and j == 0:
        return (i + 1, j), (i, j + 1), (i + 1, j + 1)
    elif i == 0 and j == maxj - 1:
        return (i + 1, j), (i, j - 1), (i + 1, j - 1)
    elif i == maxi - 1 and j == 0:
        return (i - 1, j), (i, j + 1), (i - 1, j + 1)
    elif i == maxi - 1 and j == maxj - 1:
        return (i - 1, j), (i, j - 1), (i - 1, j - 1)
    elif i == 0:
        return (i, j - 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1), (i, j + 1)
    elif i == maxi - 1:
        return (i, j - 1), (i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1)
    elif j == 0:
        return (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j)
    elif j == maxj - 1:
        return (i - 1, j), (i - 1, j - 1), (i, j - 1), (i + 1, j - 1), (i + 1, j)
    return (i + 1, j), (i, j + 1), (i + 1, j + 1), (i - 1, j), (i, j - 1), (i - 1, j - 1), (i + 1, j - 1), (
        i - 1, j + 1)


class MyWidget(QMainWindow, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start.clicked.connect(self.start_game)
        self.move(300, 300)
        # self.windowIconChanged(QIcon('GUI/picks/min.png'))
        self.lengh.setText('0')
        self.mines.setText('0')
        self.high.setText('0')
        self.playground = 0

    def start_game(self):
        self.playground = PlayGround(int(self.high.text()), int(self.lengh.text()), int(self.mines.text()))
        self.playground.show()


class Sapper(object):
    def __init__(self, high, weigh, mines):
        self.high = high
        self.weigh = weigh
        self.mines = mines
        # создание случайных номеров мин
        numbers = list(range(0, high * weigh))

        self.numbers_mine = set()
        for _ in range(min(self.mines, high * weigh)):
            random_mine = choice(numbers)
            self.numbers_mine.add(random_mine)
            numbers.remove(random_mine)
        numbers.clear()

    def get_field(self):
        field = []  # создание пустого поля
        for i in range(self.high):
            data = []
            for j in range(self.weigh):
                data.append(0)
            field.append(data)
        return field

    def edit_field(self, field):
        edited_field = field.copy()  # ставим мины
        for i in range(self.high):
            for j in range(self.weigh):
                if i * self.weigh + j in self.numbers_mine:
                    edited_field[i][j] = -1

        # ну тут как бы пишется в клетках количество рядом стоящих мин
        for i in range(self.high):
            for j in range(self.weigh):
                if edited_field[i][j] == -1:
                    for i1, j1 in get_coords(i, j, self.high, self.weigh):
                        if edited_field[i1][j1] != -1:
                            edited_field[i1][j1] += 1
        return edited_field

    # def get_coords_mines(self):
    #     numbers = set()
    #     for number_mine in self.numbers_mine:
    #         x, y = number_mine // self.weigh, number_mine % self.weigh
    #         numbers.add((x, y))
    #     return numbers  # озвращаем координаты мины в виде множества с кортежами


class PlayGround(QWidget):
    def __init__(self, high, lengh, mines):
        super(PlayGround, self).__init__()
        self.lengh_param = lengh
        self.mines_param = mines
        self.high_param = high
        # print('lOL')

        self.flag = True  # Без комментариев...
        self.initUI()
        self.i = 0
        self.j = 0
        # self.coords_mines = set()
        # self.open_square = set()
        # self.coords_flags = set()
        self.flag_checker_list = {}
        self.mouse_btm = 1
        self.off_square = set()
        self.num_of_flags = mines
        self.trash = [[]]
        self.field = [[]]  # Надо будет добавить количество мин равное количеству флагов

    def initUI(self):
        self.flags = QLabel(self)
        self.flags.setText('Кол-во флагов: {}'.format(self.mines_param))
        self.flags.move(0, 30 * self.lengh_param)
        self.flags.resize(150, 20)
        # self.setGeometry(300, 300, 480, 500)
        self.setGeometry(300, 300, 30 * self.high_param, 30 * self.lengh_param + 20)
        self.setWindowTitle("Supper")
        # делаем кнопочки :3
        # arr = Sapper(16, 16, 40, 1)
        # array = arr.get_field()
        self.buttons = []
        for i in range(self.high_param):
            self.buttons.append([0] * self.lengh_param)
        for i in range(self.high_param):
            for j in range(self.lengh_param):
                self.buttons[i][j] = QPushButton(self)
                self.buttons[i][j].resize(30, 30)
                self.buttons[i][j].move(0 + i * 30, 0 + j * 30)
                self.buttons[i][j].setText("")
                self.buttons[i][j].xy = (i, j)
                self.buttons[i][j].clicked.connect(self.sap)
        self.show()

    def open_empty_field(self, i, j):
        x = i
        y = j

        if self.field[x][y] == 0:  # проверка на пустую клетку
            self.buttons[x][y].setEnabled(False)
            for i, j in get_coords(x, y, len(self.field), len(self.field[0])):
                if self.field[i][j] == 0 and (i, j) not in self.off_square and (
                        i, j) not in self.flag_checker_list.keys():
                    self.buttons[x][y].setEnabled(False)
                    # self.open_square.add((x, y))
                    self.off_square.add((i, j))
                    self.open_empty_field(i, j)
                elif self.field[i][j] >= 1:
                    self.buttons[i][j].click()

                elif self.field[i][j] != 0:
                    break
        else:
            return

    def sap(self):
        x, y = self.sender().xy
        # print(self.i, self.j)
        if self.flag:
            self.trash = Sapper(self.high_param, self.lengh_param, self.mines_param)
            self.field = self.trash.edit_field(self.trash.get_field())
            self.flag = False
        if (x, y) in self.flag_checker_list.keys():
            pass
        elif self.field[x][y] == 0:  # проверка на пустую клетку
            self.open_empty_field(x, y)  # надо сделать другой метод открытия клетки
            self.buttons[x][y].setEnabled(False)
            # self.open_square.add((x, y))
            # проверку на клетку с флагом делать не надо, так как открыть клетку с флагом нельзя
        elif self.field[x][y] == -1:
            icon1 = QIcon('GUI/picks/min.png'.format(self.field[x][y]))
            icon1.addPixmap(QPixmap('GUI/picks/min.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon1.addPixmap(QPixmap('GUI/picks/min.png'), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.buttons[x][y].setEnabled(False)
            # self.open_square.add((x, y))
            self.buttons[x][y].setIcon(icon1)
            self.game_over()
        else:
            icon1 = QIcon('GUI/Цифры/{}.jpg'.format(self.field[x][y]))
            icon1.addPixmap(QPixmap('GUI/Цифры/{}.jpg'.format(self.field[x][y])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon1.addPixmap(QPixmap('GUI/Цифры/{}.jpg'.format(self.field[x][y])), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.buttons[x][y].setEnabled(False)
            # self.open_square.add((x, y))
            self.buttons[x][y].setIcon(icon1)
        # if self.player_victory_check():
        #     self.win_game()

    def mousePressEvent(self, event):
        self.i = event.x() // 30
        self.j = event.y() // 30
        if event.button() == Qt.RightButton:
            self.mouse_btm = event.button()
            icon = QIcon('GUI/picks/flag.png')
            if (self.i, self.j) in self.flag_checker_list.keys():
                self.buttons[self.i][self.j].setIcon(QIcon())
                self.flag_checker_list.pop((self.i, self.j))
                self.num_of_flags += 1
                # self.coords_flags.add((self.i, self.j))
                self.flags.setText('Кол-во флагов: {}'.format(self.num_of_flags))
            else:
                if self.num_of_flags <= 0:
                    return
                self.buttons[self.i][self.j].setIcon(icon)
                self.flag_checker_list[(self.i, self.j)] = True
                self.num_of_flags -= 1
                # self.coords_flags.remove((self.i, self.j))
                self.flags.setText('Кол-во флагов: {}'.format(self.num_of_flags))
                if self.num_of_flags == 0:
                    self.win_game()
            # self.buttons[self.i][self.j].clicked.connect(self.sap)
        # if self.player_victory_check():
        #     self.win_game()

    def game_over(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if (i, j) in self.flag_checker_list.keys() and self.field[i][j] != -1:
                    icon1 = QIcon('GUI/picks/f_tick.png'.format(self.field[i][j]))
                    icon1.addPixmap(QPixmap('GUI/picks/f_tick.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    icon1.addPixmap(QPixmap('GUI/picks/f_tick.png'), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                    self.buttons[i][j].setIcon(icon1)
                    self.buttons[i][j].setEnabled(False)
                elif (i, j) in self.flag_checker_list.keys() and self.field[i][j] == -1:
                    icon1 = QIcon('GUI/picks/r_tick.png'.format(self.field[i][j]))
                    icon1.addPixmap(QPixmap('GUI/picks/r_tick.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    icon1.addPixmap(QPixmap('GUI/picks/r_tick.png'), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                    self.buttons[i][j].setIcon(icon1)
                    self.buttons[i][j].setEnabled(False)
                elif self.field[i][j] == -1:
                    self.buttons[i][j].click()
                elif self.field[i][j] >= 1:
                    icon1 = QIcon('GUI/Цифры/{}.jpg'.format(self.field[i][j]))
                    icon1.addPixmap(QPixmap('GUI/Цифры/{}.jpg'.format(self.field[i][j])), QtGui.QIcon.Normal,
                                    QtGui.QIcon.Off)
                    icon1.addPixmap(QPixmap('GUI/Цифры/{}.jpg'.format(self.field[i][j])), QtGui.QIcon.Disabled,
                                    QtGui.QIcon.Off)
                    self.buttons[i][j].setEnabled(False)
                    self.buttons[i][j].setIcon(icon1)
                else:
                    self.buttons[i][j].setEnabled(False)

    def player_victory_check(self):
        predicted_mines = 0
        for i, j in self.flag_checker_list.keys():
            if self.field[i][j] == -1:
                predicted_mines += 1
        if predicted_mines == self.mines_param:
            self.win_game()

    #     self.coords_mines = self.trash.get_coords_mines()
    #     print(self.coords_mines)
    #     print(self.coords_flags)
    #     print(self.open_square)
    #     if len(self.coords_mines) + len(
    #             self.open_square) == self.lengh_param * self.high_param and self.coords_mines == self.coords_flags:
    #         return True
    #     return False

    def win_game(self):
        self.win = QMessageBox(self)
        self.win.show()
        self.win.setText("Вы победили!")
        self.game_over()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
