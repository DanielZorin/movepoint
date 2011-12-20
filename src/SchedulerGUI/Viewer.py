from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, QColor, QInputDialog, QIntValidator, qApp
from PyQt4.QtCore import QTranslator
import sys, os, pickle, _pickle, re
from SchedulerGUI.Project import Project
from SchedulerGUI.NewProjectDialog import NewProjectDialog
from SchedulerGUI.PreferencesDialog import PreferencesDialog
from SchedulerGUI.SettingsDialog import SettingsDialog
from SchedulerGUI.RandomSystemDialog import RandomSystemDialog
from SchedulerGUI.ScheduleVisualizer import ScheduleVisualizer
from SchedulerGUI.ScheduleContainer import ScheduleContainer
from SchedulerGUI.ComboBoxDialog import ComboBoxDialog
from SchedulerGUI.Windows.ui_Viewer import Ui_Viewer
from Schedules.Exceptions import SchedulerException

class Viewer(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Viewer()
        self.ui.setupUi(self)
        self.visualizer = ScheduleVisualizer(self.ui.visualizerArea)
        self.ui.visualizerArea.setWidget(self.visualizer)

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