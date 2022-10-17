# -*- coding: utf-8 -*-
import json
import sys

from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from QT_tools_code.A_Shaitu.Shaitu_tools import Cut_Image

from QT_style.style import Normal_Widget_Style, Normal_Qlabel_Style, Normal_QLineEdit_Style
from QT_style.style import Normal_Button_Style, Run_Log_Style, QCombobox_Style
file_path = r'QT_style/A_Shaitu/cut_image_QT.json'
style_dict = json.load(open(file_path, 'r', encoding='utf-8'))


class Cut_image_QT_Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Cut_image_QT_Demo, self).__init__()
        self.worker = Cut_Image()
        self.setup_ui()

    def log_info(self,info):
        self.log.append(info)
        QApplication.processEvents()  # 刷新界面

    def setup_ui(self):
        self.setWindowOpacity(0.96)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.resize(930, 768)

        self.worker._signal.connect(self.log_info)

        self.base_widget = Normal_Widget_Style(self, **style_dict['Base_Normal_Widget_Style'])
        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        self.title_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Title_label_Style'])

        self.input_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Input_label_Style'])

        self.input_dir = Normal_Button_Style(self, **style_dict['Input_dir_Button_Style'])
        self.input_dir.clicked.connect(self.input_handleButton)
        # self.path_to_images_dir = None

        self.output_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Output_label_Style'])

        self.output_dir = Normal_Button_Style(self, **style_dict['Output_dir_Button_Style'])
        self.output_dir.clicked.connect(self.output_handleButton)
        # self.path_to_images_dir = None

        self.input_path = Normal_QLineEdit_Style(self, **style_dict['Input_path_LineEdit_Style'])
        self.input_path.setPlaceholderText(("请选择待切分的文件目录"))
        self.input_path.textChanged.connect(self.set_input_path)
        self.path = None
        self.input_path.setObjectName("input_path")

        self.output_path = Normal_QLineEdit_Style(self, **style_dict['Output_path_LineEdit_Style'])
        self.output_path.setPlaceholderText(("请选择想保存的文件目录"))
        self.output_path.textChanged.connect(self.set_output_path)
        self.path1 = None
        self.output_path.setObjectName("output_path")

        # 选择切分模式
        self.mode = QCombobox_Style(self, **style_dict['Mode_QCombobox_Style'])
        self.mode.currentIndexChanged[str].connect(self.set_mode_value)
        self.mode_value = None
        self.mode.setObjectName("mode")

        # 输入切分范围
        self.input_label = Normal_Qlabel_Style(self.base_widget, **style_dict['OptionMode_label_Style'])
        self.h_range_label = Normal_Qlabel_Style(self.base_widget, **style_dict['OptionHRange_label_Style'])
        self.w_range_label = Normal_Qlabel_Style(self.base_widget, **style_dict['OptionWRange_label_Style'])

        self.h_range = Normal_QLineEdit_Style(self, **style_dict['HRange_LineEdit_Style'])
        self.h_range.setPlaceholderText(("例：0, 100, 200, ...."))
        self.h_range.textChanged.connect(self.set_h_range)
        self.h_range1 = None
        self.h_range.setObjectName("h_range")
        self.w_range = Normal_QLineEdit_Style(self, **style_dict['WRange_LineEdit_Style'])
        self.w_range.setPlaceholderText(("例：0, 100, 200, ...."))
        self.w_range.textChanged.connect(self.set_w_range)
        self.w_range1 = None
        self.w_range.setObjectName("w_range")

        # 开始转换
        self.start = Normal_Button_Style(self, **style_dict['Start_Button_Style'])
        self.start.clicked.connect(self.click_handler)

        # 制定log输出框
        self.log = Run_Log_Style(self, **style_dict['Run_Log_Style'])
        self.tips = Normal_Qlabel_Style(self.base_widget, **style_dict['Tips_label_Style'])

    def set_input_path(self):
        self.path = self.input_path.text()  # str

    def set_output_path(self):
        self.path1 = self.output_path.text()  # str

    def set_mode_value(self):
        self.mode_value = self.mode.currentText()

    def set_h_range(self):
        self.h_range1 = self.h_range.text()  # str

    def set_w_range(self):
        self.w_range1 = self.w_range.text()  # str

    def click_handler(self):

        from utils.format_check import Dir_Check
        Dir_Check = Dir_Check()
        format_right = Dir_Check.inputdir_outputdir_DIF_check(path=self.path, path1=self.path1)

        if format_right:
            QMessageBox.information(self, '提示', '提交成功')
            QApplication.processEvents()
            self.log.setText(str(">>开始分图>>"))
            self.log.append("————————————————")
            self.log.append(str(">>分图中，请稍等...>>"))
            self.log.append("————————————————")
            QApplication.processEvents()  # 刷新界面
            self.worker.input_dir = str(self.path)
            self.worker.output_dir = str(self.path1)
            self.worker.mode = str(self.mode_value)
            self.worker.h_range1 = str(self.h_range1)
            self.worker.w_range1 = str(self.w_range1)
            self.worker.start()


    def input_handleButton(self):
        fileDlg = QFileDialog()
        # fileDlg.setFileMode(QFileDialog.AnyFile)
        fileDlg.setFileMode(QFileDialog.DirectoryOnly)
        # fileDlg.setOption(QFileDialog.DontUseNativeDialog, True)
        fileDlg.setDirectory("c:/")
        listView = fileDlg.findChild(QListView, "listView")
        if listView:
            listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeView = fileDlg.findChild(QTreeView, "treeView")
        if treeView:
            treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if fileDlg.exec_():
            folders = fileDlg.selectedFiles()
            self.input_dir = folders[0]
            self.input_path.setText(str(self.input_dir))

    def output_handleButton(self):
        fileDlg = QFileDialog()
        fileDlg.setFileMode(QFileDialog.DirectoryOnly)
        # fileDlg.setOption(QFileDialog.DontUseNativeDialog, True)
        fileDlg.setDirectory("c:/")
        listView = fileDlg.findChild(QListView, "listView")
        if listView:
            listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeView = fileDlg.findChild(QTreeView, "treeView")
        if treeView:
            treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if fileDlg.exec_():
            folders = fileDlg.selectedFiles()
            self.output_dir = folders[0]
            self.output_path.setText(str(self.output_dir))

