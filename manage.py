# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5 import QtSql
from Manage_UI import Manage_UI
import sys
import qdarkstyle

class Demo(QWidget,Manage_UI):
    def __init__(self,parent=None):
        super(Demo,self).__init__(parent)

        '''用户部分的变量'''
        self.user_list=list()       #存储用户信息的数组
        self.user_listCount=0       #用户总个数
        self.user_pageCount=0       #总页数
        self.user_currentPage=1     #当前页数

        self.setupUI()

    '''用户部分操作'''
    #获取总数据数
    def get_user_listCount(self):
        pass
    #设置总数据数
    def set_user_listCount(self):
        pass
    #设置总页数
    def set_user_oageCount(self):
        pass
    #设置当前页数
    def set_user_currentPage(self):
        pass

    #搜索数据库中相应数据
    def user_recordQuery(self,start,end):
        query = QtSql.QSqlQuery('select * from user limit %d,%d'%(start,end))
        query.first()
        for i in range(query.size()):
            # print(query.value(0), query.value(1))
            sql_list = list()
            sql_list.append(query.value(0))
            sql_list.append(query.value(1))
            sql_list.append(query.value(2))
            self.user_list.append(sql_list)
            query.next()
        return True

    #刷新界面-把数据库中的信息展示在用户界面上
    def user_updateTable(self):
        #print(len(self.user_list))
        for i in range(len(self.user_list)):
            print(self.user_list[i][0])
            text1 = QTableWidgetItem(self.user_list[i][0])
            text1.setTextAlignment(Qt.AlignCenter)
            text2 = QTableWidgetItem(self.user_list[i][1])
            text2.setTextAlignment(Qt.AlignCenter)

            self.user_table.setItem(i + 1, 0, text1)
            self.user_table.setItem(i + 1, 1, text2)
            if self.user_list[i][2] == 0:
                text3 = QTableWidgetItem('管理员')
                text3.setTextAlignment(Qt.AlignCenter)
                self.user_table.setItem(i + 1, 2, text3)
            else:
                text3 = QTableWidgetItem('操作员')
                text3.setTextAlignment(Qt.AlignCenter)
                self.user_table.setItem(i + 1, 2, text3)

            self.btn_changeLevel = QPushButton("修改")
            self.user_table.setCellWidget(i + 1, 3, self.btn_changeLevel)

            self.btn_checkTime = QPushButton("查看")
            self.user_table.setCellWidget(i + 1, 4, self.btn_checkTime)

            self.btn_deleteUser = QPushButton("删除")
            self.user_table.setCellWidget(i + 1, 5, self.btn_deleteUser)


if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Demo()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form.showMaximized()
    sys.exit(app.exec_())




