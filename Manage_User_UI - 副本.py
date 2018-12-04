# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5 import QtWidgets,QtSql
import sys

class Manage_User_UI(QObject):
    def setup_User_UI(self):

        self.body_user_manage = QWidget()
        self.right_widget.addWidget(self.body_user_manage)
        self.body_user_manage.setMinimumWidth(500)
        style = '''
                    *{
                        font: 12pt \"微软雅黑\";
                    }

                    QLabel[name='body_user_label1']{
                        font-size:14pt
                    }

                    QPushButton[name='body_user_btnAddUser']{
                        padding:10px;
                        font-size:11pt;
                    }
                    
                   
                    
                '''
        self.body_user_manage.setStyleSheet(style)


        '''头部部分'''
        top = QHBoxLayout()
        label1 = QLabel("用户信息管理")
        label1.setProperty('name', 'body_user_label1')
        self.btn_addUser = QPushButton("添加新用户")
        self.btn_addUser.setProperty('name', 'body_user_btnAddUser')
        top.addWidget(label1, 0, Qt.AlignLeft)
        top.addWidget(self.btn_addUser, 0, Qt.AlignRight)

        '''查询部分'''
        # self.user_regain=QLabel()
        # self.user_regain.setPixmap(QPixmap('./images/regain.png'))
        #令label中的图片自适应label大小
        #self.user_regain.setScaledContents(True)
        #self.user_regain.setToolTip("点击回到原始状态")
        #self.user_regain.setMaximumSize(30,30)
        self.btn_user_regain = QPushButton()
        self.btn_user_regain.setIcon(QIcon(QPixmap('./images/regain.png')))
        self.btn_user_regain.setIconSize(QSize(30,30))
        spacerItem0 = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        search = QHBoxLayout()
        label2 = QLabel("账号查询：")
        self.search_userID = QLineEdit()
        self.btn_search_userID = QPushButton("查找")
        spacerItem1 = QtWidgets.QSpacerItem(30, 0, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        label3=QLabel("姓名查询：")
        self.search_username=QLineEdit()
        self.btn_search_username=QPushButton("查找")
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        search.addWidget(self.btn_user_regain,0,Qt.AlignLeft)
        search.addItem(spacerItem0)
        search.addWidget(label2, 0, Qt.AlignLeft)
        search.addWidget(self.search_userID, 0, Qt.AlignLeft)
        search.addWidget(self.btn_search_userID, 0, Qt.AlignLeft)
        search.addItem(spacerItem1)
        search.addWidget(label3, 0, Qt.AlignLeft)
        search.addWidget(self.search_username, 0, Qt.AlignLeft)
        search.addWidget(self.btn_search_username, 0, Qt.AlignLeft)
        search.addItem(spacerItem2)

        '''表格部分'''
        tab_body = QVBoxLayout()

        # 添加数据库
        db = QSqlDatabase.addDatabase("QMYSQL")
        # 设置数据库名称
        db.setDatabaseName("manage_user")
        db.setUserName("root")
        db.setPassword("123456")
        if not db.open():
            print("无法打开数据库")
            return False

        # 建设初始化表格，即
        self.user_recordQuery(0,10)
        #print(self.user_list)
        # 创建表格

        self.user_table = QTableWidget()

        screen = QDesktopWidget().screenGeometry()
        self.user_table.setMaximumHeight(screen.height()-250)
        # self.user_table.setMinimumWidth(1000)
        # self.user_table.setMinimumHeight(1000)

        # 修改表格大小

        #print(int((screen.width() - 200) / 6))
        tab_detault_w=int((screen.width() - 300) / 6)
        tab_detault_h=int((screen.height()-300)/11)
        self.user_table.horizontalHeader().setDefaultSectionSize(tab_detault_w)
        self.user_table.verticalHeader().setDefaultSectionSize(tab_detault_h)
        self.user_table.setColumnCount(6)
        self.user_table.setRowCount(11)

        # 隐藏水平和垂直表头
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.horizontalHeader().setVisible(False)

        # 设置成员等级的下拉框
        self.btn_selectLevel = QComboBox()
        self.btn_selectLevel.addItems(['  权限（全部）', '  管理员', '  操作者'])

        # 设置表格表头
        text1=QTableWidgetItem("账号")
        text1.setTextAlignment(Qt.AlignCenter)
        text2 = QTableWidgetItem("使用者")
        text2.setTextAlignment(Qt.AlignCenter)
        text3 = QTableWidgetItem("修改权限")
        text3.setTextAlignment(Qt.AlignCenter)
        text4 = QTableWidgetItem("在线时间")
        text4.setTextAlignment(Qt.AlignCenter)
        text5 = QTableWidgetItem("删除")
        text5.setTextAlignment(Qt.AlignCenter)
        self.user_table.setItem(0, 0, text1)
        self.user_table.setItem(0, 1, text2)
        self.user_table.setCellWidget(0, 2, self.btn_selectLevel)
        self.user_table.setItem(0, 3, text3)
        self.user_table.setItem(0, 4, text4)
        self.user_table.setItem(0, 5, text5)

        tab_body.addWidget(self.user_table)



        '''底部'''
        # 获取用户总个数
        self.user_listCount = self.get_user_listCount()

        # 获取总页数
        if self.user_listCount==10:
            self.user_pageCount=1
        else:
            self.user_pageCount = int(self.user_listCount / 10 + 1)


        bottom = QHBoxLayout()
        self.label_user_totalPage = QLabel("总共 " + str(self.user_pageCount) + " 页")
        self.label_user_currentPage = QLabel("当前第 " + str(self.user_currentPage) + " 页")
        self.btn_user_pre = QPushButton("上一页")
        self.btn_user_next = QPushButton("下一页")
        #设置跳转页输入框
        self.user_jump_page = QLineEdit()
        self.user_jump_page.setMaximumWidth(80)
        #只能输入数字
        userJumpPage_reg=QRegExp("^-?\d+$")
        userJumpPage_Validator=QRegExpValidator(self)
        userJumpPage_Validator.setRegExp(userJumpPage_reg)
        self.user_jump_page.setValidator(userJumpPage_Validator)
        #设置跳转按钮
        self.btn_user_searchPage=QPushButton("跳转")
        self.label_user_totalRecord = QLabel("总共 " + str(self.user_listCount) + " 个用户")
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        spacerItem3 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        spacerItem4 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        spacerItem5 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        bottom.addWidget(self.label_user_totalPage, 0, Qt.AlignLeft)
        bottom.addItem(spacerItem2)
        bottom.addWidget(self.label_user_currentPage, 0, Qt.AlignLeft)
        bottom.addItem(spacerItem3)
        bottom.addWidget(self.btn_user_pre)
        bottom.addWidget(self.btn_user_next)
        bottom.addItem(spacerItem4)
        bottom.addWidget(QLabel("跳转到第"), 0, Qt.AlignLeft)
        bottom.addWidget(self.user_jump_page)
        bottom.addWidget(QLabel("页"), 0, Qt.AlignLeft)
        bottom.addWidget(self.btn_user_searchPage)
        bottom.addItem(spacerItem5)
        bottom.addWidget(self.label_user_totalRecord, 0, Qt.AlignRight)

        vlayout = QVBoxLayout()
        vlayout.addLayout(top)
        vlayout.addLayout(search)
        vlayout.addLayout(tab_body)
        vlayout.addLayout(bottom)
        self.body_user_manage.setLayout(vlayout)

        # 把数据库中信息放入表格
        self.user_updateTable()

        #regain按钮--即回到原状态按钮被按下
        self.btn_user_regain.clicked.connect(self.userRegainButtonOnClick)

        #上一页按钮被按下
        self.btn_user_pre.clicked.connect(self.userPreButtonOnClick)

        #下一页按钮被按下
        self.btn_user_next.clicked.connect(self.userNextButtonOnClick)

        #跳转页面按钮被按下
        self.btn_user_searchPage.clicked.connect(self.userSearchPageOnClick)

        #搜索账号按钮被按下
        self.btn_search_userID.clicked.connect(self.userSearchIdOnClick)

        #搜索姓名账号被按下
        self.btn_search_username.clicked.connect(self.userSearchNameOnClick)


