'''
Created on 06.01.2011

@author: juan
'''

from PyQt4.QtGui import QDialog, QColorDialog
from SchedulerGUI.Windows.ui_PreferencesDialog import Ui_PreferencesDialog

     
class PreferencesDialog(QDialog):
    
    axisColor = None
    taskColor = None
    deliveriesColor = None
    lastopColor = None
    
    axisColortmp = None
    taskColortmp = None
    deliveriesColortmp = None
    lastopColortmp = None
    
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        
    def AxisColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.axis.setStyleSheet("background-color: " + color.name())
            self.axisColortmp = color
    
    def TaskColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.tasks.setStyleSheet("background-color: " + color.name())
            self.taskColortmp = color
    
    def DeliveriesColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.deliveries.setStyleSheet("background-color: " + color.name())
            self.deliveriesColortmp = color
    
    def LastOpColor(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.ui.lastop.setStyleSheet("background-color: " + color.name())
            self.lastopColortmp = color
    
    def setColors(self, a, t, d, l):
        self.ui.axis.setStyleSheet("background-color: " + a.name())
        self.axisColor = a
        self.ui.tasks.setStyleSheet("background-color: " + t.name())
        self.taskColor = t
        self.ui.deliveries.setStyleSheet("background-color: " + d.name())
        self.deliveriesColor = d
        self.ui.lastop.setStyleSheet("background-color: " + l.name())
        self.lastopColor = l
    
    def exec(self):
        self.axisColortmp = self.axisColor
        self.taskColortmp = self.taskColor
        self.deliveriesColortmp = self.deliveriesColor
        self.lastopColortmp = self.lastopColor      
        QDialog.exec(self)
        
    def OK(self):
        self.axisColor = self.axisColortmp
        self.taskColor = self.taskColortmp
        self.deliveriesColor = self.deliveriesColortmp
        self.lastopColor = self.lastopColortmp
        self.accept()
        
    def Cancel(self):
        self.setColors(self.axisColor, self.taskColor, self.deliveriesColor, self.lastopColor)
        self.reject()
        
    def Serialize(self):
        return {"axis":self.axisColor,
                "task":self.taskColor,
                "delivery":self.deliveriesColor,
                "lastop":self.lastopColor}
    
    def Deserialize(self, dict):
        self.setColors(dict["axis"], dict["task"], dict["delivery"], dict["lastop"])