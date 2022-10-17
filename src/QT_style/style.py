# from PyQt5 import QtCore
import re
import os
import cv2
import numpy as np
import threading
import shutil
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView, QMainWindow
from PyQt5.QtWidgets import QRadioButton, QMessageBox, QButtonGroup, QTextBrowser
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QPushButton, QLineEdit, QComboBox
from PyQt5.Qt import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor, QCursor
from PyQt5.QtCore import Qt
# from PyQt5.QtCore.Qt import AA_EnableHighDpiScaling

# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

#上层左侧菜单栏的样式
class ListWidget_Style(QListWidget):
    def __init__(self, parent=None, **kwargs):  #需要传入宽w、高h、圆角大小[左上，右上，左下，右下]、背景颜色 \"%s\"
        super(ListWidget_Style, self).__init__(parent=parent)
        self.TranslucentBackground = kwargs['TranslucentBackground']
        self.w_min = kwargs['QStackedWidget']["min-width"]
        self.h_min = kwargs['QStackedWidget']["min-height"]
        self.w_max = kwargs['QStackedWidget']["max-width"]
        self.h_max = kwargs['QStackedWidget']["max-height"]
        self.background_color = kwargs['QStackedWidget']["background"]
        self.border_top_left_radius = kwargs['QStackedWidget']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QStackedWidget']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QStackedWidget']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QStackedWidget']['border-bottom-right-radius']
        self.Item_no_selected_backgorund = kwargs['QListWidget::Item:!selected']['background']
        self.Item_no_selected_color = kwargs['QListWidget::Item:!selected']['color']
        self.Item_selected_backgorund = kwargs['QListWidget::Item:selected']['background']
        self.Item_selected_color = kwargs['QListWidget::Item:selected']['color']
        self.Item_hover_backgorund = kwargs['QListWidget::Item:hover']['background']
        self.Item_hover_color = kwargs['QListWidget::Item:hover']['color']
        self.setup_ui()
        # print("style_left_widget", self.size())

    def setup_ui(self):
        if self.TranslucentBackground == 'True':
            self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet("QListWidget {"
                               "min-width: \"%s\"; max-width: \"%s\";min-height: \"%s\";max-height: \"%s\";"
                               "border-top-left-radius: \"%s\";"
                               "border-top-right-radius:\"%s\";"
                               "border-bottom-left-radius:\"%s\";"
                               "border-bottom-right-radius:\"%s\";"
                               "background:\"%s\""
                           "}" 
                           "QListWidget::Item:!selected {"
                                "background:\"%s\";"
                                "color:\"%s\";font-weight:600"
                           "}"
                           "QListWidget::Item:selected {"
                                "background:\"%s\";"
                                "color:\"%s\";font-weight:600"
                           "}"
                            "QListWidget::Item:hover {"
                                "background:\"%s\";"
                                "color:\"%s\";font-weight:600"
                           "}"
                           % (self.w_min, self.w_max, self.h_min, self.h_max,
                              self.border_top_left_radius, self.border_top_right_radius,
                              self.border_bottom_left_radius,self.border_bottom_right_radius,
                              self.background_color,
                              self.Item_no_selected_backgorund,self.Item_no_selected_color,
                              self.Item_selected_backgorund, self.Item_selected_color,
                              self.Item_hover_backgorund, self.Item_hover_color
                              )
                            )

