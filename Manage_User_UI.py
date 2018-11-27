# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5 import QtWidgets,QtSql
import sys

class Manage_User_UI(QObject):
    def setup_User_UI(self):
        self.user_totalPage = 0
        self.user_currentPage = 0
        self.user_totalRecord = 0

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
        search = QHBoxLayout()
        label2 = QLabel("查找账号：")
        self.search_user = QLineEdit()
        self.btn_search_user = QPushButton("查找")
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        search.addWidget(label2, 0, Qt.AlignLeft)
        search.addWidget(self.search_user, 0, Qt.AlignLeft)
        search.addWidget(self.btn_search_user, 0, Qt.AlignLeft)
        search.addItem(spacerItem1)

        '''表格部分'''
        tab_body = QHBoxLayout()


        # 添加数据库
        db = QSqlDatabase.addDatabase("QMYSQL")
        # 设置数据库名称
        db.setDatabaseName("manage_user")
        db.setUserName("root")
        db.setPassword("123456")
        if not db.open():
            print("无法打开数据库")
            return False

        # 定义一个数组
        user_list = list()
        query = QtSql.QSqlQuery('select * from user')
        query.first()
        for i in range(query.size()):
            # print(query.value(0), query.value(1))
            sql_list = list()
            sql_list.append(query.value(0))
            sql_list.append(query.value(1))
            sql_list.append(query.value(2))
            user_list.append(sql_list)
            query.next()

        print(user_list)

        # 创建表格
        self.user_table = QTableWidget()

        # self.user_table.setMinimumWidth(1000)
        # self.user_table.setMinimumHeight(1000)
        #self.user_table.horizontalHeader().setDefaultSectionSize(200)
        self.user_table.setColumnCount(6)
        self.user_table.setRowCount(10)

        # 隐藏水平和垂直表头
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.horizontalHeader().setVisible(False)

        # 设置成员等级的下拉框
        self.btn_selectLevel = QComboBox()
        self.btn_selectLevel.addItems(['权限（全部）', '管理员', '操作者'])

        # 设置表格表头
        self.user_table.setItem(0, 0, QTableWidgetItem("账号"))
        self.user_table.setItem(0, 1, QTableWidgetItem("使用者"))
        self.user_table.setCellWidget(0, 2, self.btn_selectLevel)
        self.user_table.setItem(0, 3, QTableWidgetItem("修改权限"))
        self.user_table.setItem(0, 4, QTableWidgetItem("在线时间"))
        self.user_table.setItem(0, 5, QTableWidgetItem("删除"))

        # 把数据库中信息放入表格
        for i in range(len(user_list)):
            self.user_table.setItem(i + 1, 0, QTableWidgetItem(user_list[i][0]))
            self.user_table.setItem(i + 1, 1, QTableWidgetItem(user_list[i][1]))
            if user_list[i][2] == 0:
                self.user_table.setItem(i + 1, 2, QTableWidgetItem('管理员'))
            else:
                self.user_table.setItem(i + 1, 2, QTableWidgetItem('操作者'))

            self.btn_changeLevel = QPushButton("修改")
            self.user_table.setCellWidget(i + 1, 3, self.btn_changeLevel)

            self.btn_checkTime = QPushButton("查看")
            self.user_table.setCellWidget(i + 1, 4, self.btn_checkTime)

            self.btn_deleteUser = QPushButton("删除")
            self.user_table.setCellWidget(i + 1, 5, self.btn_deleteUser)

        # 关闭数据库
        db.close()
        tab_body.addWidget(self.user_table)



        '''底部'''
        bottom = QHBoxLayout()
        self.label_user_totalPage = QLabel("总共 " + str(self.user_totalPage) + " 页")
        self.label_user_currentPage = QLabel("当前第 " + str(self.user_currentPage) + " 页")
        self.btn_user_pre = QPushButton("上一页")
        self.btn_user_next = QPushButton("下一页")
        self.user_jump_page = QLineEdit()
        self.user_jump_page.setMaximumWidth(80)
        self.btn_searchPage=QPushButton("跳转")
        self.label_user_totalRecord = QLabel("总共 " + str(self.user_totalRecord) + " 个用户")
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
        bottom.addWidget(self.btn_searchPage)
        bottom.addItem(spacerItem5)
        bottom.addWidget(self.label_user_totalRecord, 0, Qt.AlignRight)

        vlayout = QVBoxLayout()
        vlayout.addLayout(top)
        vlayout.addLayout(search)
        vlayout.addLayout(tab_body)
        vlayout.addLayout(bottom)
        self.body_user_manage.setLayout(vlayout)


