import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF
from PyQt4.QtGui import QWidget, QPainter, QPainterPath, QPen, QColor, QScrollArea

class State:
    ''' Enum representing current editing mode '''
    Select = 0
    Vertex = 1
    Edge = 2

class GraphCanvas(QScrollArea):
        
    axisColor = None
    taskColor = None
    deliveriesColor = None
    lastopColor = None

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, 3000, 3000)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.program = None
        self.rects = []
        self.state = State.Select
        
    def paintEvent(self, event):
        paint = QPainter(self.viewport())
        paint.begin(self)
        paint.setPen(QColor(123, 34, 100))
        paint.setFont(QtGui.QFont('Decorative', 10*self.scale))
        for task in self.rects:
            paint.fillRect(task, QColor(123, 34, 100))
        paint.end()

    def mousePressEvent(self, e):
        if self.state == State.Vertex:
            task = QtCore.QRect(e.x() - 5, e.y() - 5, 10, 10)
            self.rects.append(task)
            self.repaint()

    def Visualize(self, p):
        self.program = p
        self.repaint()
        
    def SetColors(self, a, t, d, l):
        self.axisColor = a
        self.taskColor = t
        self.deliveriesColor = d
        self.lastopColor = l