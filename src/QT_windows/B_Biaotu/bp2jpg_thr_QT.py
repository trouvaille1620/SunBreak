# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView
from PyQt5.QtWidgets import QRadioButton, QMessageBox, QApplication, QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from QT_tools_code.B_Biaotu.Biaotu_tools import Bp2jpg_thr

from QT_style.style import Normal_Widget_Style, Normal_Qlabel_Style, Normal_QLineEdit_Style
from QT_style.style import Normal_Button_Style, Run_Log_Style
file_path = r'QT_style/B_Biaotu/bp2jpg_thr_QT0.json'
style_dict = json.load(open(file_path, 'r', encoding='utf-8'))


class Bp2jpg_thr_QT_Demo(QtWidgets.QMainWindow):

    def __init__(self):
        super(Bp2jpg_thr_QT_Demo, self).__init__()
        self.worker = Bp2jpg_thr()
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
        self.path_to_images_dir = None

        self.output_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Output_label_Style'])

        self.output_dir = Normal_Button_Style(self, **style_dict['Output_dir_Button_Style'])
        self.output_dir.clicked.connect(self.output_handleButton)
        self.path_to_images_dir = None

        self.input_path = Normal_QLineEdit_Style(self, **style_dict['Input_path_LineEdit_Style'])
        self.input_path.setPlaceholderText(("请选择图片所在文件目录"))
        self.input_path.textChanged.connect(self.set_input_path)
        self.path = None
        self.input_path.setObjectName("input_path")

        self.output_path = Normal_QLineEdit_Style(self, **style_dict['Output_path_LineEdit_Style'])
        self.output_path.setPlaceholderText(("请选择想保存的文件目录"))
        self.output_path.textChanged.connect(self.set_output_path)
        self.path1 = None
        self.output_path.setObjectName("output_path")

        # 是否保存原图像
        self.input_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Option_label_Style'])

        self.rb11 = QRadioButton('是', self)
        self.rb11.move(70, 300)
        self.rb11.setFont(QFont("Microsoft YaHei", 10))
        self.rb12 = QRadioButton('否', self)
        self.rb12.move(120, 300)
        self.rb12.setFont(QFont("Microsoft YaHei", 10))

        # 开始转换
        self.start = Normal_Button_Style(self, **style_dict['Start_Button_Style'])
        self.start.clicked.connect(self.click_handler)

        # 制定log输出框
        self.log = Run_Log_Style(self, **style_dict['Run_Log_Style'])
        self.tips = Normal_Qlabel_Style(self.base_widget, **style_dict['Tips_label_Style'])
        # self.center()

    def set_input_path(self):
        self.path = self.input_path.text()  # str

    def set_output_path(self):
        self.path1 = self.output_path.text()  # str

    def click_handler(self):

        from utils.format_check import Dir_Check
        Dir_Check = Dir_Check()
        format_right = Dir_Check.inputdir_outputdir_DIF_check(path = self.path, path1 = self.path1)

        if format_right:
            QMessageBox.information(self, '提示', '提交成功')
            QApplication.processEvents()
            self.log.setText(str(">>开始转换>>"))
            self.log.append("————————————————")
            self.log.append(str(">>转换中，请稍等...>>"))
            self.log.append("————————————————")
            QApplication.processEvents()  # 刷新界面
            if self.rb11.isChecked() or self.rb12.isChecked():
                KEEP_ORIGIN = self.rb11.isChecked()
            else:
                KEEP_ORIGIN = True
            if os.path.isfile(self.path):
                self.worker.bp2jpg_single(str(self.path), str(self.path1), KEEP_ORIGIN)
            if os.path.isdir(self.path):
                self.worker.file_path = str(self.path)
                self.worker.output_file_path = str(self.path1)
                self.worker.KEEP_ORIGIN = KEEP_ORIGIN
                self.worker.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
            # self.output_fileT.setText(str(self.output_dir))

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

    def onClick_Button(self):
        app = QApplication.instance()  # 退出应用程序
        app.quit()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Bp2jpg_thr_QT_Demo()
    MainWindow.show()
    sys.exit(app.exec_())


