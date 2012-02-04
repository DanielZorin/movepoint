'''
Created on 27.12.2010

@author: juan
'''
import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF
from PyQt4.QtGui import QWidget, QPainter, QPainterPath, QPen, QScrollArea

class ScheduleVisualizer(QScrollArea):

    time = 50
    proc = 20
    scale = 1.5
    
    axisColor = None
    taskColor = None
    deliveriesColor = None
    lastopColor = None

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, (70 + self.time * 10)*self.scale, (40 + self.proc * 20)*self.scale)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.schedule = None
        self.vertices = {}
        
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self.viewport())
        paint.setPen(self.axisColor)
        paint.setFont(QtGui.QFont('Decorative', 10*self.scale))
        if self.schedule != None:
            procX = {}
            taskRects = {}
            queues = {}
            #print("=================", self.proc, len(self.schedule.processors))
            # Draw processor names and axis
            for i in range(self.proc):  
                paint.drawText(10*self.scale, (20 + i * 20)*self.scale, str(self.schedule.processors[i].number) + " X " + str(self.schedule.processors[i].reserves))
                paint.drawLine(50*self.scale, (20 + i * 20)*self.scale, (50 + self.time * 10)*self.scale, (20 + i * 20)*self.scale)
                procX[self.schedule.processors[i].number] = 20 + i * 20
            
            # Draw tasks
            paint.setPen(self.taskColor)  
            for m in self.schedule.vertices.keys():
                for t in self.schedule.vertices[m]:
                    start = self.schedule.executionTimes[t][0]
                    finish = self.schedule.executionTimes[t][1]
                    task = QtCore.QRect((50 + start * 10)*self.scale, (procX[t.m.number] - 5)*self.scale, (finish - start)*10*self.scale, 10*self.scale)
                    self.vertices[t] = task
                    paint.fillRect(task, self.taskColor)    
                    paint.drawRect(task)
                    taskRects[(t.v.number, t.k.number)] = task
                    queues[(t.m.number, t.n)] = task
                
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
                    s = str(t.v.number) + " v" + str(t.k.number)
                    paint.drawText((10 + finish + start - int(len(s)/2))*5*self.scale, (procX[t.m.number]+5)*self.scale, s) 
                   
        paint.end()
 
    def mousePressEvent(self, e):
        for v in self.vertices.keys():
            if self.vertices[v].contains(e.pos()):
                self.selectedVertex = self.vertices[v]
                self.selectedEdge = None
                self.repaint()
                self.pressed = True
                return
        self.selectedEdge = None
        self.selectedVertex = None
        self.repaint()

    def mouseMoveEvent(self, e):
        if self.pressed:
            self.selectedVertex.moveTo(e.pos().x() - self.size / 2, e.pos().y() - self.size / 2)
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
        self.repaint()
        self.setGeometry(0, 0, int((70 + self.time * 10)*self.scale), int((40 + self.proc * 20)*self.scale) )        
            
    def Visualize(self, s):
        self.schedule = s
        self.proc = self.schedule.GetProcessorsWithoutDoubles()
        self.time = self.schedule.Interpret()
        self.repaint()
        self.setGeometry(0, 0, int((70 + self.time * 10)*self.scale), int((40 + self.proc * 20)*self.scale) )
        
    def SetColors(self, a, t, d, l):
        self.axisColor = a
        self.taskColor = t
        self.deliveriesColor = d
        self.lastopColor = l