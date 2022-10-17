# -*-coding:utf-8-*-
from database_moudle.datajson import static_data
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from database_moudle.data_model import General_Table,DataBaseTool

worker = DataBaseTool()
worker.insertmany(static_data)
print(worker.get_total_count())
page_data = worker.paginate_search(current_page = 1 , per_page = 10)

# 基于Table Widget控件的表格
class MyTable(QTableWidget):
    def __init__(self, parent=None):
        super(MyTable, self).__init__(parent)

        self.setWindowTitle("数据统计")
        self.setWindowIcon(QIcon("a1.png"))
        self.resize(800, 500)  # 设置表格尺寸

        # ===1:创建初始表格
        self.setColumnCount(11)
        self.setRowCount(10)
        # self.setShowGrid(False) #是否需要显示网格

        self.settableHeader()
        # self.inputcelldata()
        self.settableInitData()
        self.settableSelectMode()
        # self.settableHeaderFontColor()
        # self.setCellFontColor()
        # self.setCellAlign()
        # self.setCellFontSize()
        # self.setCellFontColor()
        # self.setCellSpan()
        # self.addRowColumn()
        self.settableEditTrigger()

        # layout = QHBoxLayout()
        # layout.addWidget(MyTable)
        # self.setLayout(layout)

    # ===1:设置表格单元格尺寸
    def settableSize(self):
        """
        首先，可以指定某个行或者列的大小
        self.MyTable.setColumnWidth(2,50)  #将第2列的单元格，设置成50宽度
        self.MyTable.setRowHeight(2,60)      #将第2行的单元格，设置成60的高度
        还可以将行和列的大小设为与内容相匹配
        self.MyTable.resizeColumnsToContents()   #将列调整到跟内容大小相匹配
        self.MyTable.resizeRowsToContents()      #将行大小调整到跟内容的大学相匹配
        :return:
        """
        self.setColumnWidth(0, 50)
        self.setColumnWidth(3, 50)
        # self.setRowHeight(0,500)
        # 1.2 设置表格的行和列的大小与输入内容相匹配
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


    # ===2：设置表格的表头名称
    def settableHeader(self):

        columnname = ['创建日期', '项目号', '项目名称', '项目负责人', '标注负责人','数据状态','工位','模型','相机','数据路径','备注']
        self.setHorizontalHeaderLabels(columnname)
        # self.setVerticalHeaderLabels(rowname)

    # ===3:给表格输入初始化数据
    def settableInitData(self):
        for i in range(10):
            for j in range(11):
                # 1)直接在表格中添加数据
                self.setItem(i, j, QTableWidgetItem( page_data[i][j] ))

    def inputcelldata(self):  # 输入数据
        self.setItem(0, 0, QTableWidgetItem("张三"))
        # self.setItem(0,1,"男")
        comBox = QComboBox()
        comBox.addItem("男")
        comBox.addItem("女")
        self.setCellWidget(0, 1, comBox)

        self.setItem(0, 2, QTableWidgetItem(str(25)))
        self.setItem(0, 3, QTableWidgetItem(str(160.85)))

    """在单元格里加入控件QComboBox"""

    def addwidgettocell(self):
        comBox = QComboBox()
        comBox.addItem("男")
        comBox.addItem("女")
        self.setCellWidget(0, 1, comBox)

    # ===4:表格的其他相关属性设置
    """设置表格是否可编辑"""

    def settableEditTrigger(self):
        """使用格式说明：
                在默认情况下，表格里的字符是可以更改的，
                比如双击一个单元格，就可以修改原来的内容，
                如果想禁止用户的这种操作，让这个表格对用户只读，可以这样：
           QAbstractItemView.NoEditTriggers和QAbstractItemView.EditTrigger枚举中的一个，
           都是触发修改单元格内容的条件：
            QAbstractItemView.NoEditTriggers    0   No editing possible. 不能对表格内容进行修改
            QAbstractItemView.CurrentChanged    1   Editing start whenever current item changes.任何时候都能对单元格修改
            QAbstractItemView.DoubleClicked     2   Editing starts when an item is double clicked.双击单元格
            QAbstractItemView.SelectedClicked   4   Editing starts when clicking on an already selected item.单击已选中的内容
            QAbstractItemView.EditKeyPressed    8   Editing starts when the platform edit key has been pressed over an item.
            QAbstractItemView.AnyKeyPressed     16  Editing starts when any key is pressed over an item.按下任意键就能修改
            QAbstractItemView.AllEditTriggers   31  Editing starts for all above actions.以上条件全包括
        """
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    """ 设置表格为整行选择 """

    def settableSelect(self):
        """
        QAbstractItemView.SelectionBehavior枚举还有如下类型
        Constant                      Value        Description
        QAbstractItemView.SelectItems   0   Selecting single items.选中单个单元格
        QAbstractItemView.SelectRows    1   Selecting only rows.选中一行
        QAbstractItemView.SelectColumns 2   Selecting only columns.选中一列
        """
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    """单个选中和多个选中的设置"""

    def settableSelectMode(self):
        """
        setSelectionMode(QAbstractItemView.ExtendedSelection)  #设置为可以选中多个目标
        该函数的参数还可以是：
        QAbstractItemView.NoSelection      不能选择
        QAbstractItemView.SingleSelection  选中单个目标
        QAbstractItemView.MultiSelection    选中多个目标
        QAbstractItemView.ExtendedSelection和ContiguousSelection
        的区别不明显，要功能是正常情况下是单选，但按下Ctrl或Shift键后，可以多选
        :return:
        """
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    """表头显示与隐藏"""

    def settableHeaderVisible(self):
        """对于水平或垂直方法的表头，可以用以下方式进行 隐藏/显示 的设置：
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.horizontalHeader().setVisible(False)
        """
        # 4.3 隐藏表头
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

    """对表头文字的字体、颜色进行设置"""

    def settableHeaderFontColor(self):
        """
        PyQt5中没有如下设置背景颜色和字体颜色函数
        headItem.setBackgroundColor(QColor(c))  # 设置单元格背景颜色
        headItem.setTextColor(QColor(200, 111, 30))  # 设置文字颜色
        :return:
        有（设置字体颜色）：
        headItem.setForeground(QBrush(Qt.red))
        headItem.setForeground(QBrush(QColor(128,255,0)))
        """
        f, ok = QFontDialog.getFont()

        for x in range(self.columnCount()):
            headItem = self.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
            # headItem.setFont(QFont("song",12,QFont.Bold))
            if ok:
                headItem.setFont(f)  # 设置字体
            # 设置表头字体颜色
            # headItem.setForeground(QBrush(Qt.red))
            headItem.setForeground(QBrush(QColor(128, 255, 0)))

            headItem.setTextAlignment(Qt.AlignLeft)

    def settableproperty(self):
        # 4.2 选中表格中的某一行
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    """动态插入行列 """

    def addRowColumn(self):
        """当初始的行数或者列数不能满足需要的时候，
        我们需要动态的调整表格的大小，如入动态的插入行：
        insertColumn()动态插入列。
        insertRow(int)、
        insertColumn(int)，指定位置插入行或者列
        """
        rowcount = self.rowCount()
        self.insertRow(rowcount)

    """动态移除行列 """

    def removeRowColumn(self):
        """
        removeColumn(int column) 移除column列及其内容。
        removeRow(int row)移除第row行及其内容。
        :return:
        """
        rowcount = self.rowCount()
        self.removeRow(rowcount - 1)

    # =========第2部分：对单元格的进行设置=============
    """1.单元格设置字体颜色和背景颜色"""
    """2.设置单元格中的字体和字符大小"""
    """3.设置单元格内文字的对齐方式："""
    """4.合并单元格效果的实现："""
    """5.设置单元格的大小(见settableSize()函数)"""
    """6 单元格Flag的实现"""

    def setCellFontColor(self):
        newItem = self.item(0, 1)
        newItem.setBackground(Qt.red)
        # newItem.setBackground(QColor(0, 250, 10))
        # newItem.(QColor(200, 111, 100))

    def setCellFontSize(self):
        """
        首先，先生成一个字体QFont对象，并将其字体设为宋体，大小设为12，并且加粗
        再利用单元格的QTableWidgetItem类中的setFont加载给特定的单元格。
        如果需要对所有的单元格都使用这种字体，则可以使用
        self.MyTable.setFont(testFont)
        #利用QTableWidget类中的setFont成员函数，将所有的单元格都设成该字体
        :return:
        """
        textFont = QFont("song", 12, QFont.Bold)

        newItem = QTableWidgetItem("张三")
        # newItem.setBackgroundColor(QColor(0,60,10))
        # newItem.setTextColor(QColor(200,111,100))
        newItem.setFont(textFont)
        self.setItem(0, 0, newItem)

    def setCellAlign(self):
        """
        这个比较简单，使用newItem.setTextAlignment()函数即可，
        该函数的参数为单元格内的对齐方式，和字符输入顺序是自左相右还是自右向左。
        水平对齐方式有：
        Constant         Value  Description
        Qt.AlignLeft    0x0001  Aligns with the left edge.
        Qt.AlignRight   0x0002  Aligns with the right edge.
        Qt.AlignHCenter 0x0004  Centers horizontally in the available space.
        Qt.AlignJustify 0x0008  Justifies the text in the available space.
        垂直对齐方式：
        Constant        Value   Description
        Qt.AlignTop     0x0020  Aligns with the top.
        Qt.AlignBottom  0x0040  Aligns with the bottom.
        Qt.AlignVCenter 0x0080  Centers vertically in the available space.
        如果两种都要设置，只要用 Qt.AlignHCenter |  Qt.AlignVCenter 的方式即可
        :return:
        """
        newItem = QTableWidgetItem("张三")
        newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setItem(0, 0, newItem)

    def setCellSpan(self):
        """
        self.MyTable.setSpan(0, 0, 3, 1)
        # 其参数为： 要改变单元格的   1行数  2列数
        要合并的  3行数  4列数
        :return:
        """
        self.setSpan(0, 0, 3, 1)

    def update_item_data(self, data):
        """更新内容"""
        self.setItem(0, 0, QTableWidgetItem(data))  # 设置表格内容(行， 列) 文字


class UpdateData(QThread):
    """更新数据类"""
    update_date = pyqtSignal(str)

    def run(self):
        cnt = 0
        while True:
            cnt += 1
            self.update_date.emit(str(cnt))
            time.sleep(1)


if __name__ == '__main__':
    # 实例化表格
    app = QApplication(sys.argv)
    myTable = MyTable()
    # 启动更新线程
    # update_data_thread = UpdateData()
    # update_data_thread.update_date.connect(myTable.update_item_data)  # 链接信号
    # update_data_thread.start()

    # 显示在屏幕中央
    # desktop = QApplication.desktop()  # 获取坐标
    # x = (desktop.width() - myTable.width()) // 2
    # y = (desktop.height() - myTable.height()) // 2
    # myTable.move(x, y)  # 移动

    # 显示表格
    myTable.show()
    app.exit(app.exec_())