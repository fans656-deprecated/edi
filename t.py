# coding: utf-8
import sys
import string

from PySide.QtCore import *
from PySide.QtGui import *

import util
import document

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
        self.document = document.Document()
        self.document.setText(text)
        self.layouts = []
        self.cursorTimer = QTimer()
        self.isShowingCursor = True
        self.cursorTimer.timeout.connect(self.cursorTimeout)
        self.cursorTimer.setInterval(500)
        self.cursorTimer.start()

    def cursorTimeout(self):
        self.isShowingCursor = not self.isShowingCursor
        self.update()

    def keyPressEvent(self, ev):
        ch = ev.text()
        key = ev.key()
        # \r 属于 string.printable ，所以要优先判断
        if ch and ch in '\r\n':
            self.document.newLine()
        elif key == Qt.Key_Backspace:
            self.document.delBack()
        elif ch and ch in string.printable:
            self.document.putChar(ch)
        elif key == Qt.Key_Up:
            self.document.cursorUp()
        elif key == Qt.Key_Down:
            self.document.cursorDown()
        elif key == Qt.Key_Left:
            self.document.cursorLeft()
        elif key == Qt.Key_Right:
            self.document.cursorRight()
        self.update()

    def layout(self):
        lines = self.document.lines
        self.layouts = []
        for line in lines:
            self.layoutLine(line)

    def layoutLine(self, line):
        fm = self.fontMetrics()
        self.fm = fm
        leading = fm.leading()
        y = 0.0
        lt = QTextLayout(line)
        to = lt.textOption()
        to.setWrapMode(QTextOption.WrapAnywhere)
        to.setTabStop(fm.width(' ') * 8)
        lt.setTextOption(to)
        lt.setFont(self.font())
        lt.setCacheEnabled(True)
        lt.beginLayout()
        while True:
            line = lt.createLine()
            if not line.isValid():
                break
            line.setLineWidth(self.width())
            y += leading
            line.setPosition(QPointF(0.0, y))
            y += line.height()
        lt.endLayout()
        self.layouts.append(lt)

    def paintEvent(self, ev):
        self.layout()
        painter = QPainter(self)
        pt = QPoint(0, 0)
        for i, lt in enumerate(self.layouts):
            lt.draw(painter, pt)
            if i == self.document.iLine and self.isShowingCursor:
                lt.drawCursor(painter, pt, self.document.iCol, 1)
            pt.setY(pt.y() + lt.boundingRect().height())

app = QApplication(sys.argv)
w = Widget()
w.setFont(QFont('Courier New', 10))
w.resize(480, 320)
w.show()
app.exec_()
