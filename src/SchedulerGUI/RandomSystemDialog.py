'''
Created on 09.01.2011

@author: juan
'''
from PyQt4.QtGui import QDialog
from SchedulerGUI.Windows.ui_RandomSystemDialog import Ui_RandomSystemDialog

     
class RandomSystemDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_RandomSystemDialog()
        self.ui.setupUi(self)
        
    def GetResult(self):
        return {"n":int(self.ui.n.text()), 
                "t1":int(self.ui.t1.text()), 
                "t2":int(self.ui.t2.text()), 
                "v1":int(self.ui.v1.text()), 
                "v2":int(self.ui.v2.text()),
                "tdir":self.ui.tdir.currentIndex(),
                "rdir":self.ui.rdir.currentIndex()}