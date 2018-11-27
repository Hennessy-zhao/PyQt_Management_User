# -*- coding:UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys

class Manage_checkResult_UI(QObject):
    def setup_checkResult_UI(self):
        self.body_biologyMsg = QWidget()
        self.right_widget.addWidget(self.body_biologyMsg)
        self.body_biologyMsg.setStyleSheet('background-color:blue')