import os
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView, QMainWindow
from PyQt5.QtWidgets import QRadioButton, QMessageBox, QButtonGroup, QTextBrowser
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QPushButton, QLineEdit

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor, QCursor
from PyQt5.QtCore import Qt
# from PyQt5.QtCore.Qt import AA_EnableHighDpiScaling

class Foarmat_Check():

    def __init__(self):
        pass

    def check_path_exists(self, path = None):
        return(os.path.exists(path))

    def check_path_isabs(self, path = None):
        return(os.path.isabs(path))

    def check_path_isempty(self, path = None):
        return(path == None or path == '')

    def check_path_isdif(self, path1 = None, path2 = None):
        path1_z = str(path1).replace("\\", "/").strip().split('/')
        path2_z = str(path2).replace("\\", "/").strip().split('/')
        if os.path.isdir(path1):
            a = [True for i, j in zip(path1_z, path2_z) if i == j]
            if len(a) == len(path1_z):
                isdif = False
            else:
                isdif = True
        if os.path.isfile(path1):
            real_input_path = os.path.dirname(path1).replace("\\", "/").strip().split('/')
            b = [True for i, j in zip(path1_z, path2_z) if i == j]
            if len(b) == len(real_input_path):
                isdif = False
            else:
                isdif = True
        return isdif

    def check_path_format(self, path = None):
        return (os.path.isabs(path) and os.path.exists(path))

    def check_file_num(self, path = None):
        num_file = [len(dir) + len(files) for root, dir, files in os.walk(path)]
        return num_file[0]



class Dir_Check(QtWidgets.QMainWindow):

    Foarmat_Check = Foarmat_Check()
    def __init__(self):
        super(Dir_Check, self).__init__()
        self.setWindowIcon(QIcon('./images/shuguang.png'))

    def inputdir_outputdir_DIF_check(self, path = None, path1 = None):

        if Foarmat_Check.check_path_isempty(self = self, path = path) or Foarmat_Check.check_path_isempty(self = self, path = path1):
            if Foarmat_Check.check_path_isempty(self = self, path = path):
                QMessageBox.information(self, '??????', '?????????????????????')
            if Foarmat_Check.check_path_isempty(self = self, path = path1):
                QMessageBox.information(self, '??????', '?????????????????????\n??????????????????????????????????????????????????????')
        else:
            if (not Foarmat_Check.check_path_format(self = self, path = path)) or (not Foarmat_Check.check_path_isdif(self = self, path1 = path, path2 = path1)) \
                    or (not Foarmat_Check.check_path_isabs(self = self, path = path1)):
                if not Foarmat_Check.check_path_format(self = self, path = path):
                    QMessageBox.information(self, '??????', '???????????????????????????')
                if not Foarmat_Check.check_path_isabs(self = self, path = path1):
                    QMessageBox.information(self, '??????', '???????????????????????????')
                if not Foarmat_Check.check_path_isdif(self = self, path1 = path, path2 = path1):
                    QMessageBox.information(self, '??????', '?????????????????????????????????')
            else:
                if not Foarmat_Check.check_path_exists(self = self, path = path1):
                    os.makedirs(path1)
                    QMessageBox.information(self, '??????', '???????????????????????????')
                num = Foarmat_Check.check_file_num(self = self, path = path1)
                if num != 0:
                    QMessageBox.information(self, '??????', '???????????????????????????????????????')
                else:
                    return True

    def inputdir_outputdir_SAME_check(self, path = None, path1 = None):

        if Foarmat_Check.check_path_isempty(self = self, path = path) or Foarmat_Check.check_path_isempty(self = self, path = path1):
            if Foarmat_Check.check_path_isempty(self = self, path = path):
                QMessageBox.information(self, '??????', '?????????????????????')
            if Foarmat_Check.check_path_isempty(self = self, path = path1):
                QMessageBox.information(self, '??????', '?????????????????????')
        else:
            if (not Foarmat_Check.check_path_format(self = self, path = path)) or (not Foarmat_Check.check_path_isabs(self = self, path = path1)):
                if not Foarmat_Check.check_path_format(self = self, path = path):
                    QMessageBox.information(self, '??????', '???????????????????????????')
                if not Foarmat_Check.check_path_isabs(self = self, path = path1):
                    QMessageBox.information(self, '??????', '???????????????????????????')
            else:
                if not Foarmat_Check.check_path_exists(self = self, path = path1):
                    os.makedirs(path1)
                    QMessageBox.information(self, '??????', '???????????????????????????')
                return True

    def single_dir_check(self, path = None, path1 = None):

        if Foarmat_Check.check_path_isempty(self = self, path = path):
            if Foarmat_Check.check_path_isempty(self = self, path = path):
                QMessageBox.information(self, '??????', '?????????????????????')
        else:
            if (not Foarmat_Check.check_path_format(self = self, path = path)):
                if not Foarmat_Check.check_path_format(self = self, path = path):
                    QMessageBox.information(self, '??????', '???????????????????????????')
            else:
                return True



if __name__ == "__main__":
    path = r'E:\Desktop\123'
    worker = Foarmat_Check()
    bool = worker.check_path_isempty(path)
    print(bool)