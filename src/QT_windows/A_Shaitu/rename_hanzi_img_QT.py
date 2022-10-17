# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView
from PyQt5.QtWidgets import QRadioButton, QMessageBox, QApplication, QDesktopWidget, QButtonGroup
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from QT_tools_code.A_Shaitu.Shaitu_tools import Rename_Hanzi_Image

from QT_style.style import Normal_Widget_Style, Normal_Qlabel_Style, Normal_QLineEdit_Style
from QT_style.style import Normal_Button_Style, Run_Log_Style
file_path = r'QT_style/A_Shaitu/rename_hanzi_img_QT0.json'
style_dict = json.load(open(file_path, 'r', encoding='utf-8'))


class Rename_hanzi_img_QT_Demo(QtWidgets.QMainWindow):

    def __init__(self):
        super(Rename_hanzi_img_QT_Demo, self).__init__()
        self.worker = Rename_Hanzi_Image()
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

        self.input_path = Normal_QLineEdit_Style(self, **style_dict['Input_path_LineEdit_Style'])
        self.input_path.setPlaceholderText(("请选择图片所在文件夹"))
        self.input_path.textChanged.connect(self.set_input_path)
        self.path = None
        self.input_path.setObjectName("input_path")

        # 是否前缀文件夹名
        self.input_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Option_label_Style'])

        self.rb11 = QRadioButton('是', self)
        self.rb11.move(70, 215)
        self.rb11.setFont(QFont("Microsoft YaHei", 10))
        self.rb12 = QRadioButton('否', self)
        self.rb12.move(120, 215)
        self.rb12.setFont(QFont("Microsoft YaHei", 10))

        # 是否更改project
        self.project_label = Normal_Qlabel_Style(self.base_widget, **style_dict['Option2_label_Style'])

        self.rb13 = QRadioButton('是', self)
        self.rb13.move(70, 275)
        self.rb13.setFont(QFont("Microsoft YaHei", 10))
        self.rb14 = QRadioButton('否', self)
        self.rb14.move(120, 275)
        self.rb14.setFont(QFont("Microsoft YaHei", 10))

        # 创建按键组
        QBG1 = QButtonGroup(self)
        QBG2 = QButtonGroup(self)
        # 给按键分组
        QBG1.addButton(self.rb11, 1)
        QBG1.addButton(self.rb12, 2)
        QBG2.addButton(self.rb13, 1)
        QBG2.addButton(self.rb14, 2)

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
        format_right = Dir_Check.single_dir_check(path = self.path)

        if format_right:
            QMessageBox.information(self, '提示', '提交成功')
            QApplication.processEvents()
            self.log.setText(str(">>开始转换>>"))
            self.log.append("————————————————")
            self.log.append(str(">>转换中，请稍等...>>"))
            self.log.append("————————————————")
            QApplication.processEvents()  # 刷新界面
            if self.rb11.isChecked() or self.rb12.isChecked():
                save_folder = self.rb11.isChecked()
            else:
                save_folder = False
            if self.rb13.isChecked() or self.rb14.isChecked():
                fix_project = self.rb13.isChecked()
            else:
                fix_project = False
            self.worker.file_path = str(self.path)
            self.worker.save_folder = save_folder
            self.worker.fix_project = fix_project
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


