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
        #self.user_listCount=0       #用户总个数
        #self.user_pageCount=0       #总页数
        self.user_currentPage=1     #当前页数
        self.is_user_searchID=False    #是否正在进行模糊查询ID操作
        self.user_searchID_content=''   #查询的ID名称
        self.is_user_searchName=False   #是否正在进行模糊查询名字操作
        self.user_searchName_content='' #查询的Name名称

        #显示界面样式
        self.setupUI()

        #界面数据刷新显示
        self.user_update()

    '''用户部分操作'''

    # 刷新界面-把数据库中的信息展示在用户界面上
    def user_update(self,start_s=0,count_s=10):
        if self.is_user_searchID:
            self.user_recordQuery(start=start_s,count=count_s,field='id',content=self.user_searchID_content)
            # 获得总数据数
            list_count = self.get_user_listCount(field='id',content=self.user_searchID_content)
        elif self.is_user_searchName:
            self.user_recordQuery(start=start_s,count=count_s,field='name',content=self.user_searchName_content)
            # 获得总数据数
            list_count = self.get_user_listCount(field='name',content=self.user_searchName_content)
        else:
            self.user_recordQuery(start=start_s,count=count_s)
            # 获得总数据数
            list_count=self.get_user_listCount()
        #print(list_count)

        #获得总页数
        page_count=self.get_user_pageCount()


        #设置总页数
        self.label_user_totalPage.setText("总共 " + str(page_count) + " 页")

        #设置总数据数
        self.label_user_totalRecord.setText("总共 " + str(list_count) + " 个用户")

        #设置当前页数
        self.label_user_currentPage.setText("当前第 " + str(self.user_currentPage) + " 页")

        #如果是最后一页，则表格行数是最后一页+1，如果不是，则表格是11行
        if self.user_currentPage==page_count:
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
        self.btn_user_pre.setEnabled(False)
        self.btn_user_next.setEnabled(False)
        if self.user_currentPage<page_count:
            self.btn_user_next.setEnabled(True)
        if self.user_currentPage >1:
            self.btn_user_pre.setEnabled(True)

    # 搜索数据库中相应数据
    def user_recordQuery(self, start,count,field=None,content=None):
        if field:
            sql = "select * from user where " + field + " like \'%" + content + "%\' limit " + str(start) + "," + str(count)
            query = QtSql.QSqlQuery(sql)
        else:
            query = QtSql.QSqlQuery('select * from user limit %d,%d' % (start, count))
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

    # regain按钮--即回到原状态按钮被按下
    def userRegainButtonOnClick(self):
        #修改提示label
        self.user_describe.setText("以下为所有用户的信息")
        #还原状态，则模糊查询ID和Name的状态为False
        self.is_user_searchID=False
        self.is_user_searchName = False
        self.user_searchID_content = None
        self.user_searchName_content = None
        # 页数改变
        self.user_currentPage = 1
        self.user_update(start_s=0,count_s=10)
        #清空搜索页数据
        self.search_userID.setText('')
        self.search_username.setText('')
        self.user_jump_page.setText('')


    #获取总数据数
    def get_user_listCount(self,field=None,content=None):
        if field:
            query = QtSql.QSqlQuery("select * from user where "+field +" like \'%"+content+"%\'")
        else:
            query = QtSql.QSqlQuery("select * from user")

        return query.numRowsAffected()

    #获取总页数
    def get_user_pageCount(self):
        if self.is_user_searchID:
            list_count = self.get_user_listCount(field='id',content=self.user_searchID_content)
        elif self.is_user_searchName:
            list_count=self.get_user_listCount(field='name',content=self.user_searchName_content)
        else:
            list_count=self.get_user_listCount()
        if list_count==10:
            page_count=1
        else:
            page_count=int(list_count/10)+1
        return page_count


     # 上一页按钮被按下
    def userPreButtonOnClick(self):
        start = int(self.user_currentPage-2) * 10
        # 页数增加
        self.user_currentPage -= 1
        self.user_update(start_s=start, count_s=10)

    # 下一页按钮被按下
    def userNextButtonOnClick(self):
        start = int(self.user_currentPage)*10
        #页数增加
        self.user_currentPage += 1
        self.user_update(start_s=start,count_s=10)


    # 跳转页面按钮被按下
    def userSearchPageOnClick(self):
        page=self.user_jump_page.text()
        page=int(page)
        # 获取总页数
        page_count=self.get_user_pageCount()

        if page<1 or page > page_count:
            QMessageBox.warning(self,'输入有误','您输入的页数超过了范围',QMessageBox.Ok)
            return False
        start = int(page-1) * 10
        #print(start)
        # 页数改变
        self.user_currentPage=page
        self.user_update(start_s=start,count_s=10)


    # 搜索账号按钮被按下
    def userSearchIdOnClick(self):
        self.is_user_searchID=True
        self.is_user_searchName=False
        userID=self.search_userID.text()
        self.user_searchID_content=userID
        self.user_describe.setText("以下为您搜索的账号信息和 " + userID + " 有关的用户信息")
        # 修改当前页数
        self.user_currentPage=1
        self.user_update(start_s=0,count_s=10)



    # 搜索姓名账号被按下
    def userSearchNameOnClick(self):
        self.is_user_searchID = False
        self.is_user_searchName = True
        userName = self.search_username.text()
        self.user_searchName_content = userName
        self.user_describe.setText("以下为您搜索的姓名信息和 " + userName + " 有关的用户信息")
        # 修改当前页数
        self.user_currentPage = 1
        self.user_update(start_s=0, count_s=10)


if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Demo()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form.showMaximized()
    sys.exit(app.exec_())
    # 关闭数据库
    db.close()




