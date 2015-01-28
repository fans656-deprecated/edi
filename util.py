from PySide.QtCore import QObject

class metaclass(QObject.__class__):

    def __init__(cls, name, bases, attrs):
        setattr(cls, 'super', lambda self: super(cls, self))