#底层右侧显示界面的样式
class StackWidget_Style(QStackedWidget):
    def __init__(self, parent=None, **kwargs):  #需要传入宽w、高h、圆角大小[左上，右上，左下，右下]、背景颜色
        super(StackWidget_Style, self).__init__(parent=parent)
        self.TranslucentBackground = kwargs['TranslucentBackground']
        self.w_min = kwargs['QStackedWidget']["min-width"]
        self.h_min = kwargs['QStackedWidget']["min-height"]
        self.w_max = kwargs['QStackedWidget']["max-width"]
        self.h_max = kwargs['QStackedWidget']["max-height"]
        self.background_color = kwargs['QStackedWidget']["background"]
        self.border_top_left_radius = kwargs['QStackedWidget']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QStackedWidget']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QStackedWidget']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QStackedWidget']['border-bottom-right-radius']
        self.setup_ui()

    def setup_ui(self):
        if self.TranslucentBackground == 'True':
            self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet("QStackedWidget {"
                               "min-width: \"%s\"; max-width: \"%s\";min-height: \"%s\";max-height:\"%s\";"
                               "border-top-left-radius: \"%s\";"
                               "border-top-right-radius:\"%s\";"
                               "border-bottom-left-radius:\"%s\";"
                               "border-bottom-right-radius:\"%s\";"
                               "background:url(\"%s\")"
                            "}"
                            % (self.w_min,self.w_max, self.h_min, self.h_max,
                               self.border_top_left_radius, self.border_top_right_radius,
                               self.border_bottom_left_radius, self.border_bottom_right_radius,
                               self.background_color
                               )
                               )

#一般widget的样式
class Normal_Widget_Style(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):  # 需要传入背景图片、圆角大小
        super(Normal_Widget_Style, self).__init__(parent=parent)
        self.TranslucentBackground = kwargs['TranslucentBackground']
        self.background_color = kwargs['QWidget']["background"]
        self.border_top_left_radius = kwargs['QWidget']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QWidget']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QWidget']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QWidget']['border-bottom-right-radius']
        self.setup_ui()

    def setup_ui(self):
        if self.TranslucentBackground == 'True':
            self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet('QWidget{''background-color:\"%s\";'
                                     "border-top-left-radius: \"%s\";"
                                     "border-top-right-radius:\"%s\";"
                                     "border-bottom-left-radius:\"%s\";"
                                     "border-bottom-right-radius:\"%s\";"
                                       '}'
                                       % (self.background_color,
                                          self.border_top_left_radius, self.border_top_right_radius,
                                          self.border_bottom_left_radius, self.border_bottom_right_radius
                                          )
                                       )

#最小化、退出的样式
class Mini_Exit_Button_Style(QPushButton): #需要传入x坐标、y坐标、背景图片、宽w、高h、圆角大小[左上，右上，左下，右下]、hover背景颜色
    def __init__(self, parent=None, **kwargs):
        super(Mini_Exit_Button_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.background_image = kwargs['QPushButton']['background-image']
        self.background_position = kwargs['QPushButton']['background_position']
        self.background_repeat = kwargs['QPushButton']['background_repeat']
        self.border_top_left_radius = kwargs['QPushButton']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QPushButton']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QPushButton']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QPushButton']['border-bottom-right-radius']
        self.hover_color = kwargs['QPushButton_hover']['background-color']
        self.pressed_color = kwargs['QPushButton_pressed']['background-color']
        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setFixedWidth(int(self.w))
        self.setStyleSheet("QPushButton{"
                                "background-image: url(\"%s\");\n"
                                "background-position:\"%s\";\n"
                                "background-repeat:\"%s\";\n"
                                "border-top-left-radius: \"%s\";"
                                "border-top-right-radius:\"%s\";"
                                "border-bottom-left-radius:\"%s\";"
                                "border-bottom-right-radius:\"%s\";"
                           "}"
                            "QPushButton:hover {"
                                "background-color:\"%s\";"
                           "};"
                           "QPushButton:pressed {"
                                "background-color:\"%s\""
                           "}"
                           % (self.background_image,
                              self.background_position, self.background_repeat,
                              self.border_top_left_radius, self.border_top_right_radius,
                              self.border_bottom_left_radius, self.border_bottom_right_radius,
                              self.hover_color,self.pressed_color
                              )
                           )

