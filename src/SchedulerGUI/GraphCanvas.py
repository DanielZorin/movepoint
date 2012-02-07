import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPointF
from PyQt4.QtGui import QWidget, QPainter, QPainterPath, QColor, QCursor, QDialog, QIntValidator, QTableWidgetItem
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import Version
from SchedulerGUI.Windows.ui_VertexDialog import Ui_VertexDialog
from SchedulerGUI.Windows.ui_EdgeDialog import Ui_EdgeDialog

class State:
    ''' Enum representing current editing mode '''
    Select = 0
    Vertex = 1
    Edge = 2

class VertexDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_VertexDialog()
        self.ui.setupUi(self)
        self.valid = QIntValidator(0, 1000000, self)
        self.ui.time.setValidator(self.valid)
        self.ui.versions.verticalHeader().hide()
        self.ui.versions.horizontalHeader().setStretchLastSection(True)

    def Load(self, v):
        self.ui.name.setText(v.name)
        self.ui.time.setText(str(v.time))
        for ver in v.versions:
            self.ui.versions.insertRow(0)
            item = QTableWidgetItem(str(ver.number))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            self.ui.versions.setItem(0, 0, item)
            self.ui.versions.setItem(0, 1, QTableWidgetItem(str(ver.reliability)))
        height = 0
        for i in range(self.ui.versions.rowCount()):
            height += self.ui.versions.rowHeight(i)
        # Dirty resizing to make the table visible
        self.resize(self.width(), self.height() + height - self.ui.versions.height())

    def AddVersion(self):
        self.ui.versions.insertRow(0)
        item = QTableWidgetItem(str(self.ui.versions.rowCount()))
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        self.ui.versions.setItem(0, 0, item)
        self.ui.versions.setItem(0, 1, QTableWidgetItem(str(1.0)))

    def RemoveVersion(self):
        self.ui.versions.removeRow(self.ui.versions.currentRow())

    def SetResult(self, v):
        v.name = self.ui.name.text()
        v.time = int(self.ui.time.text())
        v.versions = []
        for i in range(self.ui.versions.rowCount()):
            ver = Version(v, i + 1, float(self.ui.versions.item(i, 1).text()))
            v.versions.append(ver)
        v.versions.sort(key=lambda x: x.reliability)

class EdgeDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_EdgeDialog()
        self.ui.setupUi(self)
        self.valid = QIntValidator(0, 1000000, self)
        self.ui.volume.setValidator(self.valid)

    def Load(self, e):
        self.ui.name.setText(e.name)
        self.ui.volume.setText(str(e.volume))

    def SetResult(self, e):
        e.name = self.ui.name.text()
        e.volume = int(self.ui.volume.text())

