import sys
import os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from database_moudle.datajson import static_data,get_static_data
from database_moudle.data_model import General_Table,DataBaseTool
import logging
import platform
import subprocess
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger.info("create tmp database：{}".format(tmp_database_name))
static_data = get_static_data(static_data)
worker = DataBaseTool()
# worker.insertmany(static_data)
# print(worker.get_total_count())
page_data = worker.paginate_search(current_page = 1 , per_page = 17)


class DataGrid(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('数据统计')
        self.setFixedSize(1600,780)

        self.setWindowIcon(QIcon('./images/shuguang.png'))


        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 17

        self.initUI()

        self.current_data = None
        self.search_mode = False
        self.search_commend = None
        self.search_page_count = None

    def initUI(self):
        # 创建窗口
        self.createWindow()
        # 设置表格
        self.setTableView()

        # 信号槽连接
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)
        self.refreshButton.clicked.connect(self.searchButtonclick)

    # 创建窗口
    def createWindow(self):

        # self.base_widget = QtWidgets.QWidget()  # 创建透明窗口
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        # 操作布局
        operatorLayout = QHBoxLayout()
        self.prevButton = QPushButton("前一页")
        self.nextButton = QPushButton("后一页")
        self.switchPageButton = QPushButton("GO")
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(40)
        self.refreshButton = QPushButton("刷新")

        switchPage = QLabel('转到第')
        page = QLabel('页')
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        operatorLayout.addWidget(switchPage)
        operatorLayout.addWidget(self.switchPageLineEdit)
        operatorLayout.addWidget(page)
        operatorLayout.addWidget(self.switchPageButton)
        operatorLayout.addWidget(self.refreshButton)
        operatorLayout.addWidget(QSplitter())

        # 状态布局
        statusLayout = QHBoxLayout()
        self.totalPageLabel = QLabel()
        self.totalPageLabel.setFixedWidth(70)
        self.currentPageLabel = QLabel()
        self.currentPageLabel.setFixedWidth(70)
        self.info_label = QLabel()
        self.info_label.setFixedWidth(500)

        self.totalRecordLabel = QLabel()
        self.totalRecordLabel.setFixedWidth(70)

        statusLayout.addWidget(self.totalPageLabel)
        statusLayout.addWidget(self.currentPageLabel)
        statusLayout.addWidget(self.info_label)
        statusLayout.addWidget(QSplitter())
        statusLayout.addWidget(self.totalRecordLabel)

        # 状态布局
        # loginfoLayout = QHBoxLayout()
        # self.loginfo = QTextBrowser()
        # self.loginfo.move(50,50)
        # # self.loginfo.setGeometry(50,600,200,200)
        # self.loginfo.setFixedWidth(400)
        # self.loginfo.setFixedHeight(200)
        #
        # loginfoLayout.addWidget(self.loginfo)

        # 设置表格属性
        self.tableView = QTableView()
        # 表格宽度的自适应调整
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) #自适应列宽
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.clicked.connect(self.show_info)
        self.tableView.doubleClicked.connect(self.open_dir)


        #创建左侧界面
        LeftLayout = QVBoxLayout()
        LeftLayout.addLayout(operatorLayout)
        LeftLayout.addWidget(self.tableView)
        # LeftLayout.addLayout(loginfoLayout)
        LeftLayout.addLayout(statusLayout)


        # # 右侧搜索布局
        searchLayout = QVBoxLayout()
        title = QLabel('按条件操作')
        self.log_LineEdit = QLineEdit()
        self.log_LineEdit.setPlaceholderText("序号")
        self.project_number_LineEdit = QLineEdit()
        self.project_number_LineEdit.setPlaceholderText("项目号")
        self.project_name_LineEdit = QLineEdit()
        self.project_name_LineEdit.setPlaceholderText("项目名称")
        self.manager_LineEdit = QLineEdit()
        self.manager_LineEdit.setPlaceholderText(("项目负责人"))
        # self.manager_LineEdit = QComboBox()
        # self.manager_LineEdit.addItem("晏文仲")
        # self.manager_LineEdit.addItem("黄金")
        self.label_manager_LineEdit = QLineEdit()
        self.label_manager_LineEdit.setPlaceholderText("标注负责人")
        self.state_LineEdit = QLineEdit()
        self.state_LineEdit.setPlaceholderText("数据状态 (未标注、已标注、待修改等)")
        self.station_LineEdit = QLineEdit()
        self.station_LineEdit.setPlaceholderText("工位")
        self.Ai_model_LineEdit = QLineEdit()
        self.Ai_model_LineEdit.setPlaceholderText("模型")
        self.camera_LineEdit = QLineEdit()
        self.camera_LineEdit.setPlaceholderText("相机")
        self.data_path_LineEdit = QLineEdit()
        self.data_path_LineEdit.setPlaceholderText("数据路径")
        self.tip_LineEdit = QLineEdit()
        self.tip_LineEdit.setPlaceholderText("备注")
        self.searchButton = QPushButton("查询数据")
        self.searchButton.clicked.connect(self.searchButtonclick)
        self.insertButton = QPushButton("添加数据")
        self.insertButton.clicked.connect(self.insertButtonclick)
        self.changeButton = QPushButton("修改数据")
        self.changeButton.clicked.connect(self.changeButtonclick)
        self.changeButton.setEnabled(False)
        self.delButton = QPushButton("删除数据")
        self.delButton.clicked.connect(self.delButtonclick)
        self.delButton.setEnabled(False)

        searchLayout.addWidget(title)
        searchLayout.addWidget(self.log_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.project_number_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.project_name_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.manager_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.label_manager_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.state_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.station_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.Ai_model_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.camera_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.data_path_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.tip_LineEdit,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.searchButton,Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.insertButton, Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.changeButton, Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(self.delButton, Qt.AlignLeft | Qt.AlignTop)
        searchLayout.addWidget(QSplitter(),Qt.AlignLeft | Qt.AlignTop)


        #总体布局
        # mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(LeftLayout)
        self.mainLayout.addLayout(searchLayout)
        self.mainLayout.setStretchFactor(LeftLayout , 5)
        self.mainLayout.setStretchFactor(searchLayout, 1)


        # self.setLayout(mainLayout)

    # 设置表格
    def setTableView(self):

        columnname = ['项目序号', '项目号', '项目名称', '项目负责人', '标注负责人', '数据状态', '工位', '模型', '相机', '数据路径 (双击单元格可打开路径)', '备注']

        self.model = QStandardItemModel(self.PageRecordCount, len(columnname), self)
        self.model.setHorizontalHeaderItem(0, QStandardItem(columnname[0]))
        self.model.setHorizontalHeaderItem(1, QStandardItem(columnname[1]))
        self.model.setHorizontalHeaderItem(2, QStandardItem(columnname[2]))
        self.model.setHorizontalHeaderItem(3, QStandardItem(columnname[3]))
        self.model.setHorizontalHeaderItem(4, QStandardItem(columnname[4]))
        self.model.setHorizontalHeaderItem(5, QStandardItem(columnname[5]))
        self.model.setHorizontalHeaderItem(6, QStandardItem(columnname[6]))
        self.model.setHorizontalHeaderItem(7, QStandardItem(columnname[7]))
        self.model.setHorizontalHeaderItem(8, QStandardItem(columnname[8]))
        self.model.setHorizontalHeaderItem(9, QStandardItem(columnname[9]))
        self.model.setHorizontalHeaderItem(10, QStandardItem(columnname[10]))

        for row in range(len(page_data)):     # 2
            for column in range(len(columnname)):
                if page_data[row][column]:
                    item = QStandardItem(page_data[row][column])
                    self.model.setItem(row, column, item)
                else:
                    continue

        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 设置总记录数
        self.setTotalRecordLabel()

        # 设置模型
        self.tableView.setModel(self.model)
        # self.tableView.setModel(self.queryModel)

    # 得到记录数
    def getTotalRecordCount(self):
        # self.queryModel.setQuery("select * from student")
        # rowCount = self.queryModel.rowCount()
        rowCount = worker.get_total_count()
        #print('rowCount=' + str(rowCount))
        return rowCount

    # 得到页数
    def getPageCount(self):
        if self.totalRecrodCount % self.PageRecordCount == 0:
            return (self.totalRecrodCount / self.PageRecordCount)
        else:
            return (self.totalRecrodCount // self.PageRecordCount + 1)

    # 记录查询
    def recordQuery(self, kwargs=None , current_page = None , per_page = None):
        if not self.search_mode:
            new_page_data = worker.paginate_search(current_page = current_page , per_page = per_page)
            # logger.info("ADVANCE_SEARCH：{}".format(new_page_data))
            for row in range(self.PageRecordCount):   # 2
                for column in range(11):
                    if row  < len(new_page_data):
                        item = QStandardItem(new_page_data[row][column])
                        self.model.setItem(row, column, item)

                        # self.model.setData(self.model.index(row, column), item)
                    else:
                        self.model.setItem(row, column, QStandardItem(" "))
            # self.tableView.setModel(self.model)
        else:
            new_page_data = worker.paginate_search(kwargs = kwargs, current_page=current_page, per_page=per_page)
            # logger.info("ADVANCE_SEARCH：{}".format(new_page_data))
            for row in range(self.PageRecordCount):  # 2
                for column in range(11):
                    if row < len(new_page_data):
                        item = QStandardItem(new_page_data[row][column])
                        self.model.setItem(row, column, item)

                        # self.model.setData(self.model.index(row, column), item)
                    else:
                        self.model.setItem(row, column, QStandardItem(" "))
            # self.tableView.setModel(self.model)


    # 刷新状态
    def updateStatus(self):
        szCurrentText = ('当前第 %d 页' % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)

        # 设置按钮是否可用
        if self.currentPage <= 1:
            self.prevButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)

        if self.currentPage > self.totalPage - 1:
            self.nextButton.setEnabled(False)

        else:
            self.nextButton.setEnabled(True)

    # 设置总页数文本
    def setTotalPageLabel(self):
        szPageCountText = ('总共 %d 页' % self.totalPage)
        self.totalPageLabel.setText(szPageCountText)

    # 设置总记录数
    def setTotalRecordLabel(self):
        szTotalRecordText = ('共 %d 条' % self.totalRecrodCount)
        logger.info("*** setTotalRecordLabel szTotalRecordText=：{}".format(szTotalRecordText))
        self.totalRecordLabel.setText(szTotalRecordText)

    # 前一页被按下
    def onPrevButtonClick(self):
        logger.info("onPrevButtonClick")
        limitIndex = self.currentPage -1
        self.recordQuery(self.search_commend , current_page= limitIndex , per_page= self.PageRecordCount)
        self.currentPage -= 1
        self.updateStatus()

    # 后一页被按下
    def onNextButtonClick(self):
        logger.info("onNextButtonClick")
        limitIndex = self.currentPage + 1
        self.recordQuery(self.search_commend , current_page= limitIndex , per_page= self.PageRecordCount)
        self.currentPage += 1
        self.updateStatus()

    # 转到页按钮被按下
    def onSwitchPageButtonClick(self):
        # 得到输入的字符串
        szText = self.switchPageLineEdit.text()

        # 得到页数
        pageIndex = int(szText)
        # 判断是否有指定页
        if pageIndex > self.totalPage or pageIndex < 1:
            QMessageBox.information(self, '提示', "没有指定的页面,重新输入")
            return

        # 得到查询起始行号
        limitIndex = pageIndex

        # 记录查询
        self.recordQuery(self.search_commend, current_page= limitIndex , per_page= self.PageRecordCount)
        # 设置当前页
        self.currentPage = pageIndex
        # 刷新状态
        self.updateStatus()

    #查询数据回调
    def searchButtonclick(self):
        self.search_mode = True
        self.search_dict = {}
        if self.log_LineEdit.text():
            self.search_dict["log"] =  self.log_LineEdit.text()
        if self.project_number_LineEdit.text():
            self.search_dict["project_number"] = self.project_number_LineEdit.text()
        if self.project_name_LineEdit.text():
            self.search_dict["project_name"] = self.project_name_LineEdit.text()
        if self.manager_LineEdit.text():
            self.search_dict["manager"] = self.manager_LineEdit.text()
        if self.label_manager_LineEdit.text():
            self.search_dict["label_manager"] = self.label_manager_LineEdit.text()
        if self.state_LineEdit.text():
            self.search_dict["state"] = self.state_LineEdit.text()
        if self.station_LineEdit.text():
            self.search_dict["station"] = self.station_LineEdit.text()
        if self.Ai_model_LineEdit.text():
            self.search_dict["Ai_model"] = self.Ai_model_LineEdit.text()
        if self.camera_LineEdit.text():
            self.search_dict["camera"] = self.camera_LineEdit.text()
        if self.data_path_LineEdit.text():
            self.search_dict["data_path"] = self.data_path_LineEdit.text()
        if self.tip_LineEdit.text():
            self.search_dict["tip"] = self.tip_LineEdit.text()
        # print(self.search_dict)
        self.search_commend = self.search_dict
        if self.search_commend:
            search_page_data = worker.paginate_search(self.search_commend,current_page = 1 , per_page = self.PageRecordCount)
            self.search_page_count = worker.advance_search_count(self.search_commend)
        else:
            search_page_data = worker.paginate_search(current_page = 1 , per_page = self.PageRecordCount)
            self.search_page_count = worker.get_total_count()
        for row in range(self.PageRecordCount):  # 2
            for column in range(11):
                if row < len(search_page_data):
                    item = QStandardItem(search_page_data[row][column])
                    self.model.setItem(row, column, item)

                    # self.model.setData(self.model.index(row, column), item)
                else:
                    self.model.setItem(row, column, QStandardItem(" "))

        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.totalRecrodCount = self.search_page_count
        # 得到总页数
        if self.totalRecrodCount % self.PageRecordCount == 0:
            self.totalPage = (self.totalRecrodCount / self.PageRecordCount)
        else:
            self.totalPage = (self.totalRecrodCount // self.PageRecordCount + 1)
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 设置总记录数
        self.setTotalRecordLabel()

    #插入数据回调
    def insertButtonclick(self):
        self.insert_dict = {}
        if self.log_LineEdit.text():
            self.insert_dict["log"] =  self.log_LineEdit.text()
        if self.project_number_LineEdit.text():
            self.insert_dict["project_number"] = self.project_number_LineEdit.text()
        if self.project_name_LineEdit.text():
            self.insert_dict["project_name"] = self.project_name_LineEdit.text()
        if self.manager_LineEdit.text():
            self.insert_dict["manager"] = self.manager_LineEdit.text()
        if self.label_manager_LineEdit.text():
            self.insert_dict["label_manager"] = self.label_manager_LineEdit.text()
        if self.state_LineEdit.text():
            self.insert_dict["state"] = self.state_LineEdit.text()
        if self.station_LineEdit.text():
            self.insert_dict["station"] = self.station_LineEdit.text()
        if self.Ai_model_LineEdit.text():
            self.insert_dict["Ai_model"] = self.Ai_model_LineEdit.text()
        if self.camera_LineEdit.text():
            self.insert_dict["camera"] = self.camera_LineEdit.text()
        if self.data_path_LineEdit.text():
            self.insert_dict["data_path"] = self.data_path_LineEdit.text()
        if self.tip_LineEdit.text():
            self.insert_dict["tip"] = self.tip_LineEdit.text()
        if self.insert_dict :
            QMessageBox.information(self, '提示', '注册成功')
            worker.insertmany([self.insert_dict])
            self.search_commend = self.insert_dict
            if self.search_commend:
                search_page_data = worker.paginate_search(self.search_commend,current_page = 1 , per_page = self.PageRecordCount)
                self.search_page_count = worker.advance_search_count(self.search_commend)
            else:
                search_page_data = worker.paginate_search(current_page = 1 , per_page = self.PageRecordCount)
                self.search_page_count = worker.get_total_count()
            for row in range(self.PageRecordCount):  # 2
                for column in range(11):
                    if row < len(search_page_data):
                        item = QStandardItem(search_page_data[row][column])
                        self.model.setItem(row, column, item)

                        # self.model.setData(self.model.index(row, column), item)
                    else:
                        self.model.setItem(row, column, QStandardItem(" "))

            # 设置当前页
            self.currentPage = 1
            # 得到总记录数
            self.totalRecrodCount = self.search_page_count
            # 得到总页数
            if self.totalRecrodCount % self.PageRecordCount == 0:
                self.totalPage = (self.totalRecrodCount / self.PageRecordCount)
            else:
                self.totalPage = (self.totalRecrodCount // self.PageRecordCount + 1)
            # 刷新状态
            self.updateStatus()
            # 设置总页数文本
            self.setTotalPageLabel()
            # 设置总记录数
            self.setTotalRecordLabel()
        else:
            QMessageBox.information(self, '提示', '注册信息不能为空')

    def setbuttion(self):
        self.delButton.setEnabled(False)

    #修改数据回调
    def changeButtonclick(self):
        columnname = ['id', 'project_number', 'project_name', 'manager', 'label_manager', 'state', 'station', 'Ai_model', 'camera', 'data_path', 'tip']
        row = self.tableView.currentIndex().row()
        column = columnname[self.tableView.currentIndex().column()]
        current_data = self.tableView.currentIndex().data()
        point_data = self.tableView.model().index(row,0).data()
        # print(point_data)
        dlg = Change_Data(point_data , current_data, column)
        dlg.exec_()


    #删除数据回调
    def delButtonclick(self):
        columnname = ['id', 'project_number', 'project_name', 'manager', 'label_manager', 'state', 'station',
                      'Ai_model', 'camera', 'data_path', 'tip']
        row = self.tableView.currentIndex().row()
        column = columnname[self.tableView.currentIndex().column()]
        current_data = self.tableView.currentIndex().data()
        point_data = self.tableView.model().index(row, 0).data()
        # print(point_data)
        worker.delte(point_data)
        QtWidgets.QMessageBox.warning(self, '提示', "删除成功")

    #获取单元格内容并显示
    def show_info(self):
        self.changeButton.setEnabled(True)
        self.delButton.setEnabled(True)
        row = self.tableView.currentIndex().row()
        column = self.tableView.currentIndex().column()
        self.current_data = self.tableView.currentIndex().data()
        self.info_label.setText(self.current_data)

    #获取单元格内容并打开文件夹
    def open_dir(self):
        self.current_data = self.tableView.currentIndex().data()
        row = self.tableView.currentIndex().row()
        column = self.tableView.currentIndex().column()
        try:
            if column == 9:
                self.open_fp(self.current_data)
        except:
            QtWidgets.QMessageBox.warning(self, '提示', "打开文件夹失败，路径有误或文件夹不存在")

    #打开文件夹
    def open_fp(self , fp: str):
        """
        打开文件或文件夹
        优点: 代码输入参数少, 复制粘贴即可使用, 支持在mac和win上使用, 打开速度快稳定;
        :param fp: 需要打开的文件或文件夹路径
        """
        systemType: str = platform.platform()  # 获取系统类型
        if 'mac' in systemType:  # 判断以下当前系统类型
            fp: str = fp.replace("\\", "/")  # mac系统下,遇到`\\`让路径打不开,不清楚为什么哈,觉得没必要的话自己可以删掉啦,18行那条也是
            subprocess.call(["open", fp])
        else:
            fp: str = fp.replace("/", "\\")  # win系统下,有时`/`让路径打不开
            os.startfile(fp)

#修改数据类
class Change_Data(QDialog):
    def __init__(self, id, data,commend):
        super(Change_Data, self).__init__()


        self.id = id
        self.data = data
        self.commend = commend
        self.QBtn = QPushButton()
        self.QBtn.setText("修改")

        self.setWindowTitle("数据修改")
        self.setFixedWidth(400)
        self.setFixedHeight(150)
        self.QBtn.clicked.connect(self.change)
        layout = QVBoxLayout()

        self.searchinfo = QLabel("数据id:{} 单元格:{}".format(id,data))
        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("输入修改数据")
        layout.addWidget(self.searchinfo)
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def change(self):
        change_data = self.searchinput.text()
        commend = {}
        commend[self.commend] = change_data
        worker.update(self.id , commend)
        QtWidgets.QMessageBox.warning(self, '提示', "修改成功")
        self.close()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = DataGrid()
    w.show()
    sys.exit(app.exec_())

