# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VertexDialog.ui'
#
# Created: Sun Feb 12 15:15:54 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VertexDialog(object):
    def setupUi(self, VertexDialog):
        VertexDialog.setObjectName(_fromUtf8("VertexDialog"))
        VertexDialog.resize(231, 258)
        VertexDialog.setStyleSheet(_fromUtf8("QWidget, QMenuBar::item, QHeaderView::section {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #c5d8ef, stop: 1 #89a5c3);\n"
"}\n"
"\n"
"QLabel, QSlider {\n"
"    background-color: transparent;\n"
"}"))
        VertexDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout_2 = QtGui.QVBoxLayout(VertexDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.namelabel = QtGui.QLabel(VertexDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.namelabel.sizePolicy().hasHeightForWidth())
        self.namelabel.setSizePolicy(sizePolicy)
        self.namelabel.setObjectName(_fromUtf8("namelabel"))
        self.verticalLayout.addWidget(self.namelabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.name = QtGui.QLineEdit(VertexDialog)
        self.name.setEnabled(True)
        self.name.setReadOnly(False)
        self.name.setObjectName(_fromUtf8("name"))
        self.horizontalLayout_2.addWidget(self.name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.timelabel = QtGui.QLabel(VertexDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timelabel.sizePolicy().hasHeightForWidth())
        self.timelabel.setSizePolicy(sizePolicy)
        self.timelabel.setObjectName(_fromUtf8("timelabel"))
        self.verticalLayout.addWidget(self.timelabel)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.time = QtGui.QLineEdit(VertexDialog)
        self.time.setEnabled(True)
        self.time.setReadOnly(False)
        self.time.setObjectName(_fromUtf8("time"))
        self.horizontalLayout_3.addWidget(self.time)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(VertexDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.add = QtGui.QPushButton(VertexDialog)
        self.add.setMaximumSize(QtCore.QSize(16, 16777215))
        self.add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add.setIcon(icon)
        self.add.setFlat(True)
        self.add.setObjectName(_fromUtf8("add"))
        self.horizontalLayout_5.addWidget(self.add)
        self.remove = QtGui.QPushButton(VertexDialog)
        self.remove.setMaximumSize(QtCore.QSize(16, 16777215))
        self.remove.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove.setIcon(icon1)
        self.remove.setFlat(True)
        self.remove.setObjectName(_fromUtf8("remove"))
        self.horizontalLayout_5.addWidget(self.remove)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.versions = QtGui.QTableWidget(VertexDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versions.sizePolicy().hasHeightForWidth())
        self.versions.setSizePolicy(sizePolicy)
        self.versions.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.versions.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.versions.setShowGrid(True)
        self.versions.setColumnCount(2)
        self.versions.setObjectName(_fromUtf8("versions"))
        self.versions.setColumnCount(2)
        self.versions.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.versions.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.versions.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_4.addWidget(self.versions)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.OK = QtGui.QPushButton(VertexDialog)
        self.OK.setObjectName(_fromUtf8("OK"))
        self.horizontalLayout.addWidget(self.OK)
        self.Cancel = QtGui.QPushButton(VertexDialog)
        self.Cancel.setObjectName(_fromUtf8("Cancel"))
        self.horizontalLayout.addWidget(self.Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(VertexDialog)
        QtCore.QObject.connect(self.OK, QtCore.SIGNAL(_fromUtf8("clicked()")), VertexDialog.accept)
        QtCore.QObject.connect(self.Cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), VertexDialog.reject)
        QtCore.QObject.connect(self.add, QtCore.SIGNAL(_fromUtf8("clicked()")), VertexDialog.AddVersion)
        QtCore.QObject.connect(self.remove, QtCore.SIGNAL(_fromUtf8("clicked()")), VertexDialog.RemoveVersion)
        QtCore.QMetaObject.connectSlotsByName(VertexDialog)

    def retranslateUi(self, VertexDialog):
        VertexDialog.setWindowTitle(QtGui.QApplication.translate("VertexDialog", "Edit Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.namelabel.setText(QtGui.QApplication.translate("VertexDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.timelabel.setText(QtGui.QApplication.translate("VertexDialog", "Execution Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VertexDialog", "Versions:", None, QtGui.QApplication.UnicodeUTF8))
        self.versions.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("VertexDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.versions.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("VertexDialog", "Reliability", None, QtGui.QApplication.UnicodeUTF8))
        self.OK.setText(QtGui.QApplication.translate("VertexDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.Cancel.setText(QtGui.QApplication.translate("VertexDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
