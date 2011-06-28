from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, qApp
from PyQt4.QtCore import QTranslator
from SRGMGUI.ui_main import Ui_MainWindow
from SRGMGUI.ProjectDialog import ProjectDialog, DataSelectDialog
from SRGMGUI.Graph import Graph
from SRGMGUI.AddDataDialog import AddDataDialog
from SRGMGUI.Project import Project
from SRGM.SRGMList import SRGMList
import sys, pickle, _pickle, os

class MainWindow(QMainWindow):
    
    project = None
    projectFile = None
    
    projFilter = ""
    models = []

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graph = Graph(self)
        self.ui.graph.show()
        self.projFilter = self.tr("SRGM projects (*.srgm *.srg)")
        self.setPreferences()
    
    def __del__(self):
        ''''f = open("srgm.ini", "wb")
        settings = {}
        settings["file"] = self.projectFile
        settings["models"] = self.models
        pickle.dump(settings, f)
        f.close()'''
        pass
    
    def setPreferences(self):
        if "srgm.ini" in os.listdir("."):
            try:
                f = open("srgm.ini", "rb")
                settings = pickle.load(f)
                self.projectFile = settings["file"]
                self.OpenProjectFromFile(self.projectFile)
                self.models = settings["models"]
                self.ChangeModels(self.models)
                f.close()
                # Temporary, until the language is saved in .ini file
                self.currentLanguage = "English"  
            except:
                self.loadDefaultPreferences()
        else:
            self.loadDefaultPreferences()
            
    def loadDefaultPreferences(self):
        self.project = Project()
        self.currentLanguage = "English" 
        self.models = SRGMList.keys()
        self.ChangeModels(self.models)

    def NewProject(self):
        #Open New project dialog
        d = ProjectDialog()
        d.exec_()
        if d.result() == QDialog.Accepted:
            res = d.GetData()
            self.project = Project(name=res["name"], data=res["file"])
            self.ChangeModels(res["models"])
            self.Update() 
        
    def OpenProject(self):
        #Call Open project dialog
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
        self.setWindowTitle(self.project.name + " - SRGM GUI")
        self.Update() 
        
    def SaveProject(self):
        if self.projectFile == None:
            self.SaveProjectAs()
        else:
            self.project.Serialize(self.projectFile)
    
    def SaveProjectAs(self):
        self.projectFile = QFileDialog.getSaveFileName(directory=self.project.name + ".srgm", filter=self.projFilter)
        if self.projectFile != '':
            self.project.Serialize(self.projectFile)             

    def ChangeModelsList(self):
        #Menu item handler
        # TODO: separate class, Qt Designer
        d = QtGui.QDialog()
        label = QtGui.QLabel("Select the models: ")
        box = []
        models = list(SRGMList.keys())
        for i in range(len(models)):
            box.append(QtGui.QCheckBox(models[i]))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        for i in range(len(models)):
            layout.addWidget(box[i])
        buttonOK = QtGui.QPushButton("OK")
        layout.addWidget(buttonOK)
        d.setLayout(layout)
        QtCore.QObject.connect(buttonOK, QtCore.SIGNAL("clicked()"), d, QtCore.SLOT("accept()"))
        d.exec_()
        if d.result() == QDialog.Accepted:         
            lst = []
            for i in range(len(models)):
                if box[i].isChecked():
                    lst.append(box[i].text())
            self.ChangeModels(lst)          
    
    def ChangeModels(self, lst):
        self.ui.comboBox.clear()
        self.models = lst
        for s in self.models:
            self.ui.comboBox.addItem(s)     

    def SelectData(self):
        # TODO: pass current settings here
        # TODO: visualize current restrictions
        settingsDialog = DataSelectDialog()
        settingsDialog.SetTime(self.project.GetStartTime(), self.project.GetEndTime())
        if settingsDialog.exec_() == QDialog.Accepted:
            # TODO: research the best way to handle such things
            a, b, c, d, e = settingsDialog.GetData()
            self.project.SetRestrictions(a, b, c, d, e)
            self.Update()
                    
    def AddData(self):
        #Add a new error
        d = AddDataDialog()
        if d.exec_() == QDialog.Accepted:
            self.project.AddError(d.GetData())
            self.Update() 

    def BatchAddData(self):
        #Add a pack of errors
        fileName = QtGui.QFileDialog.getOpenFileName(filter="XML files (*.xml)")
        if fileName == "":
            return
        self.project.AddData(fileName)
        self.Update() 

    def LoadNewXml(self):
        #Loads new data, overrides current
        fileName = QtGui.QFileDialog.getOpenFileName(filter="XML files (*.xml)")
        if fileName == "":
            return
        self.project.ReplaceData(fileName)
        self.Update() 
    
    def Compute(self):
        model = self.ui.comboBox.currentText()
        res = self.project.ComputeModel(model)
        self.ui.graph.AddFunction("Mean function", res["fmean"])
        # This isn't used
        #self.ui.graph.intensity = res["fint"]
        f = res["fmean"]
        totaltime = self.project.GetTotalTime()
        total = self.project.GetErrorsNumber()
        week = f(totaltime+7)
        month = f(totaltime+30)
        year = f(totaltime+365)
        self.ui.estimate.setText(str(res["n"])[:8])
        self.ui.mttf.setText(str(res["mttf"])[:8])
        self.ui.afterWeek.setText(str(week)[:7])
        self.ui.week.setText(str(week - total)[:7])
        self.ui.afterMonth.setText(str(month)[:7])
        self.ui.month.setText(str(month - total)[:7])
        self.ui.afterYear.setText(str(year)[:7])
        self.ui.year.setText(str(year - total)[:7])
        self.ui.conf1.setText(str(res["conf1"])[:7])
        self.ui.conf2.setText(str(res["conf2"])[:7])
        self.Update()

    def Update(self):
        totaltime = self.project.GetTotalTime()
        total = self.project.GetErrorsNumber()
        self.ui.graph.SetLimits(totaltime, total)
        ef = self.project.GetErrorFunction()
        self.ui.graph.AddFunction("Errors", ef)
        self.ui.graph.update()
        self.ui.graphY.setText(str(total))
        self.ui.graphX.setText(str(totaltime))
        self.ui.numberOfFaults.setText(str(total))
        self.ui.testingTime.setText(str(totaltime))

    def About(self):
        #Calls about box
        m = QtGui.QMessageBox(self)
        m.setWindowTitle("About this program")
        m.setText("Designed by Daniel A. Zorin.")
        m.show()

    def Exit(self):
        #Quits program
        sys.exit(0)