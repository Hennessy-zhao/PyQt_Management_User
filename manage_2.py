# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5 import QtSql
from functools import partial
from Manage_UI import Manage_UI
from CommonHelper import CommonHelper
import sys
import re

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
        self.user_searchLevel_num=None  #目前查询是否有关level

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
            #以下是循环显示按钮的界面

            self.btn_changeLevel = QPushButton("修改")
            self.user_table.setCellWidget(i + 1, 3, self.btn_changeLevel)

            self.btn_changeLevel.clicked.connect(partial(self.showChangeUserLevelDialog, self.user_list[i][0],self.user_list[i][1],self.user_list[i][2]))

            self.btn_checkTime = QPushButton("查看")
            self.user_table.setCellWidget(i + 1, 4, self.btn_checkTime)

            self.btn_deleteUser = QPushButton("删除")
            self.user_table.setCellWidget(i + 1, 5, self.btn_deleteUser)

            self.btn_deleteUser.clicked.connect(partial(self.userDeleteButtonOnClick, self.user_list[i][0],self.user_list[i][1]))



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
            if self.user_searchLevel_num!=None:
                level=self.user_searchLevel_num
                sql = "select * from user where level="+str(level)+" and " + field + " like \'%" + content + "%\' limit " + str(
                    start) + "," + str(count)
            else:
                sql = "select * from user where " + field + " like \'%" + content + "%\' limit " + str(start) + "," + str(count)
            query = QtSql.QSqlQuery(sql)
        else:
            if self.user_searchLevel_num!=None:
                level=self.user_searchLevel_num
                query = QtSql.QSqlQuery('select * from user where level=%d limit %d,%d' % (level,start, count))
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
        #level级别设置为None
        self.btn_selectLevel.setCurrentIndex(0)
        self.user_searchLevel_num=None
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
            if self.user_searchLevel_num!=None:
                level=self.user_searchLevel_num
                query = QtSql.QSqlQuery("select * from user where level="+str(level)+" and " + field + " like \'%" + content + "%\'")
            else:
                query = QtSql.QSqlQuery("select * from user where "+field +" like \'%"+content+"%\'")
        else:
            if self.user_searchLevel_num!=None:
                query = QtSql.QSqlQuery("select * from user where level=%d"%self.user_searchLevel_num)
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
            box = QMessageBox(QMessageBox.Warning, "输入有误", "您输入的页数超过了范围")
            box.addButton(self.tr("确定"), QMessageBox.YesRole)
            box.exec_()
            return False
        start = int(page-1) * 10
        #print(start)
        # 页数改变
        self.user_currentPage=page
        self.user_update(start_s=start,count_s=10)


    # 搜索账号按钮被按下
    def userSearchIdOnClick(self):
        self.btn_selectLevel.setCurrentIndex(0)
        self.user_searchLevel_num = None
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
        self.btn_selectLevel.setCurrentIndex(0)
        self.user_searchLevel_num=None
        self.is_user_searchID = False
        self.is_user_searchName = True
        userName = self.search_username.text()
        self.user_searchName_content = userName
        self.user_describe.setText("以下为您搜索的姓名信息和 " + userName + " 有关的用户信息")
        # 修改当前页数
        self.user_currentPage = 1
        self.user_update(start_s=0, count_s=10)


    #根据权限查看用户
    def userSelectLevelOnClick(self,i):
        if i==1:
            self.user_searchLevel_num=0
        elif i==2:
            self.user_searchLevel_num=1
        else:
            self.user_searchLevel_num=None

        self.user_update(start_s=0, count_s=10)




    #删除用户按钮被点击
    def userDeleteButtonOnClick(self,userid,username):
        reply = QMessageBox(QMessageBox.Question, "删除用户", "您确定删除该用户吗？？\n 账号："+userid+" \n使用者："+username)
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == qyes:
            sql = "delete from user where id ='" + str(userid) + "'"
            query = QtSql.QSqlQuery(sql)
            if query.numRowsAffected()>0:
                box = QMessageBox(QMessageBox.Information, "删除成功", "您已成功删除该用户")
                box.addButton(self.tr("确定"), QMessageBox.YesRole)
                box.exec_()
            self.user_currentPage=1
            self.user_update(start_s=0, count_s=10)



    '''修改用户权限部分操作'''
    def userChangeLevelButtonOnClick(self,id,name):
        if self.btn_user_change_level1.isChecked():
            level=0
            text="管理员"
        else:
            level=1
            text="操作员"
        reply = QMessageBox(QMessageBox.Question, "修改权限", "您确定修改该用户权限为 "+text+" 吗？？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == qyes:
            sql="UPDATE user SET level = %d WHERE id = %s"%(level,id)
            query = QtSql.QSqlQuery(sql)
            if query.numRowsAffected()>0:
                box = QMessageBox(QMessageBox.Information, "修改成功", "您已成功修改该用户权限")
                box.addButton(self.tr("确定"), QMessageBox.YesRole)
                box.exec_()
            self.user_currentPage=1
            self.user_update(start_s=0, count_s=10)


    ''' 添加新用户部分操作 '''
    #验证id是否重复
    def user_verify_id(self,text):
        sql = "select * from user where id ='"+text+"'"
        query = QtSql.QSqlQuery(sql)

        if text =='':
            self.user_addid_icon.setPixmap(QPixmap(""))
            self.user_addid_msg.setText('')
        else:
            match = re.search("^[0-9]*$", text)
            if query.numRowsAffected() > 0:
                self.user_addid_icon.setPixmap(QPixmap("./images/no_1.png"))
                self.user_addid_msg.setText("账号已存在")
            elif not match:
                self.user_addid_icon.setPixmap(QPixmap("./images/no_1.png"))
                self.user_addid_msg.setText("账号不符合规范")
            else :
                self.user_addid_icon.setPixmap(QPixmap("./images/yes_1.png"))
                self.user_addid_msg.setText('')


    #验证name是否符合姓名规范
    def user_verify_name(self,text):
        if text=='':
            self.user_addname_icon.setPixmap(QPixmap(""))
            self.user_addname_msg.setText('')
        else:
            match = re.search("^[\u4E00-\u9FA5\uf900-\ufa2d·s]{2,20}$", text)
            if not match:
                self.user_addname_icon.setPixmap(QPixmap("./images/no_1.png"))
                self.user_addname_msg.setText("姓名不符合规范")
            else:
                self.user_addname_icon.setPixmap(QPixmap("./images/yes_1.png"))
                self.user_addname_msg.setText('')


    #清空AddUserDialog按钮被按下
    def reset_AddUserDialog(self):
        self.user_addid.setText('')
        self.user_addname.setText('')
        self.user_add_level_2.setChecked(True)


    #添加新用户的按钮被按下
    def addnewuserButtonOnClick(self):
        reply=QMessageBox(QMessageBox.Question, "是否添加用户", "您确定添加该用户吗？？")
        qyes=reply.addButton(self.tr("确定"),QMessageBox.YesRole)
        qno=reply.addButton(self.tr("取消"),QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton()==qyes:
            new_id=self.user_addid.text()
            new_name=self.user_addname.text()

            if self.user_add_level_1.isChecked()==True:
                new_level=0
            else:
                new_level=1

        sql = "insert into user values(\'"+new_id+"\',\'"+new_name+"\',"+str(new_level)+")"
        query = QtSql.QSqlQuery(sql)
        if query.numRowsAffected() > 0:
            self.user_currentPage=1
            self.user_update(start_s=0, count_s=10)
            box = QMessageBox(QMessageBox.Information, "添加成功", "您已成功添加用户")
            box.addButton(self.tr("确定"), QMessageBox.YesRole)
            box.exec_()


if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Demo()
    styleFile = './manage.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    app.setStyleSheet(qssStyle)
    form.showMaximized()
    sys.exit(app.exec_())
    # 关闭数据库
    db.close()






