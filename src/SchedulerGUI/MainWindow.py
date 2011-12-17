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
from SchedulerGUI.Windows.ui_MainWindow import Ui_MainWindow
from Schedules.Exceptions import SchedulerException

class MainWindow(QMainWindow):
    
    project = None
    projectFile = None
    
    projFilter = ""
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.visualizer = ScheduleVisualizer(self.ui.visualizerArea)
        self.ui.visualizerArea.setWidget(self.visualizer)
        self.projFilter = self.tr("Scheduler projects (*.proj *.prj)")
        self.title = self.tr("Scheduler GUI")
        self.loadTranslations()
        self.setPreferences()
    
    def __del__(self):
        ''''f = open("scheduler.ini", "wb")
        settings = {}
        settings["file"] = self.projectFile
        settings["preferences"] = self.preferences.Serialize()
        pickle.dump(settings, f)
        f.close()'''
        pass
    
    def setPreferences(self):
        # TODO: it's necessary to think how the default preferences are set.
        self.preferences = PreferencesDialog()
        if "scheduler.ini" in os.listdir("."):
            try:
                f = open("scheduler.ini", "rb")
                settings = pickle.load(f)
                self.preferences.Deserialize(settings["preferences"])
                self.projectFile = settings["file"]
                self.OpenProjectFromFile(self.projectFile)
                self.UpdatePreferences()
                f.close()
                # Temporary, until the language is saved in .ini file
                self.currentLanguage = "English"  
            except:
                self.loadDefaultPreferences()
        else:
            self.loadDefaultPreferences()
            
    def loadDefaultPreferences(self):
        self.preferences.setColors(QColor(168, 34, 3), QColor(168, 134, 50), QColor(100, 0, 255), QColor(255, 0, 0))
        self.visualizer.SetColors(QColor(168, 34, 3), QColor(168, 134, 50), QColor(100, 0, 255), QColor(255, 0, 0))      
        self.project = Project() 
        self.currentLanguage = "English"
    
    def loadTranslations(self):
        q = os.curdir
        tmp = os.listdir(os.curdir)
        all = os.listdir("./Translations")
        tsfile = re.compile("Scheduler_([a-zA-z]*)\.ts")
        res = []
        for s in all:
            m = tsfile.match(s)
            if m != None:
                res.append(m.group(1))
                #os.system("lrelease Translations/" + s + " -qm Translations/" + s.replace(".ts", ".qm"))
        self.languages = res

    def NewProject(self):
        self.newproject = NewProjectDialog()
        self.newproject.exec_()
        if self.newproject.result() == QDialog.Accepted:
            try:
                self.project = Project(self.newproject.GetSystem(), self.newproject.GetConfig(), self.newproject.GetName())     
            except SchedulerException as e:
                QMessageBox.critical(self, "An error occured", e.message)
                return  
            self.setWindowTitle(self.project.name + " - " + self.title) 
            self.EnableRunning()
            self.loadSchedule()
            t, r = self.project.GetLimits()
            self.setLimits(t, r)
    
    def OpenProject(self):
        name = QFileDialog.getOpenFileName(filter=self.projFilter)
        if name == None or name == '':
            return
        self.OpenProjectFromFile(name)
        
    def OpenProjectFromFile(self, name):
        self.project = Project()
        try:
            self.project.Deserialize(name)
        except _pickle.UnpicklingError:
            QMessageBox.critical(self, "An error occured", "File is not a valid project file: " + name)
            return  
        self.projectFile = name
        self.setWindowTitle(self.project.name + " - " + self.title) 
        self.EnableRunning()
        self.loadSchedule()
        t, r = self.project.GetLimits()
        self.setLimits(t, r)
    
    def SaveProject(self):
        if self.projectFile == None:
            self.SaveProjectAs()
        else:
            self.project.Serialize(self.projectFile)
    
    def SaveProjectAs(self):
        self.projectFile = QFileDialog.getSaveFileName(directory=self.project.name + ".proj", filter=self.projFilter)
        if self.projectFile != '':
            self.project.Serialize(self.projectFile)
    
    def EnableRunning(self):
        self.ui.actionStart.setEnabled(True)
        self.ui.actionTrace.setEnabled(True)
        self.ui.actionStep_Backward.setEnabled(True)
        self.ui.actionStep_Forward.setEnabled(True)
        self.ui.actionReset.setEnabled(True)
        self.ui.stepforth.setEnabled(True)
        self.ui.lineEdit.setEnabled(True)
        self.ui.laststep.setEnabled(True)
    
    def Run(self):
        self.project.method.iteration = 0
        self.project.method.Start()
        self.loadSchedule()
    
    def Trace(self):
        iter = 0
        # TODO: encapsulate number of iterations
        while iter < self.project.method.numberOfIterations:
            self.project.Step()
            iter += 1
            print(iter)
            self.loadSchedule()
    
    def StepForward(self):
        self.project.Step()
        self.loadSchedule()
    
    def StepBackward(self):
        self.loadSchedule()
            
    def SelectSchedule(self, s):
        if s == '':
            return
        # TODO: check why the validator doesn't work sometimes
        n = int(s)
        self.container.current = n - 1
        self.loadSchedule()
        
    def ResetSchedule(self):
        self.project.ResetSchedule()
        self.loadSchedule()
    
    def ChangeScale(self, value):
        self.visualizer.SetScale(1.0 + float(value) / 100.0)
        
    def ShowLastStep(self):
        self.ui.laststepdata.setText(str(self.container.GetCurrentOperation()))
        self.visualizer.Visualize(self.container.GetCurrent(), self.container.GetCurrentOperation())
    
    def LoadSystem(self):
        s = QFileDialog.getOpenFileName()
        if s != '':
            try:
                self.project.ChangeSystem(s)
            except SchedulerException as e:
                QMessageBox.critical(self, "An error occured", e.message)
                return  
            self.EnableRunning()
            self.loadSchedule()
            t, r = self.project.GetLimits()
            self.setLimits(t, r)
    
    def LoadMethod(self):
        s = QFileDialog.getOpenFileName()
        if s != '':
            try:
                self.project.ChangeMethod(s)
            except SchedulerException as e:
                QMessageBox.critical(self, "An error occured", e.message)
                return  
    
    def ChangeName(self):
        s = QInputDialog.getText(self, "Change Project Name", "Enter the new project name", text=self.project.name)
        if s[1] == True:           
            self.project.ChangeName(s[0])
            self.setWindowTitle(self.project.name + " - " + self.title) 
    
    def ChangeLimits(self):
        t, r = self.project.GetLimits()
        data = {"Time":t, "Reliability": r}
        d = SettingsDialog(data)
        d.exec_()
        if d.result() == QDialog.Accepted:
            t = data["Time"]
            r = data["Reliability"]
            self.setLimits(t, r)   
            self.project.SetLimits(t, r)   
            
    def Settings(self):
        data = self.project.method.Serialize()
        d = SettingsDialog(data)
        d.exec_()
        if d.result() == QDialog.Accepted:
            self.project.method.Deserialize(d.data)
    
    def GenerateRandomSystem(self):
        d = RandomSystemDialog()
        d.exec_()
        if d.result() == QDialog.Accepted:
            params = d.GetResult()
            self.project.GenerateRandomSystem(params)
            self.loadSchedule()
            t, r = self.project.GetLimits()
            self.setLimits(t, r)

    def ChangeLanguage(self):
        dialog = ComboBoxDialog(self.languages, self.currentLanguage)
        dialog.exec_()
        selected = self.languages[dialog.combo.currentIndex()]
        self.currentLanguage = selected
        self.Translate("Translations\Scheduler_" + selected + ".qm")
    
    def Translate(self, lang):
        # TODO: add all strings from various files
        translator = QTranslator(qApp)
        translator.load(lang)
        qApp.installTranslator(translator)
        self.ui.retranslateUi(self)   
        self.preferences.ui.retranslateUi(self.preferences) 
        self.loadSchedule()    
        self.setWindowTitle(self.project.name + " - " + self.tr(self.title)) 

    def Preferences(self):
        self.preferences.exec_()
        if self.preferences.result() == QDialog.Accepted:
            self.UpdatePreferences()
            
    def UpdatePreferences(self):
        self.visualizer.SetColors(self.preferences.axisColor, 
                                  self.preferences.taskColor,
                                  self.preferences.deliveriesColor,
                                  self.preferences.lastopColor)        
    
    def About(self):
        #Calls about box
        QMessageBox.about(self, "About this program", "Scheduler GUI.\nAuthor: Daniel A. Zorin\njuan@lvk.cs.msu.su")

    def Exit(self):
        #Quits program
        sys.exit(0)
    
    def setLimits(self, t, r):
        self.ui.tdir.setText(str(t))
        self.ui.rdir.setText('{:f}'.format(r)[:10])
    
    def loadSchedule(self):        
        self.visualizer.Visualize(self.project.system.schedule)
        return
        self.showTotals()
        self.ui.labelTotal.setText(str(self.container.GetTotal()))
        self.ui.lineEdit.setText(str(self.container.current + 1))
        self.validator = QIntValidator(1, self.container.GetTotal(), self)
        self.ui.lineEdit.setValidator(self.validator)
        
        if self.container.IsLast():
            self.ui.laststep.setEnabled(False)
        else:
            self.ui.laststep.setEnabled(True)
            
        if self.container.current == 0:
            self.ui.stepback.setEnabled(False)
        else:
            self.ui.stepback.setEnabled(True)
        
    def showTotals(self):
        s = self.container.GetCurrentStats()
        self.ui.labeltime.setText(str(s[0]))
        self.ui.labelrel.setText('{:f}'.format(s[1])[:10])
        self.ui.labelproc.setText(str(s[2]))