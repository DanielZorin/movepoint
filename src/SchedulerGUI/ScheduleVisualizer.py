'''
Created on 27.12.2010

@author: juan
'''
import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, SIGNAL, QRect
from PyQt4.QtGui import QWidget, QPainter, QPainterPath, QPen, QImage, QColor

class ScheduleVisualizer(QWidget):

    time = 50
    proc = 20
    scale = 1.5
    
    schedule = None
    method = None
    vertices = {}
    positions = {}
    procrects = {}

    colors = {
              "axis": QColor(168, 34, 3),
              "task": QColor(168, 134, 50),
              "delivery": QColor(100, 0, 255),
              "select": QColor(255, 0, 0)
              }    

    selectedTask = None
    addrect = None
    delrect = None
    targetPos = None
    pressed = False

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, (70 + self.time * 10)*self.scale, (40 + self.proc * 20)*self.scale)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        try:
            _fromUtf8 = QtCore.QString.fromUtf8
        except AttributeError:
            _fromUtf8 = lambda s: s
        self.procicon = QImage(_fromUtf8(":/pics/pics/processor.png"))
        self.addicon = QImage(_fromUtf8(":/pics/pics/add.png"))
        self.delicon = QImage(_fromUtf8(":/pics/pics/meenoos.png"))
        
    def paintEvent(self, event):        
        if self.schedule:
            paint = QPainter()
            paint.begin(self)
            paint.setPen(self.colors["axis"])
            paint.setFont(QtGui.QFont('Decorative', 9*self.scale))
            procX = {}

            # Draw processor names and axis
            for i in range(self.proc):
                paint.drawImage(QRect(15*self.scale, (10 + i * 20)*self.scale, 24*self.scale, 24*self.scale), self.procicon)  
                paint.drawText(40*self.scale, (25 + i * 20)*self.scale, str(self.schedule.processors[i].reserves))
                plus = QRect(5*self.scale, (10 + i * 20)*self.scale, 10*self.scale, 10*self.scale)
                paint.drawImage(plus, self.addicon) 
                meenoos = QRect(5*self.scale, (20 + i * 20)*self.scale, 10*self.scale, 10*self.scale)
                paint.drawImage(meenoos, self.delicon)
                self.procrects[self.schedule.processors[i]] = [plus, meenoos]
                paint.drawLine(50*self.scale, (20 + i * 20)*self.scale, (50 + self.time * 10)*self.scale, (20 + i * 20)*self.scale)
                procX[self.schedule.processors[i].number] = 20 + i * 20

            # Draw timeline
            tdir = self.method.system.tdir
            paint.drawLine(50*self.scale, self.height() - 15, (50 + tdir * 10)*self.scale, self.height() - 15)
            paint.drawLine(50*self.scale, 10 * self.scale, 50*self.scale, self.height() - 10)
            t = 0
            paint.setFont(QtGui.QFont('Decorative', 8))
            while t < tdir + 10:
                paint.drawLine((50 + t * 10)*self.scale, self.height() - 20, (50 + t * 10)*self.scale, self.height() - 10)
                paint.drawText((50 + t * 10 + 1)*self.scale, self.height() - 5, str(t))
                t += 10

            paint.setPen(self.colors["select"]) 
            paint.drawLine((50 + tdir * 10)*self.scale, 10 * self.scale, (50 + tdir * 10)*self.scale, self.height() - 10)
            if self.selectedTask:
                t = self.selectedTask
                start = self.method.interpreter.executionTimes[t][0]
                finish = self.method.interpreter.executionTimes[t][1]
                paint.drawText((50 + start * 10)*self.scale, self.height() - 16, str(start))
                paint.drawText((50 + finish * 10)*self.scale, self.height() - 16, str(finish))

            # Draw tasks
            paint.setPen(self.colors["task"])  
            paint.setFont(QtGui.QFont('Decorative', 9*self.scale))
            self.vertices = {}
            self.positions = {}
            for m in self.schedule.vertices.keys():
                i = 0
                prev = None
                for t in self.schedule.vertices[m]:
                    start = self.method.interpreter.executionTimes[t][0]
                    finish = self.method.interpreter.executionTimes[t][1]
                    task = QtCore.QRect((50 + start * 10)*self.scale, (procX[t.m.number] - 5)*self.scale, (finish - start)*10*self.scale, 10*self.scale)
                    # TODO: calculate once!
                    self.vertices[t] = task
                    if i == 0:
                        self.positions[(m, i)] = QtCore.QRect(QPoint(50*self.scale, task.y()), task.bottomLeft())
                    else:
                        self.positions[(m, i)] = QtCore.QRect(prev.topRight(), task.bottomLeft())
                    if t != self.selectedTask:
                        paint.fillRect(task, self.colors["task"])
                    else:
                        paint.fillRect(task, self.colors["select"])
                        if self.schedule.CanAddVersions(t):
                            self.addrect = QRect(task.topLeft().x(), task.topLeft().y(), 
                                                  10*self.scale, 10*self.scale)
                            paint.drawImage(self.addrect, self.addicon)              
                        if self.schedule.CanDeleteVersions(t):
                            self.delrect = QRect(task.topRight().x() - 10*self.scale, task.topRight().y(), 
                                                  10*self.scale, 10*self.scale)
                            paint.drawImage(self.delrect, self.delicon)
                    paint.setPen(self.colors["axis"])
                    paint.drawRect(task)
                    paint.setPen(self.colors["task"])
                    prev = task
                    i += 1 
                self.positions[(m, i)] = QtCore.QRect(prev.topRight(), QPoint(prev.topRight().x() + 100, prev.bottomRight().y()))
            
            if self.targetPos:
                width = min(self.selectedTask.v.time * 10 * self.scale, self.positions[self.targetPos].width())
                rect = QtCore.QRect(self.positions[self.targetPos])
                rect.setWidth(width)
                paint.fillRect(rect, self.colors["select"])
                    
            # Draw deliveries   
            paint.setPen(QPen(self.colors["delivery"], 2)) 
            for d in self.method.interpreter.deliveryTimes:
                self.drawArrow(paint, (50 + d[2] * 10)*self.scale, procX[d[0].number]*self.scale, (50 + d[3] * 10)*self.scale, procX[d[1].number]*self.scale)
            
            # Draw captions
            paint.setPen(self.colors["axis"])    
            for m in self.schedule.vertices.keys():
                for t in self.schedule.vertices[m]:
                    start = self.method.interpreter.executionTimes[t][0]
                    finish = self.method.interpreter.executionTimes[t][1]   
                    s = str(t.v.number)
                    if t.k.number > 1:
                       s += " v" + str(t.k.number)
                    paint.drawText((10 + finish + start - int(len(s)/2))*5*self.scale, (procX[t.m.number]+5)*self.scale, s)
                   
            paint.end()
 
    def mousePressEvent(self, e):
        def update():
            self.proc = self.schedule.GetProcessorsWithoutDoubles()
            self.time = self.schedule.Interpret()
            self.targetPos = None
            self.pressed = False
            self.selectedTask = None
            self.addrect = None
            self.delrect = None
            self.emit(SIGNAL("ManualOperation"))
            self.ResizeCanvas()
            self.repaint()
            return

        if self.selectedTask:
            if self.addrect:
                if self.addrect.contains(e.pos()):
                    self.method.ManualStep("AddVersion", v = self.selectedTask.v)
                    update()
                    return
            if self.delrect:
                if self.delrect.contains(e.pos()):
                    self.method.ManualStep("DeleteVersion", v = self.selectedTask.v)
                    update()
                    return

        for p in self.procrects.keys():
            if self.procrects[p][0].contains(e.pos()):
                self.method.ManualStep("AddProcessor", m = p)
                update()
                return
            if self.procrects[p][1].contains(e.pos()):
                self.method.ManualStep("DeleteProcessor", m = p)
                update()
                return

        for v in self.vertices.keys():
            if self.vertices[v].contains(e.pos()):
                self.selectedTask = v
                self.repaint()
                self.pressed = True
                return
        self.selectedTask = None
        self.addrect = None
        self.delrect = None
        self.repaint()

    def mouseMoveEvent(self, e):
        if self.pressed:
            for p in self.positions.keys():
                if self.positions[p].contains(e.pos()):
                    self.targetPos = p
                    self.repaint()
                    return
            self.targetPos = None
            self.repaint()

    def mouseReleaseEvent(self, e):
        if self.pressed and self.targetPos:
            result = self.method.ManualStep("MoveVertex", 
                                   v = self.selectedTask, 
                                   n1 = self.schedule.vertices[self.selectedTask.m].index(self.selectedTask), 
                                   m2 = self.schedule.GetProcessor(self.targetPos[0]), 
                                   n2 = self.targetPos[1])
            if result == True:
                self.proc = self.schedule.GetProcessorsWithoutDoubles()
                self.time = self.method.interpreter.Interpret(self.schedule)
                self.emit(SIGNAL("ManualOperation"))
            else:
                self.emit(SIGNAL("WrongOperation"), result)
            self.targetPos = None
            self.pressed = False
            self.selectedTask = None
            self.addrect = None
            self.delrect = None
            self.ResizeCanvas()
            self.repaint()
            return
        self.pressed = False
        self.targetPos = None
        self.repaint()
    
    def drawArrow(self, paint, x1, y1, x2, y2):
        m = paint.worldMatrix()
        paint.translate(x1,y1)
        pi = 3.1415926
        alpha = math.atan(abs(y2-y1)/abs(x2-x1)) * 180 / pi
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
        endcoord = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        p1 = QPointF(endcoord , 0)
        paint.drawLine(0, 0, p1.x(), 0)
        
        coord = math.sqrt(12**2 - 6**2)
        p2 = QPointF(endcoord - coord, 6)
        p3 = QPointF(endcoord - coord, -6)
        path = QPainterPath()
        path.moveTo(p1)
        path.lineTo(p2)
        path.lineTo(p3)
        path.lineTo(p1)
        paint.fillPath(path, paint.pen().color())
        paint.setWorldMatrix(m)
        
    def SetScale(self, d):
        self.scale = d
        self.ResizeCanvas()
        self.repaint()      
            
    def Visualize(self, m):
        self.schedule = m.system.schedule
        self.method = m
        # TODO: get rid of this
        self.proc = self.schedule.GetProcessorsWithoutDoubles()
        self.time = self.method.interpreter.Interpret(self.schedule)
        self.ResizeCanvas()
        self.repaint()

    def ResizeCanvas(self):
        self.setGeometry(0, 0, max(int((70 + self.time * 10)*self.scale), self.parent().width()), 
                         max(int((40 + self.proc * 20)*self.scale), self.parent().height()))