class GraphCanvas(QWidget):
        
    colors = {
              "line": QColor(10, 34, 200),
              "vertex": QColor(123, 34, 100),
              "selected": QColor(1, 200, 1)
              }

    size = 15
    '''Size of the vertex rectangle'''

    program = None
    vertices = {}
    edges = {}
    selectedVertex = None
    pressed = False
    edgeDraw = False
    curEdge = None
    selectedEdge = None
    state = State.Select

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
    def paintEvent(self, event):
        if not self.program:
            return
        paint = QPainter(self)
        paint.setPen(self.colors["line"])
        paint.setFont(QtGui.QFont('Decorative', 10))
        for e in self.program.edges:
            if e != self.selectedEdge:
                self.drawArrow(paint, self.vertices[e.source].x() + self.size / 2, self.vertices[e.source].y() + self.size / 2,
                             self.vertices[e.destination].x() + self.size / 2, self.vertices[e.destination].y() + self.size / 2)
            else:
                paint.setPen(self.colors["selected"])
                paint.setBrush(self.colors["selected"])
                self.drawArrow(paint, self.vertices[e.source].x() + self.size / 2, self.vertices[e.source].y() + self.size / 2,
                             self.vertices[e.destination].x() + self.size / 2, self.vertices[e.destination].y() + self.size / 2)
                paint.setPen(self.colors["line"])
                paint.setBrush(self.colors["line"])

        paint.setPen(self.colors["vertex"])
        paint.setBrush(self.colors["vertex"])
        for task in self.vertices.values():
            if task == self.selectedVertex:
                paint.setPen(self.colors["selected"])
                paint.setBrush(self.colors["selected"])
                paint.drawEllipse(task)
                paint.setPen(self.colors["vertex"])
                paint.setBrush(self.colors["vertex"])
            else:
                paint.drawEllipse(task)

        paint.setPen(self.colors["line"])
        if self.edgeDraw:
            self.drawArrow(paint, self.curEdge[0].x() + self.size / 2, self.curEdge[0].y() + self.size / 2,
                           QCursor.pos().x() - self.mapToGlobal(self.geometry().topLeft()).x(),
                           QCursor.pos().y() - self.mapToGlobal(self.geometry().topLeft()).y())
        paint.end()

    def mousePressEvent(self, e):
        if self.state == State.Select:
            for v in self.vertices.keys():
                if self.vertices[v].contains(e.pos()):
                    self.selectedVertex = self.vertices[v]
                    self.selectedEdge = None
                    self.repaint()
                    self.pressed = True
                    return
            for ed in self.program.edges:
                a = self.vertices[ed.source].center()
                b = self.vertices[ed.destination].center()
                c = e.pos()
                ab = math.sqrt((a.x() - b.x())**2 + (a.y() - b.y())**2)
                inner = QtCore.QRect(a, b)
                if inner.contains(c):
                    bc = math.sqrt((c.x() - b.x())**2 + (c.y() - b.y())**2)
                    ac = math.sqrt((a.x() - c.x())**2 + (a.y() - c.y())**2)
                    p = (ab + bc + ac) / 2.0
                    area = math.sqrt(p * (p - ab) * (p - ac) * (p - bc))
                    print(ed, area)
                    if area < 100:
                        self.selectedEdge = ed
                        self.selectedVertex = None
                        self.repaint()
                        return
            self.selectedEdge = None
            self.selectedVertex = None
            self.repaint()
            return
        elif self.state == State.Vertex:
            task = QtCore.QRect(e.x() - self.size / 2, e.y() - self.size / 2, self.size, self.size)
            v = ProgramVertex(len(self.program.vertices), 1)
            ver = Version(v, 1, 1.0)
            v.versions = [ver]
            self.vertices[v] = task
            self.program.vertices.append(v)
            self.program._buildData()
            self.ResizeCanvas()
            self.repaint()
        elif self.state == State.Edge:
            for v in self.vertices.keys():
                if self.vertices[v].contains(e.pos()):
                    self.edgeDraw = True
                    self.curEdge = []
                    self.curEdge.append(self.vertices[v])
                    self.curEdge.append(v)
                    self.repaint()

    def mouseMoveEvent(self, e):
        if self.state == State.Vertex:
            return
        elif self.state == State.Select:
            if self.pressed:
                self.selectedVertex.moveTo(e.pos().x() - self.size / 2, e.pos().y() - self.size / 2)
                self.ResizeCanvas()
                self.repaint()
        elif self.state == State.Edge:
            if self.edgeDraw:
                self.repaint()

    def mouseReleaseEvent(self, e):
        self.pressed = False
        if self.edgeDraw:
            for v in self.vertices.keys():
                if self.vertices[v].contains(e.pos()):
                    ne = ProgramEdge(self.curEdge[1], v, 1)
                    self.program.edges.append(ne)
                    self.program._buildData()
            self.edgeDraw = False
            self.curEdge = None     
            self.repaint()

    def mouseDoubleClickEvent(self, e):
        if self.selectedVertex != None:
            v = next(v for v in self.vertices.keys() if self.vertices[v] == self.selectedVertex)
            self.EditVertex(v)
            self.repaint()
        elif self.selectedEdge != None:
            self.EditEdge(self.selectedEdge)
            self.repaint()

    def keyPressEvent(self, e):
        print(e.key())
        if e.key() == QtCore.Qt.Key_Delete:
            if self.selectedVertex != None:
                v = next(v for v in self.vertices.keys() if self.vertices[v] == self.selectedVertex)
                ind = self.program.vertices.index(v)
                new_edges = []
                for e in self.program.edges:
                    if e.source != v and e.destination != v:
                        new_edges.append(e)
                    else:
                        del e
                self.program.edges = new_edges
                del self.vertices[v]
                del self.program.vertices[ind]
                del self.selectedVertex
                self.selectedVertex = None
                self.program._buildData()
                self.repaint()
            elif self.selectedEdge != None:
                new_edges = []
                for e in self.program.edges:
                    if e != self.selectedEdge:
                        new_edges.append(e)
                    else:
                        del e
                self.program.edges = new_edges
                self.selectedEdge = None
                self.program._buildData()
                self.repaint()
        elif e.key() == QtCore.Qt.Key_Return:
            print ("Enter pressed")
            if self.selectedVertex != None:
                v = next(v for v in self.vertices.keys() if self.vertices[v] == self.selectedVertex)
                self.EditVertex(v)
                self.repaint()
            elif self.selectedEdge != None:
                self.EditEdge(self.selectedEdge)
                self.repaint()

    def EditEdge(self, e):
        d = EdgeDialog()
        d.Load(e)
        d.exec_()
        if d.result() == QDialog.Accepted:
            d.SetResult(e)

    def EditVertex(self, v):
        d = VertexDialog()
        d.Load(v)
        d.exec_()
        if d.result() == QDialog.Accepted:
            d.SetResult(v)

    def Visualize(self, p):
        self.program = p
        x = 50
        y = 50
        maxi = 40 * int(math.sqrt(len(self.program.vertices)))
        maxx = 0
        for v in self.program.vertices:
            task = QtCore.QRect(x - self.size / 2, y - self.size / 2, self.size, self.size)
            if x < maxi:
                x += 40
                maxx = x
            else:
                y += 40
                x = 50
            self.vertices[v] = task
        self.ResizeCanvas()
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

    def ResizeCanvas(self):
        maxx = 0
        maxy = 0
        for r in self.vertices.values():
            if r.topRight().x() > maxx:
                maxx = r.topRight().x()
            if r.bottomRight().y() > maxy:
                maxy = r.bottomRight().y()
        self.setGeometry(0, 0, max(maxx + 10, self.parent().width()), max(maxy + 10, self.parent().height()))

    def Clear(self):
        self.vertices = {}
        self.edges = {}
        self.selectedVertex = None
        self.pressed = False
        self.edgeDraw = False
        self.curEdge = None
        self.selectedEdge = None