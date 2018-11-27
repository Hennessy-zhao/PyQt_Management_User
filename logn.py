# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import qdarkstyle

class Login(QWidget):
    def __init__(self,parent=None):
        super(Login,self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("登录")

        self.user_ID=QLineEdit()
        self.user_pad=QLineEdit()

        grid=QGridLayout()
        grid.addWidget(QLabel("账号："),0,0)
        grid.addWidget(self.user_ID,0,1)
        grid.addWidget(QLabel("密码："),1,0)
        grid.addWidget(self.user_pad,1,1)
        grid.setSpacing(20)

        vlayout=QVBoxLayout()
        vlayout.addSpacing(20)
        vlayout.addLayout(grid)
        vlayout.addSpacing(20)
        vlayout.addWidget(QPushButton("登录"),Qt.AlignCenter)
        vlayout.addSpacing(20)

        widget=QWidget()
        widget.setLayout(vlayout)
        screen=QDesktopWidget().screenGeometry()
        widget.setMaximumSize(screen.width()/6,screen.height()/3)
        widget.setMinimumSize(300,280)
        widget.setStyleSheet("font: 14pt \"微软雅黑\";")


        hlayout=QHBoxLayout()
        hlayout.addWidget(widget,Qt.AlignCenter)

        self.setLayout(hlayout)




if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Login()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form.showMaximized()
    sys.exit(app.exec_())


