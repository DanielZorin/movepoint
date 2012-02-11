# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewProjectDialog.ui'
#
# Created: Sat Feb 11 16:15:17 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        NewProjectDialog.setObjectName(_fromUtf8("NewProjectDialog"))
        NewProjectDialog.resize(318, 201)
        NewProjectDialog.setStyleSheet(_fromUtf8("QWidget, QMenuBar::item {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #c5d8ef, stop: 1 #89a5c3);\n"
"}\n"
"\n"
"QLabel, QSlider {\n"
"    background-color: transparent;\n"
"}a"))
        NewProjectDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout_2 = QtGui.QVBoxLayout(NewProjectDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(NewProjectDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditSystem = QtGui.QLineEdit(NewProjectDialog)
        self.lineEditSystem.setEnabled(True)
        self.lineEditSystem.setReadOnly(True)
        self.lineEditSystem.setObjectName(_fromUtf8("lineEditSystem"))
        self.horizontalLayout_2.addWidget(self.lineEditSystem)
        self.OpenSystem = QtGui.QPushButton(NewProjectDialog)
        self.OpenSystem.setObjectName(_fromUtf8("OpenSystem"))
        self.horizontalLayout_2.addWidget(self.OpenSystem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(NewProjectDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lineEditConfig = QtGui.QLineEdit(NewProjectDialog)
        self.lineEditConfig.setEnabled(True)
        self.lineEditConfig.setReadOnly(True)
        self.lineEditConfig.setObjectName(_fromUtf8("lineEditConfig"))
        self.horizontalLayout_3.addWidget(self.lineEditConfig)
        self.OpenConfig = QtGui.QPushButton(NewProjectDialog)
        self.OpenConfig.setObjectName(_fromUtf8("OpenConfig"))
        self.horizontalLayout_3.addWidget(self.OpenConfig)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_3 = QtGui.QLabel(NewProjectDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.ProjectName = QtGui.QLineEdit(NewProjectDialog)
        self.ProjectName.setWindowModality(QtCore.Qt.NonModal)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ProjectName.sizePolicy().hasHeightForWidth())
        self.ProjectName.setSizePolicy(sizePolicy)
        self.ProjectName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ProjectName.setObjectName(_fromUtf8("ProjectName"))
        self.horizontalLayout_4.addWidget(self.ProjectName)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.OK = QtGui.QPushButton(NewProjectDialog)
        self.OK.setObjectName(_fromUtf8("OK"))
        self.horizontalLayout.addWidget(self.OK)
        self.Cancel = QtGui.QPushButton(NewProjectDialog)
        self.Cancel.setObjectName(_fromUtf8("Cancel"))
        self.horizontalLayout.addWidget(self.Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(NewProjectDialog)
        QtCore.QObject.connect(self.OpenSystem, QtCore.SIGNAL(_fromUtf8("clicked()")), NewProjectDialog.LoadSystem)
        QtCore.QObject.connect(self.OpenConfig, QtCore.SIGNAL(_fromUtf8("clicked()")), NewProjectDialog.LoadConfig)
        QtCore.QObject.connect(self.OK, QtCore.SIGNAL(_fromUtf8("clicked()")), NewProjectDialog.accept)
        QtCore.QObject.connect(self.Cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProjectDialog)

    def retranslateUi(self, NewProjectDialog):
        NewProjectDialog.setWindowTitle(QtGui.QApplication.translate("NewProjectDialog", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewProjectDialog", "Load system:", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenSystem.setText(QtGui.QApplication.translate("NewProjectDialog", "Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewProjectDialog", "Load config file:", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenConfig.setText(QtGui.QApplication.translate("NewProjectDialog", "Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewProjectDialog", "Project name:", None, QtGui.QApplication.UnicodeUTF8))
        self.OK.setText(QtGui.QApplication.translate("NewProjectDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.Cancel.setText(QtGui.QApplication.translate("NewProjectDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

