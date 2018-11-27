# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Manage_UI import Manage_UI
import sys
import qdarkstyle

class Demo(QWidget,Manage_UI):
    def __init__(self,parent=None):
        super(Demo,self).__init__(parent)

        self.setupUI()

if __name__=='__main__':
    app=QApplication(sys.argv)
    form=Demo()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form.showMaximized()
    sys.exit(app.exec_())


