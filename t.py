# coding: utf-8
import sys
import string

from PySide.QtCore import *
from PySide.QtGui import *

import util

class Widget(QDialog):

    __metaclass__ = util.metaclass

    def __init__(self, parent=None):
        self.super().__init__(parent)
        self.text = u''
        self.layouts = []

    def keyPressEvent(self, ev):
        ch = ev.text()
        key = ev.key()
        # \r 属于 string.printable ，所以要优先判断
        if ch and ch in '\r\n':
            self.text += '\n'
        elif key == Qt.Key_Backspace:
            self.text = self.text[:-1]
        elif ch and ch in string.printable:
            self.text += ch
        self.update()

    def layout(self):
        lines = self.text.split('\n')
        self.layouts = []
        for line in lines:
            self.layoutLine(line)

    def layoutLine(self, line):
        fm = self.fontMetrics()
        self.fm = fm
        leading = fm.leading()
        y = 0.0
        lt = QTextLayout(line)
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
        for lt in self.layouts:
            lt.draw(painter, pt)
            pt.setY(pt.y() + lt.boundingRect().height())
            print pt, lt.position()
        print '*' * 40

app = QApplication(sys.argv)
w = Widget()
w.setFont(QFont('Arial', 50))
w.resize(480, 320)
w.show()
app.exec_()
