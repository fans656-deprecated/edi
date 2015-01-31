# coding: utf-8
import sys
import string

from PySide.QtCore import *
from PySide.QtGui import *

import util
from document import Document
from view import View
from controller import Controller

text = '''\
hello world
this is just a test a   b
and what do you want?
you me evo\
'''

class Widget(QDialog):

    __metaclass__ = util.metaclass

    def __init__(self, parent=None):
        self.super().__init__(parent)

        self.documents = []
        self.views = []
        self.controllers = []

        self.newDocument()

    def newDocument(self):
        document = Document()
        document.text = text

        view = View()
        view.font = self.font()
        view.cursorBlinkingTime = 1000
        view.position = QPoint(0, 0)
        view.size = self.size()

        controller = Controller()
        controller.add(view)

        # if a view is relink with another document
        # then it can finds its old controller from old document
        # and new controller from new document
        controller.document = document
        document.controller = controller

        self.documents.append(document)
        self.views.append(view)
        self.controllers.append(controller)

    def keyPressEvent(self, ev):
        ch = ev.text()
        key = ev.key()
        # \r 属于 string.printable ，所以要优先判断
        #if ch and ch in '\r\n':
        #    self.document.newLine()
        #elif key == Qt.Key_Backspace:
        #    self.document.delBack()
        #elif ch and ch in string.printable:
        #    self.document.putChar(ch)
        #elif key == Qt.Key_Up:
        #    self.document.cursorUp()
        #elif key == Qt.Key_Down:
        #    self.document.cursorDown()
        #elif key == Qt.Key_Left:
        #    self.document.cursorLeft()
        #elif key == Qt.Key_Right:
        #    self.document.cursorRight()
        #self.update()

    def paintEvent(self, ev):
        painter = QPainter(self)
        for controller in self.controllers:
            controller.draw(painter)

app = QApplication(sys.argv)
w = Widget()
w.setFont(QFont('Courier New', 10))
w.resize(480, 320)
w.show()
app.exec_()
