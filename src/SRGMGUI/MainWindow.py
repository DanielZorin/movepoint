from PyQt4 import QtGui, QtCore
from ui_main import Ui_MainWindow
from ProjectDialog import ProjectDialog, OpenDialog, SettingsDialog
from SRGM.SRGM import SRGM
from SRGM.GoelOkumoto import GoelOkumoto
from SRGM.JelinskiMoranda import JelinskiMoranda
from SRGM.LittlewoodVerrall import LittlewoodVerrall
from SRGM.SShaped import SShaped
from SRGM.Logarithmic import Logarithmic
import sys, pickle, os, math
import xml.dom.minidom

class Graph(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(440, 90, 300, 300)
        self.func = self.meanFunc = self.intensity = lambda x: 0
        self.time = self.number = 5

    def Change(self, k):
        if k == 1:
            self.func = self.meanFunc
        else:
            self.func = self.intensity

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setPen(QtGui.QColor(168, 34, 3))
        paint.setFont(QtGui.QFont('Decorative', 10))
        if self.func == self.meanFunc:
            x0, y0 = 0, self.height()
            ki = 300.0/(self.time+1)
            kj = 300.0/(self.number+1.5)
            for i in range(1, self.width()):
                x1, y1 = i, int(self.func(i/ki)*kj)
                y1 = 300 - y1
                paint.drawLine(x0, y0, x1, y1)
                x0, y0 = x1, y1
        else:
            if self.func(0) - 0.0 < 0.01:
                x0, y0 = 1, 1
                ki = 300.0/(self.time+1)
                kj = 300.0/(1.3)                
            else:
                x0, y0 = 1, self.func(0)
                ki = 300.0/(self.time+1)
                kj = 300.0/(self.func(0)*1.3)
            for i in range(1, self.width()):
                x1, y1 = i, int(self.func(i/ki)*kj)
                y1 = 300 - y1
                paint.drawLine(x0, y0, x1, y1)
                x0, y0 = x1, y1            
        paint.end()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.d = ProjectDialog()
        f = open("settings.txt", "rb")
        u = pickle.Unpickler(f)
        #Current project, list of projects with files and models
        self.settings = u.load()
        #Name of the current project
        self.currentProject = self.settings["current"]
        #File with XMl data
        self.fileNameXml = "projects/"+self.currentProject+".xml"
        #File with processed data (time only) 
        self.fileName = "projects/"+self.currentProject+".txt"
        #Computer of SRGM
        self.computer = None
        #List of relevant dta for slices
        self.programmers = []
        self.severity = []
        self.items = []
        self.errors = []
        f.close()
        self.LoadProject()
        QtCore.QObject.connect(self.ui.actionExit, 
                               QtCore.SIGNAL("triggered()"), self.Exit)
        QtCore.QObject.connect(self.ui.actionAbout, 
                               QtCore.SIGNAL("triggered()"), self.About)
        QtCore.QObject.connect(self.ui.actionNew_project, 
                               QtCore.SIGNAL("triggered()"), self.NewProject)
        QtCore.QObject.connect(self.ui.actionOpen_Project, 
                               QtCore.SIGNAL("triggered()"), self.OpenProject)
        QtCore.QObject.connect(self.ui.actionDelete_project, 
                               QtCore.SIGNAL("triggered()"), self.DeleteProject)
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
        QtCore.QObject.connect(self.d, 
                               QtCore.SIGNAL("accepted()"), self.CreateProject)
        self.ui.graph = Graph(self)
        self.ui.graph.show()
    
    def __del__(self):
        #Dump settings before exit
        f = open("settings.txt", "wb")
        p = pickle.Pickler(f)
        p.dump(self.settings)
        f.close()

    def NewProject(self):
        #Open New project dialog
        self.d.show()
        
    def OpenProject(self):
        #Call Open project dialog
        self.open = OpenDialog(self.settings["list"])
        QtCore.QObject.connect(self.open, QtCore.SIGNAL("accepted()"), self.OpenSelectedProject)
        self.open.show()
    
    def OpenSelectedProject(self):
        #Handler for OpenProject
        self.currentProject = self.open.combo.currentText()
        self.settings["current"] = self.currentProject
        self.LoadProject()
        
    def CreateProject(self):
        #Create new project: settings
        res = self.d.GetData()
        self.currentProject = res["name"]
        self.settings["list"].append(res) 
        self.settings["current"] = res["name"]
        self.fileNameXml = "projects/"+res["name"]+".xml"
        self.fileName = "projects/"+res["name"]+".txt"
        if self.fileNameXml != res["file"]:
            f = open(self.fileNameXml, "w")
            data = open(res["file"], "r")
            f.write(data.read())
            f.close()
            data.close()
        self.ParseXml()
        self.SetupData()
        self.LoadProject()
        
    def DeleteProject(self):
        #Delete project: settings
        for i in range(len(self.settings["list"])):
            if self.settings["list"][i]["name"] == self.currentProject:
                os.unlink(str( "projects/"+self.settings["list"][i]["name"]+".txt" ))
                self.settings["list"].pop(i)
        self.currentProject = self.settings["list"][0]["name"]
        self.settings["current"] = self.currentProject
        self.LoadProject()
             

    def LoadProject(self):
        #Common function: call XML parser, write all necessary data
        self.ui.label_3.setText("Project name: " + self.currentProject)
        self.fileName = "projects/"+self.currentProject+".txt"
        self.fileNameXml = "projects/"+self.currentProject+".xml"
        self.ui.comboBox.clear()
        tmp = self.settings["list"]
        for s in tmp:
            if s["name"] == self.currentProject:
                for s0 in s["models"]:
                    self.ui.comboBox.addItem(s0)
        self.ParseXml()
        self.startTime = 0
        self.endTime = 2**64
        self.SetupData()
        self.computer = SRGM(self.fileName)
        self.endTime = self.computer.totaltime
        #self.Compute()

    def ChangeModelsList(self):
        #Menu item handler
        self.dialog = QtGui.QDialog()
        self.label = QtGui.QLabel("Select the models: ")
        self.box = []
        models = ["Goel-Okumoto", "S-Shaped", "Jelinski-Moranda", "Littlewood-Verrall", "Logarithmic"]
        for i in range(0,5):
            self.box.append(QtGui.QCheckBox(models[i]))
        #self.dialog.setTitle("Select models")
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        for i in range(0,5):
            self.layout.addWidget(self.box[i])
        self.buttonOK = QtGui.QPushButton("OK")
        self.layout.addWidget(self.buttonOK)
        self.dialog.setLayout(self.layout)
        QtCore.QObject.connect(self.buttonOK, QtCore.SIGNAL("clicked()"), self.dialog, QtCore.SLOT("accept()"))
        QtCore.QObject.connect(self.dialog, QtCore.SIGNAL("accepted()"), self.ChangeModels)
        self.dialog.show()
    
    def ChangeModels(self):
        self.ui.comboBox.clear()
        lst = []
        for i in range(0, 5):
            if self.box[i].isChecked():
                lst.append(self.box[i].text())
        tmp = self.settings["list"]
        for s in tmp:
            if s["name"] == self.currentProject:
                s["models"] = lst
                for s0 in s["models"]:
                    self.ui.comboBox.addItem(s0)     

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
        self.SetupData()
        self.computer = SRGM(self.fileName)
        
    def SetupData(self):
        #Here the slice is done
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
        self.computer = SRGM(self.fileName)

    def BatchAddData(self):
        #Add a pack of errors
        def compare(a,b):
            if a["time"] > b["time"]:
                return 1
            elif a["time"] < b["time"]:
                return -1
            else:
                return 0
        fileName = QtGui.QFileDialog.getOpenFileName()
        if fileName == "":
            return
        tmp = self.fileNameXml
        self.fileNameXml = fileName
        self.ParseXml()
        self.fileNameXml = tmp
        self.errors.sort(cmp = compare)
        self.SetupData()
        self.DumpXml()
        self.computer = SRGM(self.fileName)

    def LoadNewXML(self):
        #Loads new data, overrides current
        fileName = QtGui.QFileDialog.getOpenFileName()
        if fileName == "":
            return
        f = open(fileName, "r")
        s = f.read()
        f.close()
        f = open(self.fileNameXml, "w")
        f.write(s)
        f.close()
        self.ParseXml()
        self.SetupData()
        self.computer = SRGM(self.fileName)
        
    def ParseXml(self):
        name = self.fileNameXml
        q = open(name, "r")
        dom = xml.dom.minidom.parse(q)
        dom.normalize()
        self.errors = []
        for node in dom.childNodes:
            if node.tagName == "errors":
                for error in node.childNodes:
                    currentError = {}
                    for attr in error.childNodes:
                        if attr.nodeName == "time":
                            for k in attr.childNodes:
                                currentError["time"] = int(k.nodeValue)
                        elif attr.nodeName == "programmer":
                            for k in attr.childNodes:
                                currentError["programmer"] = int(k.nodeValue)
                        elif attr.nodeName == "severity":
                            for k in attr.childNodes:
                                currentError["severity"] = int(k.nodeValue)
                        elif attr.nodeName == "item":
                            for k in attr.childNodes:
                                currentError["item"] = int(k.nodeValue)   
                    if currentError != {}:
                        self.errors.append(currentError)                         
        q.close()
        
    def DumpXml(self):
        pass
        dom = xml.dom.minidom.Document()
        root = dom.createElement("errors")
        dom.appendChild(root)
        for s in self.errors:
            node = dom.createElement("error")
            time = dom.createElement("time")
            time.appendChild(dom.createTextNode(str(s["time"])))
            programmer = dom.createElement("programmer")
            programmer.appendChild(dom.createTextNode(str(s["programmer"])))
            severity = dom.createElement("severity")
            severity.appendChild(dom.createTextNode(str(s["severity"])))
            item = dom.createElement("item")
            item.appendChild(dom.createTextNode(str(s["item"])))
            node.appendChild(time)
            node.appendChild(programmer)
            node.appendChild(severity)
            node.appendChild(item)
            root.appendChild(node)
        f = open(self.fileNameXml, "w")
        dom.writexml(f)
        f.close()
        
    def Compute(self):
        #Calls computing functions and displays results
        model = self.ui.comboBox.currentText()
        a = -1
        b = -1
        a0 = -1
        a1 = -1
        if model == "Goel-Okumoto":
            self.computer = GoelOkumoto(self.fileName)
            a, p, b, a0, a1 = self.computer.Compute()
            if a != -2:
                f = lambda x: a*(1-math.exp(-p*x))
                f2 = lambda x: a*p*math.exp(-p*x)
                if self.ui.comboBox_2.currentIndex() == 0:
                    self.ui.graph.func = f
                else:
                    self.ui.graph.func = f2
                self.ui.graph.meanFunc = f
                self.ui.graph.intensity = f2
                self.ui.graph.time = self.computer.totaltime
                self.ui.graph.number = self.computer.total
                self.ui.graph.update()
                self.ui.label_13.setText(str(self.computer.total+3))
                self.ui.label_14.setText(str(self.computer.totaltime+1))
                week = f(self.computer.totaltime+7)
                month = f(self.computer.totaltime+30)
                year = f(self.computer.totaltime+365)
                #self.ui.comboBox_2.setCurrentIndex(0)
        elif model == "S-Shaped":
            self.computer = SShaped(self.fileName)
            a, p, b = self.computer.Compute()
            f = lambda x: a*(1-(1+p)*math.exp(-p*x))
            f2 = lambda x: a*p*p*x*math.exp(-p*x)
            if self.ui.comboBox_2.currentIndex() == 0:
                self.ui.graph.func = f
            else:
                self.ui.graph.func = f2
            self.ui.graph.meanFunc = f
            self.ui.graph.intensity = f2
            self.ui.graph.time = self.computer.totaltime
            self.ui.graph.number = self.computer.total
            self.ui.graph.update()
            self.ui.label_13.setText(str(self.computer.total+3))
            self.ui.label_14.setText(str(self.computer.totaltime+1))
            week = f(self.computer.totaltime+7)
            month = f(self.computer.totaltime+30)
            year = f(self.computer.totaltime+365)
            #self.ui.comboBox_2.setCurrentIndex(0)
        elif model == "Jelinski-Moranda":
            self.computer = JelinskiMoranda(self.fileName)
            a, p, b = self.computer.Compute()
            f = lambda x: a*(1-math.exp(-p*int(x)))
            f2 = lambda x: a*p*math.exp(-p*int(x))
            if self.ui.comboBox_2.currentIndex() == 0:
                self.ui.graph.func = f
            else:
                self.ui.graph.func = f2
            self.ui.graph.meanFunc = f
            self.ui.graph.intensity = f2
            self.ui.graph.time = self.computer.totaltime
            self.ui.graph.number = self.computer.total
            self.ui.graph.update()
            week = f(self.computer.totaltime+7)
            month = f(self.computer.totaltime+30)
            year = f(self.computer.totaltime+365)
            #self.ui.comboBox_2.setCurrentIndex(0)
        elif model == "Littlewood-Verrall":
            a = -1
            self.computer = LittlewoodVerrall(self.fileName)
            a, b, p = self.computer.Compute()
            f = lambda x: (p[0]-1)/(4*p[2]*(p[0]-1)) * math.sqrt(2*p[2]*(p[0]-1)*x + p[1]**2)
            f2 = lambda x: (p[0]-1)/math.sqrt(p[1]**2+2*p[2]*x*(p[0]-1))
            if self.ui.comboBox_2.currentIndex() == 0:
                self.ui.graph.func = f
            else:
                self.ui.graph.func = f2
            self.ui.graph.meanFunc = f
            self.ui.graph.intensity = f2
            self.ui.graph.time = self.computer.totaltime
            self.ui.graph.number = self.computer.total
            self.ui.graph.update()
            self.ui.label_13.setText(str(self.computer.total+3))
            self.ui.label_14.setText(str(self.computer.totaltime+1))
            week = f(self.computer.totaltime+7)
            month = f(self.computer.totaltime+30)
            year = f(self.computer.totaltime+365)
            #self.ui.comboBox_2.setCurrentIndex(0)
        elif model == "Logarithmic":
            self.computer = Logarithmic(self.fileName)
            b0, b1, b = self.computer.Compute()
            a = -1
            f = lambda x: b0*math.log(x*b1 + 1)
            f2 = lambda x: b0*b1 / (b1*x + 1)
            if self.ui.comboBox_2.currentIndex() == 0:
                self.ui.graph.func = f
            else:
                self.ui.graph.func = f2
            self.ui.graph.meanFunc = f
            self.ui.graph.intensity = f2
            self.ui.graph.time = self.computer.totaltime
            self.ui.graph.number = self.computer.total
            self.ui.graph.update()
            self.ui.label_13.setText(str(self.computer.total+3))
            self.ui.label_14.setText(str(self.computer.totaltime+1))
            week = f(self.computer.totaltime+7)
            month = f(self.computer.totaltime+30)
            year = f(self.computer.totaltime+365)
            #self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.label_18.setText(str(self.computer.total))
        self.ui.label_22.setText(str(self.computer.totaltime))
        if a == -1:
            self.ui.label_2.setText("Undefined")
        elif a == -2:
            self.ui.label_2.setText("Diverges")
        else:
            self.ui.label_2.setText(str(a)[:8])
            self.ui.label_16.setText(str(month)[:7])
            self.ui.label_20.setText(str(month - self.computer.total)[:7])
            self.ui.label_24.setText(str(year)[:7])
            self.ui.label_26.setText(str(year - self.computer.total)[:7])
            self.ui.label_28.setText(str(week)[:7])
            self.ui.label_30.setText(str(week - self.computer.total)[:7])
        if b == -1:
            self.ui.label_5.setText("Undefined")
        elif b == -2:
            self.ui.label_5.setText("Diverges")      
        else:
            self.ui.label_5.setText(str(b)[:8])
            self.ui.label_16.setText(str(month)[:7])
            self.ui.label_20.setText(str(month - self.computer.total)[:7])
            self.ui.label_24.setText(str(year)[:7])
            self.ui.label_26.setText(str(year - self.computer.total)[:7])
            self.ui.label_28.setText(str(week)[:7])
            self.ui.label_30.setText(str(week - self.computer.total)[:7])
        if a0 == -1:
            self.ui.label_7.setText("Undefined")
        elif a0 == -2:
            self.ui.label_7.setText("Diverges")
        else:
            self.ui.label_7.setText(str(a0)[:7])
        if a1 == -1:
            self.ui.label_9.setText("Undefined")
        elif a1 == -2:
            self.ui.label_9.setText("Diverges")
        else:
            self.ui.label_9.setText(str(a1)[:7])
     
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