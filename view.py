from PySide.QtCore import *
from PySide.QtGui import *

class View(object):

    def __init__(self):
        self.layouts = []
        self._font = None

        self._document = None
        self.isCursorVisible = True
        self._halfCursorBlinkingTime = 500
        self._position = QPoint(0, 0)
        self._size = QSize(0, 0)

        self.cursorTimer = QTimer()
        self.cursorTimer.timeout.connect(self.cursorTimeout)
        self.cursorTimer.setInterval(500)
        self.cursorTimer.start()

    def cursorTimeout(self):
        pass

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        self.fm = QFontMetrics(font)

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document):
        self._document = document
        self.createLayouts()

    @property
    def cursorBlinkingTime(self):
        '''Cursor blinking time in milliseconds, visible time + invisible time'''
        return self._halfCursorBlinkingTime * 2

    @cursorBlinkingTime.setter
    def cursorBlinkingTime(self, milliseconds):
        # cursor visible time == unvisible time == halfCursorBlinkingTime
        self._halfCursorBlinkingTime = milliseconds / 2.0

    @property
    def position(self):
        '''Top left point of this viewer, QPoint'''
        return self._position

    @position.setter
    def position(self, pt):
        self._position = pt
        self.layout()

    @property
    def size(self):
        '''Width and height of this viewer, QSize'''
        return self._size

    @size.setter
    def size(self, newSize):
        self._size = newSize

    def draw(self, painter):
        x = self.position.x()
        y = self.position.y()
        for layout in self.layouts:
            layout.draw(painter, QPointF(x, y))
            y += layout.boundingRect().height()

    def layout(self, iLine=None):
        pass

    def createLayouts(self):
        doc = self.document
        width = self.size.width()
        for line in doc.lines:
            layout = QTextLayout(line, self.font)
            layout.setPosition(self.position)
            self.createLines(layout, width)
            self.layouts.append(layout)

    def createLines(self, layout, width):
        leading = self.fm.leading()
        height = self.fm.height()
        y = 0.0
        layout.beginLayout()
        while True:
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(width)
            y += leading
            line.setPosition(QPointF(0, y))
            y += height
        layout.endLayout()
