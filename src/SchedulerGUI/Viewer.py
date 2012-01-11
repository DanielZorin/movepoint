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

        if self.method.trace.current == self.method.trace.length() - 1:
            self.ui.stepforth.setEnabled(False)
        else:
            self.ui.stepforth.setEnabled(True)

    def SelectSchedule(self, s):
        if s == '':
            return
        # TODO: check why the validator doesn't work sometimes
        n = int(s)
        self.ScrollTrace(n - self.method.trace.current)

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
        self.ScrollTrace(1)

    def StepBackward(self):
        self.ScrollTrace(-1)

    def Replay(self):
        self.ScrollTrace(self.method.trace.length())

    def Rewind(self):
        self.ScrollTrace(-self.method.trace.length())

    def ScrollTrace(self, diff):
        if diff == 0:
            return
        if diff > 0:
            if self.method.trace.current + diff > self.method.trace.length():
                diff = self.method.trace.length() - self.method.trace.current
            for i in range(diff):
                self.method.trace.current += 1
                op = self.method.trace.getCurrent()
                self.method.system.schedule.ApplyOperation(op[0])
        if diff < 0:
            if self.method.trace.current - diff < 0:
                diff = -self.method.trace.current
            for i in range(-diff):
                op = self.method.trace.getCurrent()
                self.method.system.schedule.ApplyOperation(op[0].Reverse())
                print(diff, "minus")
                self.method.trace.current -= 1
        print("scrolling", diff, self.method.trace.current)
        self.setData(self.method)
        self.ui.lineEdit.setText(str(self.method.trace.current + 1))