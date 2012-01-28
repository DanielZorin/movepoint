import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF
from PyQt4.QtGui import QWidget, QPainter, QPainterPath, QPen, QColor, QScrollArea
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import Version

class State:
    ''' Enum representing current editing mode '''
    Select = 0
    Vertex = 1
    Edge = 2

class GraphCanvas(QScrollArea):
        
    colors = {
              "line": QColor(10, 34, 200),
              "vertex": QColor(123, 34, 100),
              "selected": QColor(1, 200, 1)
              }

    size = 15
    '''Size of the vertex rectangle'''

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, 3000, 3000)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.program = None
        self.vertices = {}
        self.edges = {}
        self.current = None
        self.pressed = False
        self.state = State.Select
        
    def paintEvent(self, event):
        if not self.program:
            return
        paint = QPainter(self.viewport())
        paint.setPen(self.colors["line"])
        paint.setFont(QtGui.QFont('Decorative', 10))
        for e in self.program.edges:
            self.drawArrow(paint, self.vertices[e.source].x() + self.size / 2, self.vertices[e.source].y() + self.size / 2,
                             self.vertices[e.destination].x() + self.size / 2, self.vertices[e.destination].y() + self.size / 2)

        paint.setPen(self.colors["vertex"])
        paint.setBrush(self.colors["vertex"])
        for task in self.vertices.values():
            if task == self.current:
                paint.setPen(self.colors["selected"])
                paint.setBrush(self.colors["selected"])
                paint.drawEllipse(task)
                paint.setPen(self.colors["vertex"])
                paint.setBrush(self.colors["vertex"])
            else:
                paint.drawEllipse(task)
        paint.end()

    def mousePressEvent(self, e):
        if self.state == State.Select:
            for v in self.vertices.keys():
                if self.vertices[v].contains(e.pos()):
                    self.current = self.vertices[v]
                    self.repaint()
                    self.pressed = True
                    return
            self.current = None
            self.repaint()
            return
        elif self.state == State.Vertex:
            task = QtCore.QRect(e.x() - self.size / 2, e.y() - self.size / 2, self.size, self.size)
            v = ProgramVertex(len(self.program.vertices), 1)
            ver = Version(v, 1, 1.0)
            task.versions = [ver]
            self.vertices[v] = task
            self.program.vertices.append(v)
            self.repaint()

    def mouseMoveEvent(self, e):
        if self.state != State.Select or not self.pressed:
            return
        self.current.moveTo(e.pos().x() - self.size / 2, e.pos().y() - self.size / 2)
        self.repaint()

    def mouseReleaseEvent(self, e):
        self.pressed = False

    def Visualize(self, p):
        self.program = p
        x = 50
        y = 50
        max = 40 * int(math.sqrt(len(self.program.vertices)))
        for v in self.program.vertices:
            task = QtCore.QRect(x - self.size / 2, y - self.size / 2, self.size, self.size)
            if x < max:
                x += 40
            else:
                y += 40
                x = 50
            self.vertices[v] = task
        self.repaint()
 
    def drawArrow(self, paint, x1, y1, x2, y2):
        m = paint.worldMatrix()
        paint.translate(x1,y1)
        pi = 3.1415926
        if abs(x2 - x1) > 0:
            alpha = math.atan(abs(y2-y1)/abs(x2-x1)) * 180 / pi
        else:
            alpha = 90
        if y2 > y1:
            if x2 > x1:
                paint.rotate(alpha)
            else:
                paint.rotate(180-alpha)
        else:
            if x2 > x1:
                paint.rotate(-alpha)
            else:
                paint.rotate(alpha-180)
        endcoord = math.sqrt((x2-x1)**2 + (y2-y1)**2) - self.size / 2
        p1 = QPointF(endcoord , 0)
        paint.drawLine(0, 0, p1.x(), 0)
        
        coord = math.sqrt(9**2 - 6**2)
        p2 = QPointF(endcoord - coord, 6)
        p3 = QPointF(endcoord - coord, -6)
        path = QPainterPath()
        path.moveTo(p1)
        path.lineTo(p2)
        path.lineTo(p3)
        path.lineTo(p1)
        paint.fillPath(path, paint.pen().color())
        paint.setWorldMatrix(m)
               
    def SetColors(self, a, t, d, l):
        self.axisColor = a
        self.taskColor = t
        self.deliveriesColor = d
        self.lastopColor = l