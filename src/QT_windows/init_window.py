import sys
import json
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from QT_windows import bp2jpg_thr_QT, bp2jpg_thr_QT_old, blank_window

from QT_style.style import ListWidget_Style, StackWidget_Style
file_path = r'QT_style/init_window.json'
style_dict = json.load(open(file_path, 'r'))

class Init_window_StackWidget(QWidget):

    def __init__(self):
        super(Init_window_StackWidget, self).__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setWindowOpacity(0.96)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.resize(1080, 830)

        self.base_widget = QtWidgets.QWidget()  # 创建透明窗口
        self.base_widget.setObjectName('base_widget')
        self.base_layout = QtWidgets.QGridLayout()
        self.base_widget.setLayout(self.base_layout)
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)

        self.base_layout = QHBoxLayout(self)  # 窗口的整体布局
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 左侧功能列表和右侧功能界面的样式
        self.left_widget = ListWidget_Style(self, **style_dict['Left_ListWidget_Style']) # 左侧选项列表样式
        self.right_widget = StackWidget_Style(self, **style_dict['Right_StackWidget_Style'])  # 右侧堆叠窗口样式

        self.base_layout.addWidget(self.left_widget)
        self.base_layout.addWidget(self.right_widget)
        self.base_layout.setSpacing(0)
        self.center()

        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定
        self.left_widget.setFrameShape(QListWidget.NoFrame)  # 去掉边框
        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        list_str = ['首页', 'bmp转jpg_test', 'bmp转jpg', '切分project', '按工位分图']
        tools_str = [getattr(blank_window, "WindowDemo"), getattr(bp2jpg_thr_QT_old, "bp2jpg_thr_Window"),
                     getattr(bp2jpg_thr_QT, "Bp2jpg_thr_QT_Demo"),]
        for i in range(5):
            self.item = QListWidgetItem(list_str[i], self.left_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(50, 50))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
            self.right_widget.addWidget(tools_str[i]())


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def exit_onClick_Button(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()


def main():
    app = QApplication(sys.argv)
    main_wnd = Init_window_StackWidget()
    main_wnd.show()
    app.exec()


if __name__ == '__main__':
    main()