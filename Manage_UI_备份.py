# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys

class Manage_UI(QObject):
    def setupUI(self):
        self.setWindowTitle("管理界面")
        # 窗口的整体布局
        self.main_layout = QHBoxLayout(self, spacing=0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧选项列表
        self.left_widget = QListWidget()
        # 修改左侧选项列表的样式
        style = '''
                     QListWidget {             
                        max-width: 200px;
                        font: 12pt \"微软雅黑\";
                     }
                     QListWidget::Item{
                        padding:20px 50px;
                        border-bottom:1px solid rgb(24,70,93)
                     }
                '''
        self.left_widget.setStyleSheet(style)
        self.main_layout.addWidget(self.left_widget)
        self.right_widget = QStackedWidget()
        self.main_layout.addWidget(self.right_widget)

        # list和右侧窗口的index对应绑定
        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)

        list_str = ['用户管理', '检查汇总', '生物信息']

        # 添加左侧选项卡
        for i in range(3):
            self.item = QListWidgetItem(list_str[i], self.left_widget)

        # 添加用户管理模块右边栏
        self.userManage()

        # 添加检查汇总模块右边栏
        self.checkResult()

        # 添加生物信息模块右边栏
        self.biologyMsg()

        # 用户管理模块具体内容

    def userManage(self):
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

        # 头部部分
        top = QHBoxLayout()
        label1 = QLabel("用户信息管理")
        label1.setProperty('name', 'body_user_label1')
        self.btn_addUser = QPushButton("添加新用户")
        self.btn_addUser.setProperty('name', 'body_user_btnAddUser')
        top.addWidget(label1, 0, Qt.AlignLeft)
        top.addWidget(self.btn_addUser, 0, Qt.AlignRight)

        # 查询部分
        search = QHBoxLayout()
        label2 = QLabel("查找账号：")
        self.search_user = QLineEdit()
        self.btn_search_user = QPushButton("Go")
        search.addWidget(label2, 0, Qt.AlignLeft)
        search.addWidget(self.search_user, 0, Qt.AlignLeft)
        search.addWidget(self.btn_search_user, 0, Qt.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        search.addItem(spacerItem)

        # 表格部分
        tab_body = QWidget()
        tab_body.setMinimumHeight(500)

        # 底部
        bottom = QHBoxLayout()
        self.label_user_totalPage = QLabel("总共 " + str(self.user_totalPage) + " 页")
        self.label_user_currentPage = QLabel("当前第 " + str(self.user_currentPage) + " 页")
        self.btn_user_pre = QPushButton("上一页")
        self.btn_user_next = QPushButton("下一页")
        self.user_jump_page = QLineEdit()
        self.label_user_totalRecord = QLabel("总共 " + str(self.user_totalRecord) + " 个用户")

        bottom.addWidget(self.label_user_totalPage, 0, Qt.AlignLeft)
        bottom.addWidget(self.label_user_currentPage, 0, Qt.AlignLeft)
        bottom.addWidget(self.btn_user_pre)
        bottom.addWidget(self.btn_user_next)
        bottom.addWidget(QLabel("跳转到第"), 0, Qt.AlignLeft)
        bottom.addWidget(self.user_jump_page)
        bottom.addWidget(QLabel("页"), 0, Qt.AlignLeft)
        bottom.addWidget(self.label_user_totalRecord, 0, Qt.AlignRight)

        vlayout = QVBoxLayout()
        vlayout.addLayout(top)
        vlayout.addLayout(search)
        vlayout.addWidget(tab_body)
        vlayout.addLayout(bottom)
        self.body_user_manage.setLayout(vlayout)

        # 检查汇总模块具体内容

    def checkResult(self):
        self.body_checkResult = QWidget()
        self.right_widget.addWidget(self.body_checkResult)
        self.body_checkResult.setStyleSheet('background-color:green')

        # 用户管理模块具体内容

    def biologyMsg(self):
        self.body_biologyMsg = QWidget()
        self.right_widget.addWidget(self.body_biologyMsg)
        self.body_biologyMsg.setStyleSheet('background-color:blue')
