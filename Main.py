import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
class Main(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi("")