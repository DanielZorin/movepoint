'''
Created on 09.01.2011

@author: juan
'''
from PyQt4.QtGui import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QScrollArea, QWidget, QPushButton, QIntValidator, QDoubleValidator
from PyQt4.QtCore import Qt, QObject, SIGNAL
     
class SettingsDialog(QDialog):
    
    data = {}
    ui = {}
    
    def __init__(self, config):
        QDialog.__init__(self)
        self.setWindowTitle("Method Settings")
        self.data = config             
        self.ui = {}
        self.area = QScrollArea()
        self.widget = QWidget()
        l = self._parseDict(self.data, self.ui)
        self.widget.setLayout(l)
        self.area.setWidget(self.widget)
        self.area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area)
        self.buttons = QHBoxLayout()
        self.ok = QPushButton("OK")
        self.cancel = QPushButton("Cancel")
        self.buttons.addWidget(self.ok)
        self.buttons.addWidget(self.cancel)
        self.layout.addLayout(self.buttons)
        self.setLayout(self.layout)
        QObject.connect(self.ok, SIGNAL("clicked()"), self.OK)
        QObject.connect(self.cancel, SIGNAL("clicked()"), self.Cancel)
        
    def _parseDict(self, config, ui):
        l = QVBoxLayout()
        #Parse simple members
        lst = sorted(list(config.keys()))
        for k in lst:
            t = type(config[k])
            if t == type(int()):
                hbox = QHBoxLayout()
                label = QLabel(k)
                edit = QLineEdit(str(config[k]))
                val = QIntValidator(self)
                edit.setValidator(val)
                hbox.addWidget(label)
                hbox.addWidget(edit)
                l.addLayout(hbox)
                ui[k] = (edit, label, hbox, val)
            elif t == type(float()):
                hbox = QHBoxLayout()
                label = QLabel(k)
                edit = QLineEdit(str(config[k]))
                val = QDoubleValidator(self)
                edit.setValidator(val)
                hbox.addWidget(label)
                hbox.addWidget(edit)
                l.addLayout(hbox)
                ui[k] = (edit, label, hbox, val)
        # Parse composite members
        for k in lst:
            t = type(config[k])
            if t == type(dict()):
                gbox = QGroupBox()
                gbox.setTitle(k)
                ui[k] = {"gbox":gbox}
                l2 = self._parseDict(config[k], ui[k])
                ui[k]["layout"] = l2
                gbox.setLayout(l2)
                l.addWidget(gbox)
        return l
    
    def _getData(self, config, ui):
        res = {}
        for k in config.keys():
            t = type(config[k])
            if t == type(int()):
                res[k] = int(ui[k][0].text())
            elif t == type(float()):
                res[k] = float(ui[k][0].text())
            elif t == type(dict()):
                res[k] = self._getData(config[k], ui[k])
        return res
    
    def OK(self):
        res = self._getData(self.data, self.ui)
        # We merge the dictionaries because some settings are still immutable
        self.data.update(res)
        self.accept()
    
    def Cancel(self):
        self.reject()
