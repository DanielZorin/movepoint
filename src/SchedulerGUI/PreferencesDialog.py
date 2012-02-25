'''
Created on 06.01.2011

@author: juan
'''

from PyQt4.QtGui import QDialog, QColorDialog
from SchedulerGUI.Windows.ui_PreferencesDialog import Ui_PreferencesDialog
     
class PreferencesDialog(QDialog):
    
    graphEditor = {}
    viewer = {}
    
    def __init__(self, vi, ge):
        QDialog.__init__(self)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.graphEditor = ge
        self.viewer = vi
        self.ui.axis.setStyleSheet("background-color: " + self.viewer["axis"].name())
        self.ui.tasks.setStyleSheet("background-color: " + self.viewer["task"].name())
        self.ui.deliveries.setStyleSheet("background-color: " + self.viewer["delivery"].name())
        self.ui.lastop.setStyleSheet("background-color: " + self.viewer["select"].name())  
        self.ui.vertex.setStyleSheet("background-color: " + self.graphEditor["vertex"].name())
        self.ui.edge.setStyleSheet("background-color: " + self.graphEditor["line"].name())
        self.ui.selection.setStyleSheet("background-color: " + self.graphEditor["selected"].name()) 
                
    def AxisColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.axis.setStyleSheet("background-color: " + color.name())
            self.viewer["axis"] = color
    
    def TaskColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.tasks.setStyleSheet("background-color: " + color.name())
            self.viewer["task"] = color
    
    def DeliveriesColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.deliveries.setStyleSheet("background-color: " + color.name())
            self.viewer["delivery"] = color
    
    def SelectedColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.lastop.setStyleSheet("background-color: " + color.name())
            self.viewer["select"] = color

    def VertexColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.vertex.setStyleSheet("background-color: " + color.name())
            self.graphEditor["vertex"] = color
            
    def EdgeColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.edge.setStyleSheet("background-color: " + color.name())
            self.graphEditor["line"] = color
            
    def SelectionColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.selection.setStyleSheet("background-color: " + color.name())
            self.graphEditor["selected"] = color
                
    def exec_(self):
        self.Backup()  
        QDialog.exec_(self)
        
    def OK(self):
        self.accept()
        
    def Cancel(self):
        self.LoadBackup()
        self.reject()

    def Backup(self):
        self.backup = [{}, {}]
        for k in self.viewer.keys():
            self.backup[0][k] = self.viewer[k]
        for k in self.graphEditor.keys():
            self.backup[1][k] = self.graphEditor[k]

    def LoadBackup(self):
        for k in self.viewer.keys():
            self.viewer[k] = self.backup[0][k]
        for k in self.graphEditor.keys():
            self.graphEditor[k] = self.backup[1][k]
        self.backup = [{}, {}]