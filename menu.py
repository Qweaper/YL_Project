# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_menu.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName("Menu")
        Menu.resize(300, 295)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("GUI/picks/min.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Menu.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(60, 10, 180, 80))
        font = QtGui.QFont()
        font.setFamily("Padauk Book [PYRS]")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.t_high = QtWidgets.QLabel(self.centralwidget)
        self.t_high.setGeometry(QtCore.QRect(40, 110, 58, 18))
        self.t_high.setObjectName("t_high")
        self.t_lengh = QtWidgets.QLabel(self.centralwidget)
        self.t_lengh.setGeometry(QtCore.QRect(40, 160, 58, 18))
        self.t_lengh.setObjectName("t_lengh")
        self.t_mine = QtWidgets.QLabel(self.centralwidget)
        self.t_mine.setGeometry(QtCore.QRect(40, 210, 81, 18))
        self.t_mine.setObjectName("t_mine")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setEnabled(True)
        self.start.setGeometry(QtCore.QRect(0, 260, 300, 34))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("GUI/picks/flag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("GUI/picks/flag.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.start.setIcon(icon1)
        self.start.setObjectName("start")
        self.high = QtWidgets.QLineEdit(self.centralwidget)
        self.high.setGeometry(QtCore.QRect(150, 110, 113, 30))
        self.high.setObjectName("high")
        self.lengh = QtWidgets.QLineEdit(self.centralwidget)
        self.lengh.setGeometry(QtCore.QRect(150, 160, 113, 30))
        self.lengh.setObjectName("lengh")
        self.mines = QtWidgets.QLineEdit(self.centralwidget)
        self.mines.setGeometry(QtCore.QRect(150, 210, 113, 30))
        self.mines.setObjectName("mines")
        Menu.setCentralWidget(self.centralwidget)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        _translate = QtCore.QCoreApplication.translate
        Menu.setWindowTitle(_translate("Menu", "Сапёр"))
        self.name.setText(_translate("Menu", "Сапёр"))
        self.t_high.setText(_translate("Menu", "Длинна"))
        self.t_lengh.setText(_translate("Menu", "Высота"))
        self.t_mine.setText(_translate("Menu", "Кол-во мин"))
        self.start.setText(_translate("Menu", "Start Game"))

