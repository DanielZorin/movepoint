from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, qApp
from PyQt4.QtCore import QTranslator
from ui_main import Ui_MainWindow
from ProjectDialog import ProjectDialog, DataSelectDialog
from Graph import Graph
from AddDataDialog import AddDataDialog
from Project import Project
from SRGM.SRGMList import SRGMList
import sys, pickle, _pickle, os, math

class MainWindow(QMainWindow):
    
    project = None
    projectFile = None
    
    projFilter = ""
    models = []

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.projFilter = self.tr("SRGM projects (*.srgm *.srg)")
        self.setPreferences()
        self.ui.graph = Graph(self)
        self.ui.graph.show()
    
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
        d.exec()
        if d.result() == QDialog.Accepted:
            res = d.GetData()
            self.project = Project(name=res["name"], data=res["file"])
            self.ChangeModels(res["models"])
        
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
        d.exec()
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
        if settingsDialog.exec() == QDialog.Accepted:
            # TODO: research the best way to handle such things
            a, b, c, d, e = settingsDialog.GetData()
            self.project.SetRestrictions(a, b, c, d, e)
                    
    def AddData(self):
        #Add a new error
        d = AddDataDialog()
        if d.exec() == QDialog.Accepted:
            self.project.AddError(d.GetData()) 

    def BatchAddData(self):
        #Add a pack of errors
        fileName = QtGui.QFileDialog.getOpenFileName()
        if fileName == "":
            return
        self.project.AddData(fileName)

    def LoadNewXml(self):
        #Loads new data, overrides current
        fileName = QtGui.QFileDialog.getOpenFileName()
        if fileName == "":
            return
        self.project.ReplaceData(fileName)
    
    def Compute(self):
        model = self.ui.comboBox.currentText()
        res = self.project.ComputeModel(model)
        if self.ui.comboBox_2.currentIndex() == 0:
            self.ui.graph.func = res["fmean"]
        else:
            self.ui.graph.func = res["fint"]
        self.ui.graph.meanFunc = res["fmean"]
        self.ui.graph.intensity = res["fint"]
        f = res["fmean"]
        totaltime = self.project.GetTotalTime()
        total = self.project.GetErrorsNumber()
        self.ui.graph.time = totaltime
        self.ui.graph.number = total
        self.ui.graph.update()
        self.ui.label_13.setText(str(total+3))
        self.ui.label_14.setText(str(totaltime+1))
        week = f(totaltime+7)
        month = f(totaltime+30)
        year = f(totaltime+365)
        self.ui.label_18.setText(str(total))
        self.ui.label_22.setText(str(totaltime))
        self.ui.label_2.setText(str(res["n"])[:8])
        self.ui.label_5.setText(str(res["mttf"])[:8])
        self.ui.label_16.setText(str(month)[:7])
        self.ui.label_20.setText(str(month - total)[:7])
        self.ui.label_24.setText(str(year)[:7])
        self.ui.label_26.setText(str(year - total)[:7])
        self.ui.label_28.setText(str(week)[:7])
        self.ui.label_30.setText(str(week - total)[:7])
        self.ui.label_7.setText(str(res["conf1"])[:7])
        self.ui.label_9.setText(str(res["conf2"])[:7])
        self.RePlot()

    def RePlot(self):
        #Refreshes the graph
        # TODO: refactor the graph widget
        if self.ui.comboBox_2.currentText() == "Mean value function":
            self.ui.graph.Change(1)
        else:
            self.ui.graph.Change(2)
        self.ui.graph.update()

    def About(self):
        #Calls about box
        m = QtGui.QMessageBox(self)
        m.setWindowTitle("About this program")
        m.setText("Designed by Daniel A. Zorin. Just as planned!")
        m.show()

    def Exit(self):
        #Quits program
        sys.exit(0)