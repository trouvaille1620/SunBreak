import sys
import json
import platform
import subprocess
import os
import PySide2
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtGui import QIcon

from QT_windows import blank_window
from QT_windows.A_Shaitu import shaitu_window
from QT_windows.B_Biaotu import biaotu_window
from QT_windows.C_Biaozhutongji import biaozhutongji_window
from QT_windows.D_Dianjian import dianjian_window
from QT_windows.E_Biaozhunbiangeng import biaozhunbiangeng_window
from database_moudle.data_show_page import DataGrid

from QT_style.style import StackWidget_Style, Mini_Exit_Button_Style, Still_Button_Style, Normal_Button_Style
file_path = r'QT_style/Real_main_window.json'
style_dict = json.load(open(file_path, 'r'))

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class MainWidget(QtWidgets.QMainWindow, QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.app = QApplication(sys.argv)
        self.scaleRate = 1
        self.init_ui(self.scaleRate)
        self.setup_ui()
        self.add_shadow()

    def init_ui(self, scaleRate):

        self.resize(1322 * scaleRate, 830 * scaleRate)

    def setup_ui(self):

        # self.setWindowOpacity(0.97)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明----
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowIcon(QIcon('./images/shuguang.png'))

        self.base_widget = QtWidgets.QWidget()  # 创建透明窗口
        self.base_widget.setObjectName('base_widget')
        self.base_layout = QtWidgets.QGridLayout()
        self.base_widget.setLayout(self.base_layout)
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setStyleSheet('QWidget#main_widget{border-top-left-radius:25px;border-bottom-left-radius:25px;'
                                       'border-top-right-radius:0px;border-bottom-right-radius:0px;'
                                        'background-image: url(./images/background7.png);'
                                       '}' )
        self.base_layout.addWidget(self.main_widget,0,0)

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setContentsMargins(105, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 退出及最小化按钮
        self.exit = Mini_Exit_Button_Style(self, **style_dict['Exit_Button_Style'])
        self.exit.clicked.connect(self.exit_onClick_Button)

        self.mini = Mini_Exit_Button_Style(self, **style_dict['Mini_Button_Style'])
        self.mini.clicked.connect(lambda: self.showMinimized())

        self.refresh = Mini_Exit_Button_Style(self, **style_dict['Refresh_Button_Style'])
        self.refresh.clicked.connect(self.refresh_onClick_Button)

        self.homepage = Mini_Exit_Button_Style(self, **style_dict['Homepage_Button_Style'])
        self.homepage.clicked.connect(self.homepage_onClick_Button)

        # 右侧“切换界面”窗口
        self.Init_window_StackWidget = StackWidget_Style(self, **style_dict['Init_window_StackWidget_Style'])
        self.main_layout.addWidget(self.Init_window_StackWidget)

        #左侧菜单栏图标
        self.button1 = Still_Button_Style(self, **style_dict['Shaitu_Still_Button_Style'])
        self.button1.clicked.connect(self.button1_onClick_Button)

        self.button2 = Still_Button_Style(self, **style_dict['Biaotu_Still_Button_Style'])
        self.button2.clicked.connect(self.button2_onClick_Button)

        self.button3 = Still_Button_Style(self, **style_dict['Biaozhutongji_Still_Button_Style'])
        self.button3.clicked.connect(self.button3_onClick_Button)

        self.button4 = Still_Button_Style(self, **style_dict['Dianjian_Still_Button_Style'])
        self.button4.clicked.connect(self.button4_onClick_Button)

        self.button5 = Still_Button_Style(self, **style_dict['Biaozhun_Still_Button_Style'])
        self.button5.clicked.connect(self.button5_onClick_Button)

        self.button6 = Normal_Button_Style(self, **style_dict['Database_Button_Style'])
        self.button6.clicked.connect(self.button6_onClick_Button)

        self.button7 = Normal_Button_Style(self, **style_dict['VIA_Button_Style'])
        self.button7.clicked.connect(self.button7_onClick_Button)

        tools_str = [getattr(blank_window, "WindowDemo"),
                     getattr(shaitu_window, "Shaitu_window_StackWidget"),
                     getattr(biaotu_window, "Biaozhu_window_StackWidget"),
                     getattr(biaozhutongji_window, "Biaozhujiancha_window_StackWidget"),
                     getattr(dianjian_window, "Dianjian_window_StackWidget"),
                     getattr(biaozhunbiangeng_window, "Biaozhunbiangeng_window_StackWidget"),
                     ]
        for i in range(6):
            self.Init_window_StackWidget.addWidget(tools_str[i]())

    def add_shadow(self):
        # 添加阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(10)  # 阴影半径
        self.effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()
            if len(self.app.screens()) == 1:
                self.scaleRate = 1
            else:
                self.scaleRate = self.app.screens()[1].logicalDotsPerInch() / 96
            self.init_ui(self.scaleRate)
            self.add_shadow()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def exit_onClick_Button(self):
        app = QApplication.instance()  # 退出应用程序
        app.quit()

    def refresh_onClick_Button(self):
        QApplication.processEvents()  # 刷新界面
        status_bool = [False, False, False, False, False, False]
        i = self.Init_window_StackWidget.currentIndex()
        status_bool[i - 1] = True
        self.button1.setAutoExclusive(False)
        self.button1.setChecked(status_bool[0])
        self.button1.setAutoExclusive(True)
        self.button2.setAutoExclusive(False)
        self.button2.setChecked(status_bool[1])
        self.button2.setAutoExclusive(True)
        self.button3.setAutoExclusive(False)
        self.button3.setChecked(status_bool[2])
        self.button3.setAutoExclusive(True)
        self.button4.setAutoExclusive(False)
        self.button4.setChecked(status_bool[3])
        self.button4.setAutoExclusive(True)
        self.button5.setAutoExclusive(False)
        self.button5.setChecked(status_bool[4])
        self.button5.setAutoExclusive(True)
        self.button6.setAutoExclusive(False)
        self.button6.setChecked(status_bool[5])
        self.button6.setAutoExclusive(True)

    def homepage_onClick_Button(self):
        self.Init_window_StackWidget.setCurrentIndex(0)
        self.button1.setAutoExclusive(False)
        self.button1.setChecked(False)
        self.button1.setAutoExclusive(True)
        self.button2.setAutoExclusive(False)
        self.button2.setChecked(False)
        self.button2.setAutoExclusive(True)
        self.button3.setAutoExclusive(False)
        self.button3.setChecked(False)
        self.button3.setAutoExclusive(True)
        self.button4.setAutoExclusive(False)
        self.button4.setChecked(False)
        self.button4.setAutoExclusive(True)
        self.button5.setAutoExclusive(False)
        self.button5.setChecked(False)
        self.button5.setAutoExclusive(True)
        self.button6.setAutoExclusive(False)
        self.button6.setChecked(False)
        self.button6.setAutoExclusive(True)

    def button1_onClick_Button(self):
        self.Init_window_StackWidget.setCurrentIndex(1)

    def button2_onClick_Button(self):
        self.Init_window_StackWidget.setCurrentIndex(2)

    def button3_onClick_Button(self):
        self.Init_window_StackWidget.setCurrentIndex(3)

    def button4_onClick_Button(self):
        self.Init_window_StackWidget.setCurrentIndex(4)

    def button5_onClick_Button(self):
        self.Init_window_StackWidget.setCurrentIndex(5)

    def button6_onClick_Button(self):
        self.datapage = DataGrid()
        self.datapage.show()

    def button7_onClick_Button(self):
        fp = r'via-src-2.0.11/dist/via.html'
        systemType: str = platform.platform()  # 获取系统类型
        if 'mac' in systemType:  # 判断以下当前系统类型
            fp: str = fp.replace("\\", "/")  # mac系统下,遇到`\\`让路径打不开,不清楚为什么哈,觉得没必要的话自己可以删掉啦,18行那条也是
            subprocess.call(["open", fp])
        else:
            fp: str = fp.replace("/", "\\")  # win系统下,有时`/`让路径打不开
            os.startfile(fp)


def main():

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_wnd = MainWidget()
    main_wnd.show()
    app.exec()


if __name__ == '__main__':
    main()