# 保持状态按钮的样式
class Still_Button_Style(QPushButton):
    def __init__(self, parent=None, **kwargs):  # 需要传入背景图片、x坐标、y坐标、宽w、高h、圆角大小[左上，右上，左下，右下]、hover背景颜色
        super(Still_Button_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.border_image = kwargs['QPushButton']['border-image']
        self.border_top_left_radius = kwargs['QPushButton']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QPushButton']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QPushButton']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QPushButton']['border-bottom-right-radius']
        self.hover_image = kwargs['QPushButton_hover']['border-image']
        self.pressed_image = kwargs['QToolButton_checked']['border-image']
        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setFixedWidth(int(self.w))
        self.setFixedHeight(int(self.h))
        self.setCheckable(True)
        self.setAutoExclusive(True)

        self.setStyleSheet("QPushButton{border-image: url(\"%s\");"
                                "border-top-left-radius: \"%s\";"
                                "border-top-right-radius:\"%s\";"
                                "border-bottom-left-radius:\"%s\";"
                                "border-bottom-right-radius:\"%s\";}"
                           "QPushButton:hover{border-image: url(\"%s\");}"
                           "QPushButton::checked,QToolButton::checked{border-image: url(\"%s\");}"
                           % (self.border_image,
                              self.border_top_left_radius, self.border_top_right_radius,
                              self.border_bottom_left_radius, self.border_bottom_right_radius,
                              self.hover_image, self.pressed_image
                              )
                           )

#一般按钮的样式
class Normal_Button_Style(QPushButton): #需要传入x坐标、y坐标、背景图片、宽w、高h、圆角大小[左上，右上，左下，右下]、hover背景颜色
    def __init__(self, parent=None, **kwargs):
        super(Normal_Button_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.background_image = kwargs['QPushButton']['background-image']
        self.background_position = kwargs['QPushButton']['background_position']
        self.background_repeat = kwargs['QPushButton']['background_repeat']
        self.border_top_left_radius = kwargs['QPushButton']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QPushButton']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QPushButton']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QPushButton']['border-bottom-right-radius']
        self.hover_image = kwargs['QPushButton_hover']['background-image']
        self.pressed_image = kwargs['QPushButton_pressed']['background-image']
        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setFixedWidth(int(self.w))
        self.setFixedHeight(int(self.h))
        self.setStyleSheet("QPushButton{"
                                "background-image: url(\"%s\");\n"
                                "background-position:\"%s\";\n"
                                "background-repeat:\"%s\";\n"
                                "border-top-left-radius: \"%s\";"
                                "border-top-right-radius:\"%s\";"
                                "border-bottom-left-radius:\"%s\";"
                                "border-bottom-right-radius:\"%s\";"
                           "}"
                            "QPushButton:hover {"
                                "background-image: url(\"%s\");\n"
                           "};"
                           "QPushButton:pressed {"
                                "background-image: url(\"%s\");\n"
                           "}"
                           % (self.background_image,
                              self.background_position, self.background_repeat,
                              self.border_top_left_radius, self.border_top_right_radius,
                              self.border_bottom_left_radius, self.border_bottom_right_radius,
                              self.hover_image,
                              self.pressed_image
                              )
                           )

