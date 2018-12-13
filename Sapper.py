import sys
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


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


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = True  # Без комментариев...
        self.initUI()
        self.i = 0
        self.j = 0
        self.mouse_btm = 1

    def initUI(self):
        self.setGeometry(300, 300, 480, 480)
        self.setWindowTitle("Supper")
        # делаем кнопочки :3
        arr = Sapper(16, 16, 40, 1)
        array = arr.get_field()
        self.buttons = []
        for i in range(16):
            self.buttons.append([0] * 16)
        self.pictures = self.buttons.copy()  # взамен кнопок в будущем
        for i in range(16):
            for j in range(16):
                self.buttons[i][j] = QPushButton(self)
                self.buttons[i][j].resize(30, 30)
                self.buttons[i][j].move(0 + i * 30, 0 + j * 30)
                self.buttons[i][j].setText("")
                self.buttons[i][j].xy = (i, j)
                self.buttons[i][j].clicked.connect(self.sap)

        self.coords = QLabel(self)
        self.coords.setText("Координаты:None, None")
        self.coords.move(30, 30)

    def open_empty_field(self, i, j):
        x = i
        y = j
        if self.field[x][y] == 0:  # проверка на пустую клетку
            for i, j in get_coords(x, y, len(self.field),
                                   len(self.field[0])):  # надо сделать другой метод открытия клетки
                self.open_empty_field(x, y)
                if self.buttons[x][y] == 0:
                    self.buttons[x][y].setEnabled(False)
                else:
                    break
        # Добвать проверку на наличие флага
        if self.field[x][y] == -1:  # Добавить метод заканчивающий игру
            self.icon = QIcon('C:/Pictures/mine.jpg')
            self.buttons[x][y].setIcon(self.icon)
        else:
            self.icon = QIcon('C:/Цифры/{}.jpg'.format(self.field[x][y]))
            self.buttons[x][y].setIcon(self.icon)

    def sap(self):
        x, y = self.sender().xy
        print(self.i, self.j)
        if self.flag:
            self.trash = Sapper(16, 16, 40, x * 16 + y)
            self.field = self.trash.edit_field(self.trash.get_field())
            self.flag = False
        for i in self.field:
            for j in i:
                print(j, end=' ')
            print('\t')
        if self.field[x][y] == 0:  # проверка на пустую клетку
            self.open_empty_field(x, y)# надо сделать другой метод открытия клетки
            self.buttons[x][y].setEnabled(False)
            # проверку на клетку с флагом делать не надо, так как открыть клетку с флагом нельзя
        if self.field[x][y] == -1:
            self.icon = QIcon('C:/Pictures/mine.jpg')
            self.buttons[x][y].setIcon(self.icon)
        else:
            self.icon = QIcon('C:/Цифры/{}.jpg'.format(self.field[x][y]))
            self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 2:
        #     self.icon = QIcon('C:/Цифры/2.jpg')
        #     self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 3:
        #     self.icon = QIcon('C:/Цифры/3.jpg')
        #     self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 4:
        #     self.icon = QIcon('C:/Цифры/4.jpg')
        #     self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 5:
        #     self.icon = QIcon('C:/Цифры/5.jpg')
        #     self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 6:
        #     self.icon = QIcon('C:/Цифры/6.jpg')
        #     self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 7:
        #     self.icon = QIcon('C:/Цифры/7.jpg')
        #     self.buttons[x][y].setIcon(self.icon)
        # elif self.field[x][y] == 8:
        #     self.icon = QIcon('C:/Цифры/8.jpg')
        #     self.buttons[x][y].setIcon(self.icon)

    def mousePressEvent(self, event):
        self.i = event.x() // 30
        self.j = event.y() // 30
        self.coords.setText("Координаты:{}, {}".format(event.x(), event.y()))
        print(self.i, self.j)  # флажок на наличие клика мышки
        if event.button() == Qt.RightButton:
            self.mouse_btm = event.button()
            icon = QIcon('')
            if self.buttons[self.i][self.j].icon():
                self.buttons[self.i][self.j].setIcon(QIcon())
            else:
                self.buttons[self.i][self.j].setIcon(icon)
        # self.buttons[self.i][self.j].clicked.connect(self.sap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
