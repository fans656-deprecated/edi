class Controller(object):

    def __init__(self):
        self._document = None
        self.views = []

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document):
        self._document = document
        for view in self.views:
            view.document = document

    def add(self, view):
        if self.document:
            self.view.document = document
        self.views.append(view)

    def notify(self, ev):
        print ev

    def draw(self, painter):
        for view in self.views:
            view.draw(painter)
