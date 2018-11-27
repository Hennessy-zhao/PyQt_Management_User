# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys

class Manage_biologyMsg_UI(QObject):
    def setup_biologyMsg_UI(self):
        self.body_checkResult = QWidget()
        self.right_widget.addWidget(self.body_checkResult)
        self.body_checkResult.setStyleSheet('background-color:green')