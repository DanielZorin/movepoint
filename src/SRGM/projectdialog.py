from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

#Pages of the wizard "Create Project"
class FirstPage(QWizardPage):
    def __init__(self):
        QWizardPage.__init__(self)
        self.label = QLabel("Enter project name: ")
        self.lineedit = QLineEdit()
        self.setTitle("First step")
        self.registerField("Enter project name: *", self.lineedit)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineedit)
        self.setLayout(self.layout)
        
        
class SecondPage(QWizardPage):
    def __init__(self):
        QWizardPage.__init__(self)
        self.label = QLabel("Select file of data: ")
        self.button = QPushButton("Select...")
        self.lineedit = QLineEdit()
        self.lineedit.setReadOnly(True)
        self.w = QWidget()
        fileSelect = QHBoxLayout()
        fileSelect.addWidget(self.lineedit)
        fileSelect.addWidget(self.button)
        self.w.setLayout(fileSelect)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("clicked()"), self.GetFile)
        self.setTitle("Second step")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.w)
        self.setLayout(self.layout)
        self.registerField("File*", self.lineedit)
    def GetFile(self):
        name = QFileDialog.getOpenFileName()
        self.lineedit.setText(name)
        self.ProcessData()
    def ProcessData(self):
        pass
        
  
class ThirdPage(QWizardPage):  
    def __init__(self):
        QWizardPage.__init__(self)
        self.label = QLabel("Select the models: ")
        self.box = []
        models = ["Goel-Okumoto", "S-Shaped", "Jelinski-Moranda", "Littlewood-Verrall", "Logarithmic"]
        for i in range(0,5):
            self.box.append(QCheckBox(models[i]))
        self.setTitle("Third step")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        for i in range(0,5):
            self.layout.addWidget(self.box[i])
        self.setLayout(self.layout)
      
#Calls the wizard                
class ProjectDialog(QWizard):
    def __init__(self):
        QWizard.__init__(self)
        self.firstpage = FirstPage()
        self.secondpage = SecondPage()
        self.thirdpage = ThirdPage()
        self.addPage(self.firstpage)
        self.addPage(self.secondpage)
        self.addPage(self.thirdpage)
    def GetData(self):
        lst = []
        for i in range(0, 5):
            if self.thirdpage.box[i].isChecked():
                lst.append(self.thirdpage.box[i].text())
        return {"name": self.firstpage.lineedit.text(), 
                "file": self.secondpage.lineedit.text(),
                "models": lst}


#Open an existing project        
class OpenDialog(QDialog):
    def __init__(self, list):
        QDialog.__init__(self)
        self.label = QLabel("Select project: ")
        self.combo = QComboBox()
        self.button = QDialogButtonBox(QDialogButtonBox.Ok)
        for s in list:
            self.combo.addItem(s["name"])
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("accepted()"), self.accept)

#Set data slice        
class SettingsDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.label1 = QLabel("Enter programmer ids")
        self.label2 = QLabel("Enter severity")
        self.label3 = QLabel("Enter item ids")
        self.label4 = QLabel("Time period")
        self.label5 = QLabel(" to ")
        self.lineedit1 = QLineEdit()
        self.lineedit2 = QLineEdit()
        self.lineedit3 = QLineEdit()
        self.lineedit4 = QLineEdit()
        self.lineedit5 = QLineEdit()
        self.button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.layout = QGridLayout()
        self.layout.addWidget(self.label1, 1, 1, 1, 3)
        self.layout.addWidget(self.lineedit1, 2, 1, 1, 3)
        self.layout.addWidget(self.label2, 3, 1, 1, 3)
        self.layout.addWidget(self.lineedit2, 4, 1, 1, 3)
        self.layout.addWidget(self.label3, 5, 1, 1, 3)
        self.layout.addWidget(self.lineedit3, 6, 1, 1, 3)
        self.layout.addWidget(self.label4, 7, 1, 1, 3)
        self.layout.addWidget(self.lineedit4, 8, 1)
        self.layout.addWidget(self.label5, 8, 2)
        self.layout.addWidget(self.lineedit5, 8, 3)
        self.layout.addWidget(self.button, 9, 1, 1, 3)
        self.setLayout(self.layout)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("accepted()"), self.accept)