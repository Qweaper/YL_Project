import sys
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


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
    def __init__(self, high, weigh, mines, excpt):
        self.high = high
        self.weigh = weigh
        self.mines = mines
        # создание случайных номеров мин
        numbers = list(range(0, high * weigh))
        numbers.remove(excpt - 1)  # для себя: возможно придеться отнисать единичку в связи с рассхождением индексом кнопок
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
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 480, 480)
        self.setWindowTitle("Supper")

        arr = Sapper(16, 16, 40, 1)
        array = arr.edit_field(arr.get_field())
        self.buttons = []
        for i in range(16):
            self.buttons.append([0] * 16)
        for i in range(16):
            for j in range(16):
                self.buttons[i][j] = QPushButton(self)
                self.buttons[i][j].resize(30, 30)
                self.buttons[i][j].move(0 + i * 30, 0 + j * 30)
                self.buttons[i][j].setText("")
                self.buttons[i][j].xy = (i, j)
                self.buttons[i][j].clicked.connect(self.check)

    def check(self):
        x, y = self.sender().xy

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
