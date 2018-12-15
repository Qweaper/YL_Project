import sys
from PyQt5 import QtGui
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QDialog, QMainWindow
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

    def start_game(self):
        self.playground = PlayGround(int(self.high.text()), int(self.lengh.text()), int(self.mines.text()))
        # playground = PlayGround()
        self.playground.show()



class Sapper(object):
    def __init__(self, high, weigh, mines, excpt=None):
        self.high = high
        self.weigh = weigh
        self.mines = mines
        if excpt:
            # создание случайных номеров мин
            numbers = list(range(0, high * weigh))
            numbers.remove(
                excpt - 1)  # для себя: возможно придеться отнисать единичку в связи с рассхождением индексом кнопок
            ouch = (excpt - 1) // weigh
            for i1, j1 in get_coords(ouch, excpt - (high * ouch) - 1, high, weigh):
                numbers.remove(i1 * weigh + j1)
            self.numbers_mine = set()
            for _ in range(self.mines):
                self.numbers_mine.add(choice(numbers))
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

    def get_coords_mines(self):
        return self.numbers_mine  # озвращаем координаты мины в виде множества с кортежами


class PlayGround(QWidget):
    def __init__(self, high, lenth, mines):
        super(PlayGround, self).__init__()
        self.lengh_param = mines
        self.mines_param = lenth
        self.high_param = high
        print('lOL')

        self.flag = True  # Без комментариев...
        self.initUI()
        self.i = 0
        self.j = 0
        self.coords_flags = set()
        self.flag_checker_list = {}
        self.mouse_btm = 1
        self.off_square = set()
        self.num_of_flags = 0
        self.trash = [[]]
        self.field = [[]]  # Надо будет добавить количество мин равное количеству флагов

    def initUI(self):
        self.flags = QLabel(self)
        self.flags.setText('Кол-во флагов: {}'.format(0))
        # self.flags.move(0, 480)
        self.flags.move(0, 30 * self.high_param)
        self.flags.resize(150, 20)
        # self.setGeometry(300, 300, 480, 500)
        self.setGeometry(300, 300, 30 * self.lengh_param, 30 * self.high_param + 20)
        self.setWindowTitle("Supper")
        # делаем кнопочки :3
        # arr = Sapper(16, 16, 40, 1)
        # array = arr.get_field()
        self.buttons = []
        for i in range(self.mines_param):
            self.buttons.append([0] * self.mines_param)
        for i in range(self.high_param):
            for j in range(self.mines_param):
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
                if self.field[i][j] == 0 and (i, j) not in self.off_square:
                    self.buttons[x][y].setEnabled(False)
                    self.off_square.add((i, j))
                    self.open_empty_field(i, j)
                elif self.field[i][j] >= 1:
                    self.buttons[i][j].click()
                    break
                elif self.field[i][j] != 0:
                    break
        else:
            return

    def sap(self):
        x, y = self.sender().xy
        # print(self.i, self.j)
        if self.flag:
            self.trash = Sapper(self.high_param, self.lengh_param, self.mines_param, x * self.high_param + y)
            self.field = self.trash.edit_field(self.trash.get_field())
            self.flag = False
        if self.field[x][y] == 0:  # проверка на пустую клетку
            self.open_empty_field(x, y)  # надо сделать другой метод открытия клетки
            self.buttons[x][y].setEnabled(False)
            # проверку на клетку с флагом делать не надо, так как открыть клетку с флагом нельзя
        elif (x, y) in self.flag_checker_list.keys():
            pass
        elif self.field[x][y] == -1:
            icon1 = QIcon('GUI/picks/min.png'.format(self.field[x][y]))
            icon1.addPixmap(QPixmap('GUI/picks/min.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon1.addPixmap(QPixmap('GUI/picks/min.png'), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.buttons[x][y].setEnabled(False)
            self.buttons[x][y].setIcon(icon1)
            self.game_over()
        else:
            icon1 = QIcon('GUI/Цифры/{}.jpg'.format(self.field[x][y]))
            icon1.addPixmap(QPixmap('GUI/Цифры/{}.jpg'.format(self.field[x][y])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon1.addPixmap(QPixmap('GUI/Цифры/{}.jpg'.format(self.field[x][y])), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.buttons[x][y].setEnabled(False)
            self.buttons[x][y].setIcon(icon1)

    def mousePressEvent(self, event):
        self.i = event.x() // 30
        self.j = event.y() // 30
        if event.button() == Qt.RightButton:
            self.mouse_btm = event.button()
            icon = QIcon('GUI/picks/flag.png')
            if (self.i, self.j) in self.flag_checker_list.keys():
                try:
                    self.buttons[self.i][self.j].setIcon(QIcon())
                    self.flag_checker_list.pop((self.i, self.j))
                    self.num_of_flags += 1
                    self.flags.setText('Кол-во флагов: {}'.format(self.num_of_flags))
                except PlayGround:
                    pass
            else:
                self.buttons[self.i][self.j].setIcon(icon)
                self.flag_checker_list[(self.i, self.j)] = True
                self.num_of_flags -= 1
                self.flags.setText('Кол-во флагов: {}'.format(self.num_of_flags))
            # self.buttons[self.i][self.j].clicked.connect(self.sap)

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
        mines = self.trash.get_coords_mines()
        flags = self.coords_flags

    def win_game(self):
        # for i in range(16):
        # for j in range(16):
        #     if self.field[i][j] == -1 and self.flag_checker_list[i][j] is True:
        question = ()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
