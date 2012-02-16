from PyQt4.QtGui import QDialog, QMainWindow, QIntValidator
from PyQt4.QtCore import SIGNAL, QObject
from SchedulerGUI.PreferencesDialog import PreferencesDialog
from SchedulerGUI.ScheduleVisualizer import ScheduleVisualizer
from SchedulerGUI.Windows.ui_Viewer import Ui_Viewer

class Viewer(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Viewer()
        self.ui.setupUi(self)
        self.visualizer = ScheduleVisualizer(self.ui.visualizerArea)
        self.ui.visualizerArea.setWidget(self.visualizer)
        self.preferences = PreferencesDialog()
        QObject.connect(self.visualizer, SIGNAL("ManualOperation"), self.Update)
        QObject.connect(self.visualizer, SIGNAL("WrongOperation"), self.Statusbar)

    def setData(self, m):
        self.method = m
        self.visualizer.Visualize(self.method)
        self.ui.stepforth.setEnabled(True)
        self.ui.lineEdit.setEnabled(True)
        self.ui.labelTotal.setText(str(self.method.trace.length()))
        self.ui.lineEdit.setText(str(self.method.trace.current + 1))
        self.validator = QIntValidator(1, self.method.trace.length(), self)
        self.ui.lineEdit.setValidator(self.validator)
        op = self.method.trace.getCurrent()
        self.showTotals(op[1])
            
        if self.method.trace.current == 0:
            self.ui.stepback.setEnabled(False)
            self.ui.rewind.setEnabled(False)
        else:
            self.ui.stepback.setEnabled(True)
            self.ui.rewind.setEnabled(True)

        if self.method.trace.current == self.method.trace.length() - 1:
            self.ui.stepforth.setEnabled(False)
            self.ui.replay.setEnabled(False)
        else:
            self.ui.stepforth.setEnabled(True)
            self.ui.replay.setEnabled(True)

    def Update(self):
        self.setData(self.method)

    def Statusbar(self, msg):
        self.ui.statusBar.showMessage(msg, 5000)

    def SelectSchedule(self, s):
        if s == '':
            return
        # TODO: check why the validator doesn't work sometimes
        n = int(s)
        self.ScrollTrace(n - 1 - self.method.trace.current)

    def ShowBest(self):
        self.ScrollTrace(self.method.trace.best - self.method.trace.current)

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
            if self.method.trace.current + diff >= self.method.trace.length():
                diff = self.method.trace.length() - self.method.trace.current - 1
            for i in range(diff):
                self.method.trace.current += 1
                op = self.method.trace.getCurrent()
                self.method.system.schedule.ApplyOperation(op[0])
        if diff < 0:
            if self.method.trace.current + diff < 0:
                diff = -self.method.trace.current
            for i in range(-diff):
                op = self.method.trace.getCurrent()
                self.method.system.schedule.ApplyOperation(op[0].Reverse())
                self.method.trace.current -= 1
        self.setData(self.method)
        self.ui.lineEdit.setText(str(self.method.trace.current + 1))
        op = self.method.trace.getCurrent()
        self.showTotals(op[1])

    def showTotals(self, s):
        self.ui.labeltime.setText(str(s["time"]))
        self.ui.labelrel.setText('{:f}'.format(s["reliability"])[:5])
        self.ui.labelproc.setText(str(s["processors"]))

    def Scale(self, v):
        newscale = 1.5
        v = float(v) / 50.0
        if v < 0:
            v = v / 2.0
            v += 1.0
        else:
            v *= 3.0
            v += 1.0
        self.visualizer.SetScale(1.5 * v)

    def resizeEvent(self, e):
        super(QMainWindow, self).resizeEvent(e)
        self.visualizer.ResizeCanvas()