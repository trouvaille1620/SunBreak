# from PyQt5 import QtCore
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QPushButton, QLineEdit, QTextBrowser

# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class WindowDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(WindowDemo, self).__init__()
        self.setup_ui()
        # self.add_shadow()

    def setup_ui(self):

        self.setWindowOpacity(0.96)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.base_widget = QtWidgets.QWidget()
        self.base_widget.setStyleSheet('''QWidget{
                                     border-bottom-left-radius: 22px; /*右上角圆角*/;"
                                    "border-bottom-right-radius: 22px; /*左下角圆角*/;
                                    background-color:	#F5F5F5;
                                    }''')

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        self.button = QPushButton(self)
        self.button.move(400, 550)
        self.button.setFixedWidth(288)
        self.button.setFixedHeight(119)
        self.button.setStyleSheet("QPushButton{"
                                "background-image: url(./images/star3.png);\n"
                                "border-top-left-radius: 0px;"
                                "border-top-right-radius:0px;"
                                "border-bottom-left-radius:0px;"
                                "border-bottom-right-radius:0px;"
                           "}"
                            "QPushButton:hover {"
                                "background-image: url(./images/star3.png);\n"
                           "};"
                           "QPushButton:pressed {"
                                "background-image: url(./images/star3.png);\n"
                           "}")

        self.button1 = QPushButton(self)
        self.button1.move(260, 100)
        self.button1.setFixedWidth(548)
        self.button1.setFixedHeight(367)
        self.button1.setStyleSheet("QPushButton{"
                                "background-image: url(./images/first.png);\n"
                                "border-top-left-radius: 0px;"
                                "border-top-right-radius:0px;"
                                "border-bottom-left-radius:0px;"
                                "border-bottom-right-radius:0px;"
                           "}"
                            "QPushButton:hover {"
                                "background-image: url(./images/first.png);\n"
                           "};"
                           "QPushButton:pressed {"
                                "background-image: url(./images/first.png);\n"
                           "}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = WindowDemo()
    MainWindow.show()
    sys.exit(app.exec_())


