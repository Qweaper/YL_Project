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
        self.setGeometry(300, 300, 1000, 200)
        self.setWindowTitle("Supper")

        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("Кнопка 1")
        self.button_1.clicked.connect(self.run)

        self.button_2 = QPushButton(self)
        self.button_2.move(20, 80)
        self.button_2.setText("Кнопка 2")
        self.button_2.clicked.connect(self.run)

        self.show()

    def run(self):
        if self.sender().text == 'Легкий':
            pass
        if self.sender().text == 'Нормальный':
            pass
        if self.sender().text == 'Сложный':
            pass

    def easy(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
