# -*- coding: utf-8 -*-
import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView
from PyQt5.QtWidgets import QApplication, QMessageBox

from QT_tools_code.C_Biaozhutongji.Biaozhutongji_tools import Extract_assign_labelindex

from QT_style.style import Normal_Widget_Style, Normal_Qlabel_Style, Normal_QLineEdit_Style, Normal_Button_Style, Run_Log_Style
file_path = r'QT_style/C_Biaozhutongji/extract_assign_labelindex_data_QT.json'
style_dict = json.load(open(file_path, 'r', encoding='utf-8'))


class Extract_assign_labelindex_data_QT_Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Extract_assign_labelindex_data_QT_Demo, self).__init__()
        self.worker = Extract_assign_labelindex()
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

        self.output_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Output_label_Style'])

        self.output_dir = Normal_Button_Style(self, **style_dict['Output_dir_Button_Style'])
        self.output_dir.clicked.connect(self.output_handleButton)

        self.input_path = Normal_QLineEdit_Style(self, **style_dict['Input_path_LineEdit_Style'])
        self.input_path.setPlaceholderText(("确认txt与图片在同一目录下且名称相对应"))
        self.input_path.textChanged.connect(self.set_input_path)
        self.path = None
        self.input_path.setObjectName("input_path")

        self.output_path = Normal_QLineEdit_Style(self, **style_dict['Output_path_LineEdit_Style'])
        self.output_path.setPlaceholderText(("图片与txt将被一起复制"))
        self.output_path.textChanged.connect(self.set_output_path)
        self.path1 = None
        self.output_path.setObjectName("output_path")

        self.label_index_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Label_index_label_Style'])

        self.label_index = Normal_QLineEdit_Style(self, **style_dict['Label_index_LineEdit_Style'])
        self.label_index.textChanged.connect(self.set_label_index)
        self.label_index1 = None
        self.label_index.setObjectName("label_index")

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

    def set_label_index(self):
        self.label_index1 = self.label_index.text()  # str

    def click_handler(self):

        from utils.format_check import Dir_Check
        Dir_Check = Dir_Check()
        format_right = Dir_Check.inputdir_outputdir_DIF_check(path=self.path, path1=self.path1)

        if format_right:
            QMessageBox.information(self, '提示', '提交成功')
            QApplication.processEvents()
            self.log.setText(str(">>开始提取>>"))
            self.log.append("————————————————")
            self.log.append(str(">>提取中，请稍等...>>"))
            self.log.append("————————————————")
            QApplication.processEvents()  # 刷新界面
            self.worker.input_dir = str(self.path)
            self.worker.output_dir = str(self.path1)
            self.worker.label_index = str(self.label_index1)
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



