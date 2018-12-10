import sys
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


class Sapper():
    def __init__(self, high, weigh, mines, excpt):
        self.high = high
        self.weigh = weigh
        self.mines = mines
        # создание случайных номеров мин
        numbers = set(range(0, self.high * self.weigh))
        numbers.remove(excpt)
        self.numbers_mine = set()
        for _ in range(self.mines):
            self.numbers_mine.add(choice(numbers))
        del numbers

    def get_field(self):
        field = []  # создание поля с минами
        for i in range(self.high):
            data = []
            for j in range(self.weigh):
                if i * self.weigh + j in self.numbers_mine:
                    data.append(-1)
                else:
                    data.append(0)
            field.append(data)
        # ну тут как бы пишется в клетках количество рядом стоящих мин
        for i in range(self.high):  # и да, выглядит очень больно
            for j in range(self.weigh):
                if field[i][j] == -1:
                    if i == 0 and j == 0:
                        field[i + 1][j + 1] += 1
                        field[i + 1][j] += 1
                        field[i][j + 1] += 1
                    elif i == 0 and j == self.weigh - 1:
                        field[i + 1][j - 1] += 1
                        field[i + 1][j] += 1
                        field[i][j - 1] += 1
                    elif i == self.high - 1 and j == 0:
                        field[i - 1][j + 1] += 1
                        field[i - 1][j] += 1
                        field[i][j + 1] += 1
                    elif i == self.high - 1 and j == self.weigh - 1:
                        field[i - 1][j - 1] += 1
                        field[i - 1][j] += 1
                        field[i][j - 1] += 1
                    elif i == 0:
                        field[i + 1][j - 1] += 1
                        field[i][j + 1] += 1
                        field[i + 1][j + 1] += 1
                        field[i][j - 1] += 1
                        field[i + 1][j] += 1
                    elif j == 0:
                        field[i - 1][j + 1] += 1
                        field[i][j + 1] += 1
                        field[i + 1][j + 1] += 1
                        field[i - 1][j] += 1
                        field[i + 1][j] += 1
                    elif i == self.high - 1:
                        field[i - 1][j - 1] += 1
                        field[i][j + 1] += 1
                        field[i - 1][j + 1] += 1
                        field[i][j - 1] += 1
                        field[i - 1][j] += 1
                    elif j == self.weigh - 1:
                        field[i - 1][j - 1] += 1
                        field[i][j - 1] += 1
                        field[i + 1][j - 1] += 1
                        field[i - 1][j] += 1
                        field[i + 1][j] += 1
                    else:
                        field[i + 1][j + 1] += 1
                        field[i + 1][j] += 1
                        field[i][j + 1] += 1

                        field[i - 1][j - 1] += 1
                        field[i - 1][j] += 1
                        field[i][j - 1] += 1

                        field[i - 1][j + 1] += 1
                        field[i + 1][j - 1] += 1
        return field


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
        if self.sender().text == 'Хардкор':
            pass

    def easy(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
