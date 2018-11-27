# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5 import  QtSql
import sys

class Demo(QWidget):
    def __init__(self,parent=None):
        super(Demo,self).__init__(parent)
        self.initUI()
        self.resize(1000,1000)

    def initUI(self):
        # 添加数据库
        db = QSqlDatabase.addDatabase("QMYSQL")
        # 设置数据库名称
        db.setDatabaseName("manage_user")
        db.setUserName("root")
        db.setPassword("123456")
        if not db.open():
            print("无法打开数据库")
            return False

        #定义一个数组
        user_list=list()
        query = QtSql.QSqlQuery('select * from user')
        query.first()
        for i in range(query.size()):
            #print(query.value(0), query.value(1))
            sql_list=list()
            sql_list.append(query.value(0))
            sql_list.append(query.value(1))
            sql_list.append(query.value(2))
            user_list.append(sql_list)
            query.next()

        print(user_list)

        #创建表格
        self.user_table=QTableWidget(self)
        self.user_table.setMinimumWidth(1000)
        self.user_table.setMinimumHeight(1000)
        self.user_table.setColumnCount(6)
        self.user_table.setRowCount(10)

        #隐藏水平和垂直表头
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.horizontalHeader().setVisible(False)

        # 设置成员等级的下拉框
        self.btn_selectLevel = QComboBox()
        self.btn_selectLevel.addItems(['权限（全部）', '管理员', '操作者'])


        #设置表格表头
        self.user_table.setItem(0,0,QTableWidgetItem("账号"))
        self.user_table.setItem(0,1,QTableWidgetItem("使用者"))
        self.user_table.setCellWidget(0,2,self.btn_selectLevel)
        self.user_table.setItem(0,3,QTableWidgetItem("修改权限"))
        self.user_table.setItem(0,4,QTableWidgetItem("在线时间"))
        self.user_table.setItem(0,5,QTableWidgetItem("删除"))

        #把数据库中信息放入表格
        for i in range(len(user_list)):
            self.user_table.setItem(i+1,0,QTableWidgetItem(user_list[i][0]))
            self.user_table.setItem(i+1,1,QTableWidgetItem(user_list[i][1]))
            if user_list[i][2]==0:
                self.user_table.setItem(i + 1, 2, QTableWidgetItem('管理员'))
            else:
                self.user_table.setItem(i + 1, 2, QTableWidgetItem('操作者'))

            self.btn_changeLevel=QPushButton("修改")
            self.user_table.setCellWidget(i+1,3,self.btn_changeLevel)

            self.btn_checkTime = QPushButton("查看")
            self.user_table.setCellWidget(i+1,4,self.btn_checkTime)

            self.btn_deleteUser=QPushButton("删除")
            self.user_table.setCellWidget(i+1,5,self.btn_deleteUser)
       
        #关闭数据库
        db.close()

if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Demo()
    form.show()
    sys.exit(app.exec_())


