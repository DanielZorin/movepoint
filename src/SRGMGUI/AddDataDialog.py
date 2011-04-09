'''
Created on 09.04.2011

@author: juan
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, QColor, QInputDialog, QIntValidator, qApp


class AddDataDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self):
        # TODO: Qt Designer
        QDialog.__init__(self)
        self.label = QtGui.QLabel("Input data for a new error: ")
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.label1 = QtGui.QLabel("Time: ")
        self.input1 = QtGui.QSpinBox()
        self.input1.setValue(1)
        self.label2 = QtGui.QLabel("Programmer ID: ")
        self.input2 = QtGui.QSpinBox()
        self.input2.setValue(1)
        self.label3 = QtGui.QLabel("Severity: ")
        self.input3 = QtGui.QSpinBox()
        self.input3.setValue(1)
        self.label4 = QtGui.QLabel("Item: ")
        self.input4 = QtGui.QSpinBox()
        self.input4.setValue(1)
        self.accept = QtGui.QPushButton("OK")
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.input2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.input3)
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.input4)
        self.layout.addWidget(self.accept)
        self.setLayout(self.layout)
        QtCore.QObject.connect(self.accept, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
        
    def GetData(self):
        newError = {}
        newError["time"] = self.input1.value()
        newError["programmer"] = self.input2.value()
        newError["severity"] = self.input3.value()
        newError["item"] = self.input4.value() 
        return newError