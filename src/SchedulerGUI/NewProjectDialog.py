'''
Created on 15.12.2010

@author: juan
'''

from PyQt4.QtGui import QDialog, QFileDialog
import os
from SchedulerGUI.Windows.ui_NewProjectDialog import Ui_NewProjectDialog

     
class NewProjectDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_NewProjectDialog()
        self.ui.setupUi(self)
        
    def LoadSystem(self):
        name = QFileDialog.getOpenFileName()
        self.ui.lineEditSystem.setText(name)
        print(self.ui.ProjectName.text())
        if self.ui.ProjectName.text() == "":
            ff = os.path.basename(name)
            self.ui.ProjectName.setText(ff[:ff.find(".")])
        
    def GetSystem(self):
        return self.ui.lineEditSystem.text()
    
    def GetName(self):
        return self.ui.ProjectName.text()