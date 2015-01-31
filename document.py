class Document(object):

    def __init__(self):
        self.lines = [u'']
        self.iLine = 0
        self.iCol = 0

    @property
    def text(self):
        return '\n'.join(self.lines)

    @text.setter
    def text(self, text):
        self.lines = text.split('\n')

    def put(self, o):
        if type(o) == str:
            self.putRawString(o)

    def putRawString(self, rawS):
        for s in rawS.split('\n'):
            self.putString(s)
            self.newLine()

    def putChar(self, ch):
        self.putString(ch)

    def putString(self, s):
        i = self.iCol
        line = self.lines[self.iLine]
        line = line[:i] + s + line[i:]
        self.lines[self.iLine] = line
        self.iCol += len(s)
        self.controller.notify({
            'type': 'linechange',
            'indexes': [self.iLine]
            })

    def newLine(self):
        line = self.line()
        a, b = self.lineParts()
        self.line(a)
        self.iLine += 1
        self.lines.insert(self.iLine, b)
        self.adjustCursorInLine()

        if len(b):
            self.controller.notify({
                'type': 'linechange',
                'indexes': [self.iLine - 1]
                })
        self.controller.notify({
            'type': 'newline',
            'index': self.iLine
            })

    def delBack(self, what='char'):
        if what == 'char':
            if self.iCol == 0:
                if self.iLine > 0:
                    self.iLine -= 1
                    self.iCol = len(self.line())
                    self.joinLines(self.iLine, 2)
            else:
                a, b = self.lineParts()
                self.line(a[:-1] + b)
                self.iCol -= 1
                self.controller.notify({
                    'type': 'linechange',
                    'indexes': [self.iLine]
                    })

    def joinLines(self, beg, n):
        if beg >= 0:
            self.lines[beg] = ''.join(self.lines[beg:beg + n])
            del self.lines[beg + 1:beg + n]
            self.controller.notify({
                'type': 'linechange',
                'indexes': [self.iLine]
                })
            self.controller.notify({
                'type': 'delline',
                'indexes': [beg + i for i in range(1, n)]
                })

    def delForward(self, what):
        if what == 'char':
            pass

    def line(self, newLine=None):
        if newLine is not None:
            self.lines[self.iLine] = newLine
        return self.lines[self.iLine]

    def lineParts(self):
        line = self.line()
        return line[:self.iCol], line[self.iCol:]

    def cursorUp(self):
        if self.iLine > 0:
            self.iLine -= 1
            self.adjustCursorInLine()
            self.notifyCursorChange()

    def cursorDown(self):
        if self.iLine + 1 < len(self.lines):
            self.iLine += 1
            self.adjustCursorInLine()
            self.notifyCursorChange()

    def cursorLeft(self):
        if self.iCol == 0:
            if self.iLine > 0:
                self.iLine -= 1
                self.iCol = len(self.line())
                self.notifyCursorChange()
        else:
            self.iCol -= 1
            self.notifyCursorChange()

    def cursorRight(self):
        lenLine = len(self.line())
        if self.iCol == lenLine:
            if self.iLine < len(self.lines):
                self.iLine += 1
                self.iCol = 0
                self.notifyCursorChange()
        else:
            self.iCol += 1
            self.notifyCursorChange()

    def notifyCursorChange(self):
        self.controller.notify({
            'type': 'cursorchange'
            })

    def adjustCursorInLine(self):
        lenLine = len(self.line())
        if self.iCol > lenLine:
            self.iCol = lenLine
