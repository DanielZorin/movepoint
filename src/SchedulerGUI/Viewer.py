from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, QColor, QInputDialog, QIntValidator, qApp
from PyQt4.QtCore import QTranslator
import sys, os, pickle, _pickle, re
from SchedulerGUI.Project import Project
from SchedulerGUI.PreferencesDialog import PreferencesDialog
from SchedulerGUI.ScheduleVisualizer import ScheduleVisualizer
from SchedulerGUI.Windows.ui_Viewer import Ui_Viewer
from Schedules.Exceptions import SchedulerException

class Viewer(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Viewer()
        self.ui.setupUi(self)
        self.visualizer = ScheduleVisualizer(self.ui.visualizerArea)
        self.ui.visualizerArea.setWidget(self.visualizer)
        self.preferences = PreferencesDialog()

    def setData(self, m):
        self.method = m
        self.visualizer.Visualize(self.method.system.schedule)
        self.ui.stepforth.setEnabled(True)
        self.ui.lineEdit.setEnabled(True)
        self.ui.labelTotal.setText(str(self.method.trace.length()))
        self.ui.lineEdit.setText(str(self.method.trace.length()))
        self.validator = QIntValidator(1, self.method.trace.length(), self)
        self.ui.lineEdit.setValidator(self.validator)
            
        if self.method.trace.current == 0:
            self.ui.stepback.setEnabled(False)
        else:
            self.ui.stepback.setEnabled(True)

    def SelectSchedule(self, s):
        if s == '':
            return
        # TODO: check why the validator doesn't work sometimes
        n = int(s)
        self.container.current = n - 1
        self.loadSchedule()

    def Colors(self):
        self.preferences.exec_()
        if self.preferences.result() == QDialog.Accepted:
            self.UpdatePreferences()
            
    def UpdatePreferences(self):
        self.visualizer.SetColors(self.preferences.axisColor, 
                                  self.preferences.taskColor,
                                  self.preferences.deliveriesColor,
                                  self.preferences.lastopColor)  
        
    def StepForward(self):
        return  

    def StepBackward(self):
        return 