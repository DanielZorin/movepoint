'''
Created on 27.12.2010

@author: juan
'''
import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, SIGNAL, QRect
from PyQt4.QtGui import QWidget, QPainter, QPainterPath, QPen, QImage

class ScheduleVisualizer(QWidget):

    time = 50
    proc = 20
    scale = 1.5
    
    schedule = None
    method = None
    vertices = {}
    positions = {}

    axisColor = None
    taskColor = None
    deliveriesColor = None
    lastopColor = None

    selectedTask = None
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
        self.delicon = QImage(_fromUtf8(":/pics/pics/delete.png"))
        
    def paintEvent(self, event):        
        if self.schedule:
            paint = QPainter()
            paint.begin(self)
            paint.setPen(self.axisColor)
            paint.setFont(QtGui.QFont('Decorative', 9*self.scale))
            procX = {}

            # Draw processor names and axis
            for i in range(self.proc):
                paint.drawImage(QRect(10*self.scale, (10 + i * 20)*self.scale, 24*self.scale, 24*self.scale), self.procicon)  
                paint.drawText(35*self.scale, (25 + i * 20)*self.scale, str(self.schedule.processors[i].reserves))
                paint.drawLine(50*self.scale, (20 + i * 20)*self.scale, (50 + self.time * 10)*self.scale, (20 + i * 20)*self.scale)
                procX[self.schedule.processors[i].number] = 20 + i * 20
            
            # Draw tasks
            paint.setPen(self.taskColor)  
            self.vertices = {}
            self.positions = {}
            for m in self.schedule.vertices.keys():
                i = 0
                prev = None
                for t in self.schedule.vertices[m]:
                    start = self.schedule.executionTimes[t][0]
                    finish = self.schedule.executionTimes[t][1]
                    task = QtCore.QRect((50 + start * 10)*self.scale, (procX[t.m.number] - 5)*self.scale, (finish - start)*10*self.scale, 10*self.scale)
                    # TODO: calculate once!
                    self.vertices[t] = task
                    if i == 0:
                        self.positions[(m, i)] = QtCore.QRect(QPoint(50*self.scale, task.y()), task.bottomLeft())
                    else:
                        self.positions[(m, i)] = QtCore.QRect(prev.topRight(), task.bottomLeft())
                    if t != self.selectedTask:
                        paint.fillRect(task, self.taskColor)
                    else:
                        paint.fillRect(task, self.lastopColor)
                        if self.schedule.CanAddVersions(t):
                            paint.drawImage(QRect(task.topLeft().x(), task.topLeft().y(), 
                                                  10*self.scale, 10*self.scale), self.addicon)              
                        if self.schedule.CanDeleteVersions(t):
                            paint.drawImage(QRect(task.topRight().x() - 10*self.scale, task.topRight().y(), 
                                                  10*self.scale, 10*self.scale), self.delicon) 
                    paint.setPen(self.axisColor)
                    paint.drawRect(task)
                    paint.setPen(self.taskColor)
                    prev = task
                    i += 1 
                self.positions[(m, i)] = QtCore.QRect(prev.topRight(), QPoint(prev.topRight().x() + 100, prev.bottomRight().y()))
            
            if self.targetPos:
                width = min(self.selectedTask.v.time * 10 * self.scale, self.positions[self.targetPos].width())
                rect = QtCore.QRect(self.positions[self.targetPos])
                rect.setWidth(width)
                paint.fillRect(rect, self.lastopColor)
                    
            # Draw deliveries   
            paint.setPen(QPen(self.deliveriesColor, 2)) 
            for d in self.schedule.deliveryTimes:
                self.drawArrow(paint, (50 + d[2] * 10)*self.scale, procX[d[0].number]*self.scale, (50 + d[3] * 10)*self.scale, procX[d[1].number]*self.scale)
            
            # Draw captions
            paint.setPen(self.axisColor)    
            for m in self.schedule.vertices.keys():
                for t in self.schedule.vertices[m]:
                    start = self.schedule.executionTimes[t][0]
                    finish = self.schedule.executionTimes[t][1]   
                    s = str(t.v.number)
                    if t.k.number > 1:
                       s += " v" + str(t.k.number)
                    paint.drawText((10 + finish + start - int(len(s)/2))*5*self.scale, (procX[t.m.number]+5)*self.scale, s)
                   
            paint.end()
 
    def mousePressEvent(self, e):
        for v in self.vertices.keys():
            if self.vertices[v].contains(e.pos()):
                self.selectedTask = v
                self.repaint()
                self.pressed = True
                return
        self.selectedTask = None
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
            if result:
                self.proc = self.schedule.GetProcessorsWithoutDoubles()
                self.time = self.schedule.Interpret()
                self.emit(SIGNAL("ManualOperation"))
            self.targetPos = None
            self.pressed = False
            self.selectedTask = None
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
        self.time = self.schedule.Interpret()
        self.ResizeCanvas()
        self.repaint()
        
    def SetColors(self, a, t, d, l):
        self.axisColor = a
        self.taskColor = t
        self.deliveriesColor = d
        self.lastopColor = l

    def ResizeCanvas(self):
        self.setGeometry(0, 0, max(int((70 + self.time * 10)*self.scale), self.parent().width()), 
                         max(int((40 + self.proc * 20)*self.scale), self.parent().height()))