# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Manage_User_UI import Manage_User_UI
from Manage_checkResult_UI import Manage_checkResult_UI
from Manage_biologyMsg_UI import Manage_biologyMsg_UI
import sys

class Manage_UI(Manage_User_UI,Manage_checkResult_UI,Manage_biologyMsg_UI):
    def setupUI(self):
        self.setWindowTitle("管理界面")
        # 设置软件logo
        self.setWindowIcon(QIcon('./images/logo_1.png'))
        # 窗口的整体布局
        self.main_layout = QHBoxLayout(self, spacing=0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧选项列表
        self.left_widget = QListWidget()
        # 修改左侧选项列表的样式
        style = '''
                     QListWidget {             
                        max-width: 200px;
                        min-width:200px;
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
        self.setup_User_UI()

        # 添加检查汇总模块右边栏
        self.setup_checkResult_UI()

        # 添加生物信息模块右边栏
        self.setup_biologyMsg_UI()

