import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QMenu, QAction
from ui_mainwindow import Ui_MainWindow
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QDir, Qt
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolBar
from file_Object import file_Object
from PyQt5.QtGui import QIcon, QCursor
import os
from enum import Enum
from PyQt5 import QtCore

class TreeItemType(Enum):    ##节点类型枚举类型
   itTopItem=1001    #顶层节点
   itGroupItem=1002  #组节点
   itImageItem=1003  #图片文件节点

class TreeColNum(Enum):   ##目录树的列号枚举类型
   colItem=0         #分组/文件名列
   colItemType=1     #节点类型列


class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("近场测量系统")
        icon = QIcon("./img/icon2.svg")
        self.ui.action.setIcon(icon)
        icon = QIcon("./img/icon3.svg")
        self.ui.action_4.setIcon(icon)
        icon = QIcon("./img/icon4.svg")
        self.ui.action_1.setIcon(icon)
        icon = QIcon("./img/icon7.svg")
        self.ui.action_2.setIcon(icon)
        ##rcParams[]参数设置，以正确显示汉字
        mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']
        mpl.rcParams['font.size'] = 12
        mpl.rcParams['axes.unicode_minus'] = False
        self.itemFlags = (Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
                          | Qt.ItemIsEnabled | Qt.ItemIsAutoTristate)
        self.ui.mainToolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.__initTree()
        textEdit = self.ui.treeWidget
        textEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        textEdit.customContextMenuRequested[QtCore.QPoint].connect(self.myListWidgetContext)

        #创建绘图系统
        # self.__initFigure()
        #绘图
        # self.__drawFigure()



    #显示近场数据
    @pyqtSlot()
    def __displayFile(self):
        self.__fig=mpl.figure.Figure(figsize=(8, 5))
        self.__fig.suptitle("近场数据")
        figCanvas = FigureCanvas(self.__fig)
        self.setCentralWidget(figCanvas)



    #=======由connectSlotsByName()自动与组件的信号关联的槽函数
    # 这里必须加@pyqtSlot()，因为如果不加这句程序会不知道调用的是有参triggered还是无参，所以程序会执行两次
    @pyqtSlot()
    def on_action_triggered(self):
        dirStr = QFileDialog.getExistingDirectory()  # 选择目录
        if (dirStr == ""):
            return
        icon = QIcon("./img/icon6.svg")
        dirObj = QDir(dirStr)  # QDir对象
        nodeText = dirObj.dirName()  # 最后一级目录的名称
        item = QTreeWidgetItem(TreeItemType.itGroupItem.value)  # 节点类型
        item.setIcon(TreeColNum.colItem.value, icon)
        item.setText(TreeColNum.colItem.value, "工程文件")  # 第1列
        item.setData(TreeColNum.colItem.value, Qt.UserRole, dirStr)  # 关联数据为目录全名
        self.ui.treeWidget.addTopLevelItem(item)
        print(self.ui.treeWidget.topLevelItem(1).data(0, Qt.UserRole))

    def on_action_4_triggered(self):
        sys.exit(app.exec_())

    @pyqtSlot()
    def on_action_1_triggered(self):
        self.__displayFile()

    def __initTree(self):
        #初始化目录树
        self.ui.treeWidget.clear()
        self.ui.treeWidget.header().hide()
        icon = QIcon("./img/icon6")
        item = QTreeWidgetItem(TreeItemType.itTopItem.value)
        item.setIcon(TreeColNum.colItem.value, icon)
        item.setText(TreeColNum.colItem.value, "工程文件")
        # item.setFlags(self.itemFlags)
        # item.setCheckState(TreeColNum.colItem.value, Qt.Checked)

        # item.setData(TreeColNum.colItem.value, Qt.UserRole, "")
        self.ui.treeWidget.addTopLevelItem(item)
        #设置子节点对齐
        # self.ui.treeWidget.setIndentation(0)
        item = QTreeWidgetItem(TreeItemType.itGroupItem.value)
        item.setText(0, "近场数据")
        self.ui.treeWidget.topLevelItem(0).addChild(item)
        item = QTreeWidgetItem(TreeItemType.itGroupItem.value)
        item.setText(0, "远场数据")
        self.ui.treeWidget.topLevelItem(0).addChild(item)

    @pyqtSlot()  ##添加目录节点
    def on_action_4_triggered(self):
        sys.exit(app.exec_())

    # 自定义右键按钮
    def myListWidgetContext(self):
        popMenu = QMenu()
        popMenu.addAction(QAction(u'字体放大', self))
        popMenu.addAction(QAction(u'字体减小', self))
        popMenu.triggered[QAction].connect(self.processtrigger)
        popMenu.exec_(QCursor.pos())

        # 右键按钮事件
    def processtrigger(self, q):
        text = self.newTextEdit.toPlainText()
        if not text.strip():
            return
        # 输出那个Qmenu对象被点击
        if q.text() == "字体放大":
            self.fontSize += 1
        elif q.text() == "字体减小":
            self.fontSize -= 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = QmyMainWindow()
    icon = QIcon("./img/icon1.svg")
    form.setWindowIcon(icon)
    form.show()
    sys.exit(app.exec_())

