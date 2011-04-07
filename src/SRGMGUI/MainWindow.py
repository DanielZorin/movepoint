from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFileDialog, QDialog, QMessageBox, QMainWindow, QColor, QInputDialog, QIntValidator, qApp
from PyQt4.QtCore import QTranslator
from ui_main import Ui_MainWindow
from ProjectDialog import ProjectDialog, OpenDialog, SettingsDialog
from Graph import Graph
from Project import Project
from SRGM.SRGM import SRGM
from SRGM.SRGMList import SRGMList
from SRGM.GoelOkumoto import GoelOkumoto
from SRGM.JelinskiMoranda import JelinskiMoranda
from SRGM.LittlewoodVerrall import LittlewoodVerrall
from SRGM.SShaped import SShaped
from SRGM.Logarithmic import Logarithmic
from SRGM.SRGMList import SRGMList
import sys, pickle, _pickle, os, math
import xml.dom.minidom

class MainWindow(QtGui.QMainWindow):
    
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
        #List of relevant data for slices
        self.programmers = []
        self.severity = []
        self.items = []
        self.errors = []
        self.LoadProject()
        QtCore.QObject.connect(self.ui.actionChange_models_list, 
                               QtCore.SIGNAL("triggered()"), self.ChangeModelsList)
        QtCore.QObject.connect(self.ui.actionLoad_new_XML_file, 
                               QtCore.SIGNAL("triggered()"), self.LoadNewXML)
        QtCore.QObject.connect(self.ui.actionSetup_data_selection, 
                               QtCore.SIGNAL("triggered()"), self.SetupDataDialog)
        QtCore.QObject.connect(self.ui.actionAdd_data_to_current_project, 
                               QtCore.SIGNAL("triggered()"), self.AddData)
        QtCore.QObject.connect(self.ui.actionBatch_data_load, 
                               QtCore.SIGNAL("triggered()"), self.BatchAddData)
        QtCore.QObject.connect(self.ui.pushButton, 
                               QtCore.SIGNAL("clicked()"), self.Compute)
        QtCore.QObject.connect(self.ui.pushButton_2, 
                               QtCore.SIGNAL("clicked()"), self.RePlot)
        QtCore.QObject.connect(self.ui.pushButton_3, 
                               QtCore.SIGNAL("clicked()"), self.Compare)
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

    def NewProject(self):
        #Open New project dialog
        d = ProjectDialog()
        d.exec()
        if d.result() == QDialog.Accepted:
            res = d.GetData()
            self.project = Project(name=res["name"], data=res["file"])
            self.ChangeModels(res["models"])
            self.LoadProject()
        
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
        self.LoadProject()
        
    def SaveProject(self):
        if self.projectFile == None:
            self.SaveProjectAs()
        else:
            self.project.Serialize(self.projectFile)
    
    def SaveProjectAs(self):
        self.projectFile = QFileDialog.getSaveFileName(directory=self.project.name + ".srgm", filter=self.projFilter)
        if self.projectFile != '':
            self.project.Serialize(self.projectFile)             

    def LoadProject(self):
        #Common function: call XML parser, write all necessary data
        self.ui.label_3.setText("Project name: " + self.project.name)
        self.ui.comboBox.clear()
        for s in self.models:
            self.ui.comboBox.addItem(s)
        self.startTime = 0
        self.endTime = 2**64
        self.computer = SRGM()
        self.endTime = self.computer.totaltime

    def ChangeModelsList(self):
        #Menu item handler
        d = QtGui.QDialog()
        label = QtGui.QLabel("Select the models: ")
        box = []
        models = list(SRGMList.keys())
        for i in range(len(models)):
            box.append(QtGui.QCheckBox(models[i]))
        #self.dialog.setTitle("Select models")
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

    def SetupDataDialog(self):
        #Setup slice of data
        self.settingsDialog = SettingsDialog()
        self.settingsDialog.lineedit4.setText(str(self.startTime))
        self.settingsDialog.lineedit5.setText(str(self.endTime))
        QtCore.QObject.connect(self.settingsDialog, QtCore.SIGNAL("accepted()"), self.SetupDataHandler)
        self.settingsDialog.show()   
        
    def SetupDataHandler(self):
        self.programmers = str(self.settingsDialog.lineedit1.text()).split(",")
        self.severity = str(self.settingsDialog.lineedit2.text()).split(",")
        self.items = str(self.settingsDialog.lineedit3.text()).split(",")
        if self.programmers == ['']:
            self.programmers = []
        if self.severity == ['']:
            self.severity = []
        if self.items == ['']:
            self.items = []
        self.startTime = int(self.settingsDialog.lineedit4.text())
        self.endTime = int(self.settingsDialog.lineedit5.text())
        #self.SetupData()
        
    def SetupData(self):
        #Here the slice is done
        #TODO: WTF IS THIS WHY THE FUCK DO WE OVERWRITE THE FILE!?
        times = []
        if self.programmers == [] or str(self.errors[0]["programmer"]) in self.programmers:
            if self.severity == [] or str(self.errors[0]["severity"]) in self.severity:
                if self.items == [] or str(self.errors[0]["item"]) in self.items:
                    times.append(self.errors[0]["time"])
        for s in self.errors[1:]:
            if self.programmers != [] and not str(s["programmer"]) in self.programmers:
                pass
            elif self.severity != [] and not str(s["severity"]) in self.severity:
                pass
            elif self.items != [] and not str(s["item"]) in self.items:
                pass
            else:
                times.append(s["time"])
        times.sort()
        f = open(self.fileName, "w")
        f.close()
        for i in range(len(times)):
            if times[i] >= self.startTime:
                f = open(self.fileName, "w")
                f.write(str(times[i]))
                for k in times[i+1:]:
                    if k > self.endTime:
                        break
                    f.write(","+str(k))
                f.close() 
                break   
                    
    def AddData(self):
        #Add a new error
        self.dialog = QtGui.QDialog()
        self.label = QtGui.QLabel("Input data for a new error: ")
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.label1 = QtGui.QLabel("Time: ")
        self.input1 = QtGui.QSpinBox()
        self.input1.setValue(self.computer.totaltime)
        self.label2 = QtGui.QLabel("Programmer ID: ")
        self.input2 = QtGui.QSpinBox()
        self.input2.setValue(1)
        self.label3 = QtGui.QLabel("Severity: ")
        self.input3 = QtGui.QSpinBox()
        self.input3.setValue(1)
        self.label4 = QtGui.QLabel("Item: ")
        self.input4 = QtGui.QSpinBox()
        self.input4.setValue(1)
        self.accept = QtGui.QPushButton("OK")
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.input2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.input3)
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.input4)
        self.layout.addWidget(self.accept)
        self.dialog.setLayout(self.layout)
        QtCore.QObject.connect(self.accept, QtCore.SIGNAL("clicked()"), self.dialog, QtCore.SLOT("accept()"))
        QtCore.QObject.connect(self.dialog, QtCore.SIGNAL("accepted()"), self.AddDataHandler)
        self.dialog.show()  
              

    def AddDataHandler(self):
        newError = {}
        newError["time"] = self.input1.value()
        newError["programmer"] = self.input2.value()
        newError["severity"] = self.input3.value()
        newError["item"] = self.input4.value()
        name = self.fileNameXml
        q = open(name, "r")
        dom = xml.dom.minidom.parse(q)
        q.close()
        dom.normalize()
        for node in dom.childNodes:
            if node.tagName == "errors":
                e = dom.createElement("error")
                node.appendChild(e)
                time = dom.createElement("time")
                time.appendChild(dom.createTextNode(str(newError["time"])))
                e.appendChild(time)
                programmer = dom.createElement("programmer")
                programmer.appendChild(dom.createTextNode(str(newError["programmer"])))
                e.appendChild(programmer)
                severity = dom.createElement("severity")
                severity.appendChild(dom.createTextNode(str(newError["severity"])))
                e.appendChild(severity)
                item = dom.createElement("item")
                item.appendChild(dom.createTextNode(str(newError["item"])))
                e.appendChild(item)
        ft = open(self.fileNameXml, "w")
        dom.writexml(ft)
        ft.close()
        self.ParseXml()
        self.SetupData()

    def BatchAddData(self):
        #Add a pack of errors
        fileName = QtGui.QFileDialog.getOpenFileName()
        if fileName == "":
            return
        self.project.AddData(fileName)

    def LoadNewXML(self):
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

    def RePlot(self):
        #Refreshes the graph
        if self.ui.comboBox_2.currentText() == "Mean value function":
            self.ui.graph.Change(1)
            self.ui.label_13.setText(str(self.computer.total+1.5))
            self.ui.label_14.setText(str(self.computer.totaltime+1))
        else:
            self.ui.graph.Change(2)
            self.ui.label_13.setText(str(self.ui.graph.func(0)*1.3))
            self.ui.label_14.setText(str(self.computer.totaltime+1))
        self.ui.graph.update()
        
    def Compare(self):
        #Fills the table of comparison
        try:
            f = open("projects/"+self.currentProject+".log", "rb")
            u = pickle.Unpickler(f)
            log = u.load()
            f.close()
        except:
            log = []
        #log = [-1,-1,-1,-1,-1]
        numbers = []
        a, p, b, a0, a1 = self.computer.GoelOkumoto()
        model = {}
        model["estimate"] = a
        if a == -2:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (a*(1-math.exp(-p*t))/i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[0]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = a / log[0]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        a, p, b = self.computer.JelinskiMoranda()
        model = {}
        model["estimate"] = a
        if a == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (a*(1-math.exp(-p*int(t))) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[1]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = a / log[1]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        a, b, p = -1, -1, [-1, -1, -1]#self.computer.LittlewoodVerrall()
        model = {}
        model["estimate"] = (100*(p[0]-1)**2 - p[1]**2)/(2*p[2]*(p[0]-1))
        if model["estimate"] < 0:
            model["estimate"] = - model["estimate"]
        if b == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += ((p[0]-1)/(4*p[2]*(p[0]-1)) * math.sqrt(2*p[2]*(p[0]-1)*t + p[1]**2) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[2]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = model["estimate"] / log[2]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        #numbers.append({"converge":"no", "accuracy":0, "stability":0, "recommend":"no"})
        a, p, b = self.computer.SShaped()
        model = {}
        model["estimate"] = a
        if a == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (a*(1-(1+p)*math.exp(-p*t)) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[3]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = a / log[3]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        b0, b1, b = self.computer.Logarithmic()
        model = {}
        model["estimate"] = (b0*b1*10 - 1) / b1
        if a == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (b0*math.log(t*b1 + 1) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[4]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = model["estimate"] / log[4]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        f = open("projects/"+self.currentProject+".log", "wb")
        p = pickle.Pickler(f)
        p.dump(numbers)
        f.close()
        self.ui.tableWidget.setItem(0,0, QtGui.QTableWidgetItem(numbers[0]["converge"]))
        self.ui.tableWidget.setItem(0,1, QtGui.QTableWidgetItem(numbers[1]["converge"]))
        self.ui.tableWidget.setItem(0,2, QtGui.QTableWidgetItem(numbers[2]["converge"]))
        self.ui.tableWidget.setItem(0,3, QtGui.QTableWidgetItem(numbers[3]["converge"]))
        self.ui.tableWidget.setItem(0,4, QtGui.QTableWidgetItem(numbers[4]["converge"]))
        self.ui.tableWidget.setItem(1,0, QtGui.QTableWidgetItem(str(numbers[0]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,1, QtGui.QTableWidgetItem(str(numbers[1]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,2, QtGui.QTableWidgetItem(str(numbers[2]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,3, QtGui.QTableWidgetItem(str(numbers[3]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,4, QtGui.QTableWidgetItem(str(numbers[4]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(2,0, QtGui.QTableWidgetItem(str(numbers[0]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,1, QtGui.QTableWidgetItem(str(numbers[1]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,2, QtGui.QTableWidgetItem(str(numbers[2]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,3, QtGui.QTableWidgetItem(str(numbers[3]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,4, QtGui.QTableWidgetItem(str(numbers[4]["stability"])[:6]))
        self.ui.tableWidget.setItem(3,0, QtGui.QTableWidgetItem(numbers[0]["recommend"]))
        self.ui.tableWidget.setItem(3,1, QtGui.QTableWidgetItem(numbers[1]["recommend"]))
        self.ui.tableWidget.setItem(3,2, QtGui.QTableWidgetItem(numbers[2]["recommend"]))
        self.ui.tableWidget.setItem(3,3, QtGui.QTableWidgetItem(numbers[3]["recommend"]))
        self.ui.tableWidget.setItem(3,4, QtGui.QTableWidgetItem(numbers[4]["recommend"]))
        
    def About(self):
        #Calls about box
        m = QtGui.QMessageBox(self)
        m.setWindowTitle("About this program")
        m.setText("Designed by Daniel A. Zorin. Just as planned!")
        m.show()

    def Exit(self):
        #Quits program
        sys.exit(0)