# coding: utf-8
import sys
import string

from PySide.QtCore import *
from PySide.QtGui import *

import util

class Text(object):

    def __init__(self):
        self.s = u''

    def backspace(self):
        self.s = self.s[:-1]
        self.show()

    def __iadd__(self, other):
        self.s += other
        self.show()
        return self

    def show(self):
        print repr(self.s)

class Edi(QDialog):

    __metaclass__ = util.metaclass

    def __init__(self, parent=None):
        self.super().__init__(parent)
        self.text = Text()
        self.setAttribute(Qt.WA_InputMethodEnabled)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.resize(320, 240)

    def keyPressEvent(self, event):
        ch = event.text()
        if ch == '\b':
            self.text.backspace()
        elif ch and ch in '\r\n':
            self.text += '\n'
        elif ch in string.printable:
            self.text += ch
        self.update()
        self.super().keyPressEvent(event)

    def inputMethodEvent(self, event):
        s = event.commitString()
        if s:
            self.text += s
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        font = p.font()
        font.setPointSize(40)
        p.setFont(font)
        p.drawText(self.rect(), self.text.s)

app = QApplication(sys.argv)
edi = Edi()
edi.show()
app.exec_()