#一般文本标题的样式
class Normal_Qlabel_Style(QLabel):
    def __init__(self, parent=None, **kwargs):  # 需要传入背景图片、x坐标、y坐标、宽w、字体颜色、字体
        super(Normal_Qlabel_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.content = kwargs['content']
        self.content_format = kwargs['content_format']
        self.content_size = kwargs['content_size']
        self.content_color = kwargs['content_color']

        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setText(self.content)
        self.setFont(QFont(self.content_format, int(self.content_size)))
        self.setStyleSheet("QLabel{background-color:transparent ;color:\"%s\";}"
                           % (self.content_color
                              )
                           )
        # self.setStyleSheet("QLabel{color:#FFFFFF ;}")

#一般单行文本输入框的样式
class Normal_QLineEdit_Style(QLineEdit):
    def __init__(self, parent=None, **kwargs):  # 需要传入背景颜色、圆角、边粗细、边颜色、点击变色
        super(Normal_QLineEdit_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.background_color = kwargs['QLineEdit']['background-color']
        self.border_top_left_radius = kwargs['QLineEdit']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QLineEdit']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QLineEdit']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QLineEdit']['border-bottom-right-radius']
        self.content_format = kwargs['content_format']
        self.content_size = kwargs['content_size']
        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setFixedWidth(int(self.w))
        self.setFixedHeight(int(self.h))
        self.setFont(QFont(self.content_format, int(self.content_size)))
        self.setStyleSheet("QLineEdit{background-color:\"%s\";"
                               "border-top-left-radius: \"%s\";"
                               "border-top-right-radius:\"%s\";"
                               "border-bottom-left-radius:\"%s\";"
                               "border-bottom-right-radius:\"%s\";"
                               "border: 1px solid #696969;}"
                                 % (self.background_color,
                                    self.border_top_left_radius, self.border_top_right_radius,
                                    self.border_bottom_left_radius, self.border_bottom_right_radius,
                                    )
                                 )

#一般多行文本输入框的样式
class Normal_QTextEdit_Style(QTextEdit):
    def __init__(self, parent=None, **kwargs):  # 需要传入背景颜色、圆角、边粗细、边颜色、点击变色
        super(Normal_QTextEdit_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.background_color = kwargs['QTextEdit']['background-color']
        self.border_top_left_radius = kwargs['QTextEdit']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QTextEdit']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QTextEdit']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QTextEdit']['border-bottom-right-radius']
        self.content_format = kwargs['content_format']
        self.content_size = kwargs['content_size']
        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setFixedWidth(int(self.w))
        self.setFixedHeight(int(self.h))
        self.setFont(QFont(self.content_format, int(self.content_size)))
        self.setStyleSheet("QTextEdit{background-color:\"%s\";"
                               "border-top-left-radius: \"%s\";"
                               "border-top-right-radius:\"%s\";"
                               "border-bottom-left-radius:\"%s\";"
                               "border-bottom-right-radius:\"%s\";"
                               "border: 1px solid #696969;}"
                                 % (self.background_color,
                                    self.border_top_left_radius, self.border_top_right_radius,
                                    self.border_bottom_left_radius, self.border_bottom_right_radius,
                                    )
                                 )

#log输出框的样式
class Run_Log_Style(QTextBrowser):
    def __init__(self, parent=None, **kwargs):
        super(Run_Log_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.background_color = kwargs['QTextBrowser']['background-color']
        self.border_top_left_radius = kwargs['QTextBrowser']['border-top-left-radius']
        self.border_top_right_radius = kwargs['QTextBrowser']['border-top-right-radius']
        self.border_bottom_left_radius = kwargs['QTextBrowser']['border-bottom-left-radius']
        self.border_bottom_right_radius = kwargs['QTextBrowser']['border-bottom-right-radius']
        self.content_format = kwargs['content_format']
        self.content_size = kwargs['content_size']
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(int(self.x), int(self.y), int(self.w), int(self.h))
        self.setFont(QFont(self.content_format, int(self.content_size)))
        self.setStyleSheet("QTextBrowser{"
                           "border-top-left-radius: \"%s\";"
                           "border-top-right-radius:\"%s\";"
                           "border-bottom-left-radius:\"%s\";"
                           "border-bottom-right-radius:\"%s\";"
                           "border: 1px solid #FFFFFF; background-color:\"%s\";}"
                           % (self.border_top_left_radius, self.border_top_right_radius,
                              self.border_bottom_left_radius, self.border_bottom_right_radius,
                              self.background_color
                              )
            )
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

#下拉菜单栏的输出样式
class QCombobox_Style(QComboBox):
    def __init__(self, parent=None, **kwargs):  # 需要传入背景颜色、圆角、边粗细、边颜色、点击变色
        super(QCombobox_Style, self).__init__(parent=parent)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.content_format = kwargs['content_format']
        self.content_size = kwargs['content_size']
        self.Items = kwargs['Items']
        self.setup_ui()

    def setup_ui(self):
        self.move(int(self.x), int(self.y))
        self.setFixedWidth(int(self.w))
        self.setFixedHeight(int(self.h))
        self.setFont(QFont(self.content_format, int(self.content_size)))

        x = self.Items.strip().split(";")
        items = [item for item in x]
        self.addItems(items)