from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, QColor, QListWidgetItem, QIntValidator, QDoubleValidator, QLineEdit, qApp, QTableWidgetItem
from PyQt4.QtCore import QTranslator, SIGNAL
import sys, os, pickle, _pickle, re
from SchedulerGUI.Project import Project
from SchedulerGUI.NewProjectDialog import NewProjectDialog
from SchedulerGUI.SettingsDialog import SettingsDialog
from SchedulerGUI.PreferencesDialog import PreferencesDialog
from SchedulerGUI.RandomSystemDialog import RandomSystemDialog
from SchedulerGUI.ComboBoxDialog import ComboBoxDialog
from SchedulerGUI.Viewer import Viewer
from SchedulerGUI.GraphEditor import GraphEditor
from Schedules.Exceptions import SchedulerException
from SchedulerGUI.Windows.ui_MainWindowInitial import Ui_MainWindow as SplashScreen
from SchedulerGUI.Windows.ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    
    project = None
    projectFile = None
    recentfiles = []
    
    currentLanguage = "English"
    projFilter = ""

    splash = True
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = SplashScreen()
        self.ui.setupUi(self)
        self.projFilter = self.tr("Scheduler projects (*.proj *.prj)")
        self.title = self.tr("Scheduler GUI")
        self.loadTranslations()
        self.loadIniFile()
 
    def loadIniFile(self):
        if "scheduler.ini" in os.listdir("."):
            try:
                f = open("scheduler.ini", "rb")
                settings = pickle.load(f)
                self.recentfiles = settings["recent"]
                self.currentLanguage = settings["language"]
                f.close()
            except:
                pass
            for p in self.recentfiles:
                self.ui.recent.addItem(p[1])
            self.Translate(self.currentLanguage)
 
    def writeIniFile(self):
        f = open("scheduler.ini", "wb")
        settings = {}
        settings["recent"] = self.recentfiles
        settings["language"] = self.currentLanguage
        pickle.dump(settings, f)
        f.close()          
                    
    def closeEvent(self, e):
        self.writeIniFile()
        e.accept()

    def LoadMainWindow(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.viewer = Viewer()
        self.graphEditor = GraphEditor()
        self.settings = PreferencesDialog(self.viewer.visualizer.colors, self.graphEditor.canvas.colors)
        QtCore.QObject.connect(self, SIGNAL("step"), self.ui.progress.setValue)
        self.splash = False

    def LoadNew(self):
        self.newproject = NewProjectDialog()
        self.newproject.exec_()
        if self.newproject.result() == QDialog.Accepted:
            try:
                self.project = Project(self.newproject.GetSystem(), self.newproject.GetName())     
            except SchedulerException as e:
                QMessageBox.critical(self, "An error occured", e.message)
                return  
            self.LoadMainWindow()
            self.setupProject()

    def LoadOpen(self):
        name = QFileDialog.getOpenFileName(filter=self.projFilter)
        if name == None or name == '':
            return
        self.LoadMainWindow()
        self.OpenProjectFromFile(name)

    def LoadRecent(self, item):
        for p in self.recentfiles:
            if p[1] == item.text():
                name = p[0]
                self.project = Project()
                try:
                    self.project.Deserialize(name)
                except: #_pickle.UnpicklingError:
                    QMessageBox.critical(self, "An error occured", "File is not a valid project file: " + name)
                    self.recentfiles = [p for p in self.recentfiles if p[0] != name]
                    for p in self.recentfiles:
                        self.ui.recent.addItem(p[1])
                    return
                self.LoadMainWindow()
                self.projectFile = name
                self.setupProject()
                self.AddToRecent(name, self.project.name)
                return                
    
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
                self.project = Project(self.newproject.GetSystem(), self.newproject.GetName())     
            except SchedulerException as e:
                QMessageBox.critical(self, "An error occured", e.message)
                return  
            self.setupProject()
    
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
        self.setupProject()
        self.AddToRecent(name, self.project.name)
    
    def SaveProject(self):
        if self.projectFile == None:
            self.SaveProjectAs()
        else:
            self.project.graph = self.graphEditor.SavePositions()
            self.project.Serialize(self.projectFile)
            self.AddToRecent(self.projectFile, self.project.name)
    
    def SaveProjectAs(self):
        self.projectFile = QFileDialog.getSaveFileName(directory=self.project.name + ".proj", filter=self.projFilter)
        if self.projectFile != '':
            self.project.graph = self.graphEditor.SavePositions()
            self.project.Serialize(self.projectFile)
            self.AddToRecent(self.projectFile, self.project.name)

    def setupProject(self):
        self.setWindowTitle(self.project.name + " - " + self.title)
        self.graphEditor.setData(self.project.system)
        if self.LoadErrors():
            self.EnableRunning()
        else:
            self.DisableRunning()
        self.loadSchedule()
        self.ui.projectname.setText(self.project.name)
        self.graphEditor.LoadPositions(self.project.graph)
 
    def AddToRecent(self, f, name):
        newrecent = []
        toadd = True
        for p in self.recentfiles:
            if p[0] == f:
                newrecent = [[p[0], name]] + newrecent
                toadd = False
            else:
                newrecent.append(p)
        if toadd:
            newrecent = [[f, name]] + newrecent
            if len(newrecent) > 5:
                newrecent = newrecent[:-1]
        self.recentfiles = newrecent
            
    def EnableRunning(self):
        self.ui.actionStart.setEnabled(True)
        self.ui.actionReset.setEnabled(True)
        self.ui.actionLaunch_Viewer.setEnabled(True)
        self.ui.runbutton.setEnabled(True) 

    def DisableRunning(self):
        self.ui.actionStart.setEnabled(False)
        self.ui.actionReset.setEnabled(False)
        self.ui.actionLaunch_Viewer.setEnabled(False)
        self.ui.runbutton.setEnabled(False) 

    def LaunchViewer(self):
        self.viewer.show()

    def EditProgram(self):
        self.graphEditor.show()
        # Wait until the editor window is closed
        while self.graphEditor.isVisible():
            qApp.processEvents()
        if self.LoadErrors():
            self.project.method.Reset()
            self.viewer.setData(self.project.method)
            self.EnableRunning()
        else:
            self.DisableRunning()
            self.viewer.hide()

    def LoadErrors(self):
        self.ui.errors.clear()
        self.ui.errors.verticalHeader().hide()
        self.ui.errors.horizontalHeader().hide()
        self.ui.errors.horizontalHeader().setStretchLastSection(True)
        self.ui.errors.setColumnCount(2)
        cycles = self.project.method.system.program.CheckCycles()
        ok = True
        for v in cycles:
            ok = False
            self.ui.errors.insertRow(0)
            item = QTableWidgetItem("Error")
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.errors.setItem(0, 0, item)
            item2 = QTableWidgetItem("Task " + v.name + " " + str(v.number) + " is in a cycle")
            item2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.errors.setItem(0, 1, item2)
        return ok

    def HideErrors(self):
        self.ui.errors.hide()
        # TODO: adjust window size

    def Run(self):
        self.project.method.iteration = 0
        while self.project.method.iteration < self.project.method.numberOfIterations:
            self.project.method.Step()
            print(self.project.method.iteration)
            self.project.method.iteration += 1
            #self.ui.progress.setValue(self.project.method.iteration)
            self.emit(SIGNAL("step"), self.project.method.iteration)
        self.loadSchedule()
        
    def ResetSchedule(self):
        self.project.ResetSchedule()
        self.loadSchedule()
    
    def ChangeScale(self, value):
        self.visualizer.SetScale(1.0 + float(value) / 100.0)
        
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
    
    def EditName(self):
        self.lineedit = QLineEdit(self.ui.projectname.parentWidget())
        self.lineedit.setGeometry(self.ui.projectname.geometry())
        self.lineedit.setText(self.ui.projectname.text())
        self.lineedit.setFocus()
        self.lineedit.show()
        self.ui.projectname.hide()
        # TODO: what's wrong?
        #self.ui.editname.hide()
        QtCore.QObject.connect(self.lineedit, SIGNAL("editingFinished()"), self.ChangeName)

    def ChangeName(self):
        s = self.lineedit.text()
        self.ui.projectname.setText(s)
        self.ui.projectname.show()
        #self.ui.editname.show()
        self.lineedit.hide() 
        self.project.ChangeName(s)
        self.setWindowTitle(self.project.name + " - " + self.title) 

    def EditTdir(self):
        self.tlineedit = QLineEdit(self.ui.tdir.parentWidget())
        self.tlineedit.setGeometry(self.ui.tdir.geometry())
        self.tlineedit.setText(self.ui.tdir.text())
        val = QIntValidator(self)
        self.tlineedit.setValidator(val)
        self.tlineedit.setFocus()
        self.tlineedit.show()
        #self.ui.tdir.hide()
        self.ui.edittime.hide()
        QtCore.QObject.connect(self.tlineedit, SIGNAL("editingFinished()"), self.ChangeTdir)
    
    def ChangeTdir(self):
        t = self.tlineedit.text()
        self.ui.tdir.setText(t)
        self.ui.tdir.show()
        self.ui.edittime.show()
        self.tlineedit.hide()
        t = int(t)
        self.project.SetTdir(t)

    def EditRdir(self):
        self.rlineedit = QLineEdit(self.ui.rdir.parentWidget())
        self.rlineedit.setGeometry(self.ui.rdir.geometry())
        self.rlineedit.setText(self.ui.rdir.text())
        val = QDoubleValidator(self)
        self.rlineedit.setValidator(val)
        self.rlineedit.setFocus()
        self.rlineedit.show()
        #self.ui.rdir.hide()
        self.ui.editrel.hide()
        QtCore.QObject.connect(self.rlineedit, SIGNAL("editingFinished()"), self.ChangeRdir)

    def ChangeRdir(self):
        r = self.rlineedit.text()
        self.ui.rdir.setText(r)
        self.ui.rdir.show()
        self.ui.editrel.show()
        self.rlineedit.hide()
        r = float(r)
        self.project.SetRdir(r)  
            
    def Parameters(self):
        data = self.project.method.Serialize()
        d = SettingsDialog(data)
        d.exec_()
        if d.result() == QDialog.Accepted:
            self.project.method.Deserialize(d.data)
 
    def Settings(self):
        self.settings.exec_()
        if self.settings.result() == QDialog.Accepted:
            pass
               
    def GenerateRandomSystem(self):
        d = RandomSystemDialog()
        d.exec_()
        if d.result() == QDialog.Accepted:
            params = d.GetResult()
            self.project.GenerateRandomSystem(params)
            self.loadSchedule()

    def ChangeLanguage(self):
        dialog = ComboBoxDialog(self.languages, self.currentLanguage)
        dialog.exec_()
        selected = self.languages[dialog.combo.currentIndex()]
        self.currentLanguage = selected
        self.Translate(selected)
    
    def Translate(self, lang):
        # TODO: add all strings from various files
        translator = QTranslator(qApp)
        translator.load("Translations\Scheduler_" + lang + ".qm")
        qApp.installTranslator(translator)
        self.ui.retranslateUi(self)
        if not self.splash:
            self.viewer.preferences.ui.retranslateUi(self.viewer.preferences)
            self.viewer.ui.retranslateUi(self.viewer) 
            self.loadSchedule()    
            self.setWindowTitle(self.project.name + " - " + self.tr(self.title))     
    
    def ExportTrace(self):
        tracefile = QFileDialog.getSaveFileName(directory=self.project.name + ".trace")
        if tracefile != '':
            f = open(tracefile, "w")
            f.write(self.project.method.trace.Export())
            f.close()

    def ExportSchedule(self):
        file = QFileDialog.getSaveFileName(directory=self.project.name + "-result.xml")
        if file != '':
            f = open(file, "w")
            f.write(self.project.system.schedule.ExportXml())
            f.close()

    def GenerateCode(self):
        pass

    def About(self):
        #Calls about box
        QMessageBox.about(self, "About this program", "Scheduler GUI.\nAuthor: Daniel A. Zorin\njuan@lvk.cs.msu.su")

    def Exit(self):
        #Quits program
        self.writeIniFile()
        sys.exit(0)
    
    def loadSchedule(self): 
        self.viewer.setData(self.project.method)  
        self.ui.vertices.setText(str(len(self.project.system.schedule.program.vertices)))
        self.ui.edges.setText(str(len(self.project.system.schedule.program.edges)))
        self.ui.tracelen.setText(str(self.project.method.trace.length()))
        t, r = self.project.GetLimits()
        self.ui.tdir.setText(str(t))
        self.ui.rdir.setText('{:f}'.format(r)[:10])
        return