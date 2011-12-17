'''
Created on 27.12.2010

@author: juan
'''
import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF
from PyQt4.QtGui import QWidget, QPainter, QPainterPath

class ScheduleVisualizer(QWidget):

    time = 50
    proc = 20
    scale = 1.5
    
    axisColor = None
    taskColor = None
    deliveriesColor = None
    lastopColor = None

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, (70 + self.time * 10)*self.scale, (40 + self.proc * 20)*self.scale )
        self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
        self.schedule = None
        self.operation = None
        
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setPen(self.axisColor)
        paint.setFont(QtGui.QFont('Decorative', 10*self.scale))
        if self.schedule == None:
            paint.drawText(10+10*self.scale, 10+10*self.scale, "Welcome to Scheduler GUI!")
            paint.drawText(10+20*self.scale, 10+20*self.scale, "Create or open a project before starting testing.")
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        else:
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
            paint.setPen(self.deliveriesColor)  
            for m in self.schedule.vertices.keys():
                for t in self.schedule.vertices[m]:
                    start = self.schedule.executionTimes[t][0]
                    finish = self.schedule.executionTimes[t][1]  
                    task = QtCore.QRect((50 + start * 10)*self.scale, (procX[t.m.number] - 5)*self.scale, (finish - start)*10*self.scale, 10*self.scale)
                    paint.fillRect(task, self.taskColor)    
                    paint.drawRect(task)    
                    taskRects[(t.v.number, t.k.number)] = task
                    queues[(t.m.number, t.n)] = task
                
            # Draw deliveries    
            for d in self.schedule.deliveryTimes:
                self.drawArrow(paint, (50 + d[2] * 10)*self.scale, procX[d[0].number]*self.scale, (50 + d[3] * 10)*self.scale, procX[d[1].number]*self.scale)
            
            if self.operation != None and self.operation["result"] == True:
                # Draw last operation
                paint.setPen(self.lastopColor)
                # TODO: visualize other operations
                if self.operation["operation"] == "MoveVertex":
                    rect = taskRects[(self.operation["parameters"][0], self.operation["parameters"][1])]
                    paint.fillRect(rect, QtGui.QColor(255, 0, 0))
                    if self.operation["parameters"][2] == -1:
                        targetY = (40 + self.proc * 20)*self.scale
                        targetX = 50
                    else:
                        targetY = procX[self.operation["parameters"][2]] * self.scale
                        if queues.__contains__((self.operation["parameters"][2], self.operation["parameters"][3])):
                            targetX = queues[(self.operation["parameters"][2], self.operation["parameters"][3])].x()
                        else:
                            # This happens if the task is moved to the last position
                            # This needs a HUGE refactoring
                            # TODO: there's a bug here, can't make it reproduce though
                            r = queues[(self.operation["parameters"][2], self.operation["parameters"][3]-1)]
                            targetX = r.x() + r.width()
                    self.drawArrow(paint, rect.center().x(), rect.center().y(), targetX, targetY)
            
            # Draw captions
            paint.setPen(self.axisColor)    
            for m in self.schedule.vertices.keys():
                for t in self.schedule.vertices[m]:
                    start = self.schedule.executionTimes[t][0]
                    finish = self.schedule.executionTimes[t][1]   
                    s = str(t.v.number) + " v" + str(t.k.number)
                    paint.drawText((10 + finish + start - int(len(s)/2))*5*self.scale, (procX[t.m.number]+5)*self.scale, s) 
                   
        paint.end()
        
    
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
        p1 = QPointF(math.sqrt((x2-x1)**2 + (y2-y1)**2) , 0)
        paint.drawLine(0, 0, p1.x(), 0)
        
        p2 = QPointF(math.sqrt((x2-x1)**2 + (y2-y1)**2) - 5, 5)
        p3 = QPointF(math.sqrt((x2-x1)**2 + (y2-y1)**2) - 5, -5)
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
            
    def Visualize(self, s, op=None):
        self.schedule = s
        self.operation = op
        self.proc = self.schedule.GetProcessorsWithoutDoubles()
        self.time = self.schedule.Interpret()
        self.repaint()
        self.setGeometry(0, 0, int((70 + self.time * 10)*self.scale), int((40 + self.proc * 20)*self.scale) )
        
    def SetColors(self, a, t, d, l):
        self.axisColor = a
        self.taskColor = t
        self.deliveriesColor = d
        self.lastopColor = l