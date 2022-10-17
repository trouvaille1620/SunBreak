# -*- coding: utf-8 -*-
import json
from PyQt5 import QtWidgets
from PyQt5.Qt import *

from ..A_Shaitu import split_gongwei_QT, cut_image_QT, average_image_folder_QT, rename_img_QT, rename_hanzi_img_QT

from QT_style.style import ListWidget_Style, StackWidget_Style
file_path = r'QT_style/init_window.json'
style_dict = json.load(open(file_path, 'r'))

class Shaitu_window_StackWidget(QWidget):

    def __init__(self):
        super(Shaitu_window_StackWidget, self).__init__()
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


        list_str = ['切图', '按工位分图','按数目分图', '图片重命名', '含中文图片重命名']
        tools_str = [getattr(cut_image_QT, "Cut_image_QT_Demo"),
                     getattr(split_gongwei_QT, "Split_gongwei_QT_Demo"),
                     getattr(average_image_folder_QT, "Average_image_folder_QT_Demo"),
                     getattr(rename_img_QT, "Rename_img_QT_Demo"),
                     getattr(rename_hanzi_img_QT, "Rename_hanzi_img_QT_Demo"),
                     ]
        for i in range(5):
            self.item = QListWidgetItem(list_str[i], self.left_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(50, 50))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
            self.right_widget.addWidget(tools_str[i]())

        self.left_widget.setCurrentRow(0)

        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定
        self.left_widget.setFrameShape(QListWidget.NoFrame)  # 去掉边框
        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

