'''
Created on 06.04.2011

@author: juan
'''
from PyQt4 import QtGui, QtCore

class Graph(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(440, 90, 300, 300)
        self.func = self.meanFunc = self.intensity = lambda x: 0
        self.time = self.number = 5

    def Change(self, k):
        if k == 1:
            self.func = self.meanFunc
        else:
            self.func = self.intensity

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setPen(QtGui.QColor(168, 34, 3))
        paint.setFont(QtGui.QFont('Decorative', 10))
        if self.func == self.meanFunc:
            x0, y0 = 0, self.height()
            ki = 300.0/(self.time+1)
            kj = 300.0/(self.number+1.5)
            for i in range(1, self.width()):
                x1, y1 = i, int(self.func(i/ki)*kj)
                y1 = 300 - y1
                paint.drawLine(x0, y0, x1, y1)
                x0, y0 = x1, y1
        else:
            if self.func(0) - 0.0 < 0.01:
                x0, y0 = 1, 1
                ki = 300.0/(self.time+1)
                kj = 300.0/(1.3)                
            else:
                x0, y0 = 1, self.func(0)
                ki = 300.0/(self.time+1)
                kj = 300.0/(self.func(0)*1.3)
            for i in range(1, self.width()):
                x1, y1 = i, int(self.func(i/ki)*kj)
                y1 = 300 - y1
                paint.drawLine(x0, y0, x1, y1)
                x0, y0 = x1, y1            
        paint.end()