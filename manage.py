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
        self.is_user_searchID=False    #是否正在进行模糊查询ID操作
        self.user_searchID_content=''   #查询的ID名称
        self.is_user_searchName=False   #是否正在进行模糊查询名字操作
        self.user_searchName_content='' #查询的Name名称


        #显示界面样式
        self.setupUI()

    '''用户部分操作'''

    # regain按钮--即回到原状态按钮被按下
    def userRegainButtonOnClick(self):
        #还原状态，则模糊查询ID和Name的状态为False
        self.is_user_searchID=False
        self.is_user_searchName = False
        self.user_searchID_content = ''
        self.user_searchName_content = ''
        start = 0
        self.user_recordQuery(start, 10)
        # print(self.user_list)
        # 页数改变
        self.user_currentPage = 1
        # 修改页数信息
        self.set_page_messages()
        self.user_updateTable()

    #设置页数，用户数信息
    def set_page_messages(self):
        # 设置总页数
        if len(self.user_list)==10:
            self.user_pageCount=1
        else:
            self.user_pageCount=len(self.user_list)/10+1
        self.label_user_totalPage.setText("总共 " + str(self.user_pageCount) + " 页")
        # 修改总用户数
        self.user_listCount = len(self.user_list)
        # 设置总用户数
        self.label_user_totalRecord.setText("总共 " + str(self.user_listCount) + " 个用户")

    #获取总数据数
    def get_user_listCount(self):
        query = QtSql.QSqlQuery('select * from user')
        return query.numRowsAffected()
    #设置总数据数
    def set_user_listCount(self):
        pass
    #设置总页数
    def set_user_oageCount(self):
        pass
    #设置当前页数
    def set_user_currentPage(self):
        self.label_user_currentPage.setText("当前第 " + str(self.user_currentPage) + " 页")

    #搜索数据库中因页数改变匹配相应数据
    def user_recordQuery(self,start,end):
        query = QtSql.QSqlQuery('select * from user limit %d,%d'%(start,end))

        self.user_list=None
        self.user_list=list()
        query.first()
        for i in range(query.size()):
            #print(query.value(0), query.value(1))
            sql_list = list()
            sql_list.append(query.value(0))
            sql_list.append(query.value(1))
            sql_list.append(query.value(2))
            self.user_list.append(sql_list)
            query.next()
        return True

    # 搜索数据库中因模糊查询匹配相应数据
    def user_recordQuery_vague(self,start,end,field,content):
        print(1)
        sql = "select * from user where "+field+" like \'%"+content + "%\' limit "+str(start)+","+str(end)
        #print(sql)
        query = QtSql.QSqlQuery(sql)
        self.user_list=None
        self.user_list=list()
        query.first()
        for i in range(query.size()):
            #print(query.value(0), query.value(1))
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
        #如果是最后一页，则表格行数是最后一页+1，如果不是，则表格是11行
        if self.user_currentPage==self.user_pageCount:
            self.user_table.setRowCount(len(self.user_list)+1)
        else:
            self.user_table.setRowCount(11)

        #将用户信息显示在桌面上
        for i in range(len(self.user_list)):
            #print(self.user_list[i][0])
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

        #检查按钮是否可以点击
        count=self.user_pageCount
        self.btn_user_pre.setEnabled(False)
        self.btn_user_next.setEnabled(False)
        if self.user_currentPage<count:
            self.btn_user_next.setEnabled(True)
        if self.user_currentPage >1:
            self.btn_user_pre.setEnabled(True)


     # 上一页按钮被按下
    def userPreButtonOnClick(self):
        start = int(self.user_currentPage-2) * 10
        if self.is_user_searchID:
            pass
        elif self.is_user_searchName:
            pass
        else:
            self.user_recordQuery(start, 10)
        # print(self.user_list)
        # 页数减少
        self.user_currentPage -= 1
        self.user_updateTable()
        # 修改当前页数
        self.set_user_currentPage()

    # 下一页按钮被按下
    def userNextButtonOnClick(self):
        start = int(self.user_currentPage)*10
        if self.is_user_searchID:
            self.user_recordQuery_vague(start,10,'id',self.user_searchID_content)
        elif self.is_user_searchName:
            pass
        else:
            self.user_recordQuery(start, 10)
        #页数增加
        self.user_currentPage+=1
        self.user_updateTable()
        #修改当前页数
        self.set_user_currentPage()


    # 跳转页面按钮被按下
    def userSearchPageOnClick(self):
        page=self.user_jump_page.text()
        page=int(page)
        if page<1 or page > self.user_pageCount:
            QMessageBox.warning(self,'输入有误','您输入的页数超过了范围',QMessageBox.Ok)
            return False
        start = int(page-1) * 10
        self.user_recordQuery(start, 10)
        # 页数改变
        self.user_currentPage = page
        self.user_updateTable()
        # 修改当前页数
        self.set_user_currentPage()


    # 搜索账号按钮被按下
    def userSearchIdOnClick(self):
        self.is_user_searchID=True
        self.is_user_searchName=False
        userID=self.search_userID.text()
        self.user_searchID_content=userID
        self.user_recordQuery_vague(0,10,'id',userID)
        # 修改当前页数
        self.user_currentPage=1
        #修改总页数
        if len(self.user_list)==10:
            self.user_pageCount=1
        else:
            self.user_pageCount=int(len(self.user_list)/10)+1
        #设置页数信息
        self.set_page_messages()
        #把查询的信息显示在页面上
        self.user_updateTable()



    # 搜索姓名账号被按下
    def userSearchNameOnClick(self):
        pass


if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Demo()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form.showMaximized()
    sys.exit(app.exec_())
    # 关闭数据库
    db.close()




