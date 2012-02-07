'''
Created on 18.01.2011

@author: juan
'''
from PyQt4.QtGui import QLabel, QDialog, QComboBox, QDialogButtonBox, QVBoxLayout
from PyQt4.QtCore import QObject, SIGNAL

class ComboBoxDialog(QDialog):
    def __init__(self, list, cur, title="Select one of the options below:"):
        QDialog.__init__(self)
        self.setWindowTitle(title)
        self.label = QLabel("Select language: ")
        self.combo = QComboBox()
        self.button = QDialogButtonBox(QDialogButtonBox.Ok)
        i = 0
        for s in list:
            self.combo.addItem(s)
            if s == cur:
                self.combo.setCurrentIndex(i)
            i += 1
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        QObject.connect(self.button, SIGNAL("accepted()"), self.accept)