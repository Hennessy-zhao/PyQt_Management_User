# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5 import QtGui,QtCore


#重写QPushButton
class MyButton(QtGui,QPushButton):
    myclicked=QtCore.pyqtSingal()