# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowInitial.ui'
#
# Created: Sun Feb 12 16:48:57 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(352, 295)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/star.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(_fromUtf8("QWidget, QMenuBar::item {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #c5d8ef, stop: 1 #89a5c3);\n"
"}\n"
"\n"
"QLabel, QSlider {\n"
"    background-color: transparent;\n"
"}a"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 22, 352, 273))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.loadnew = QtGui.QPushButton(self.centralwidget)
        self.loadnew.setGeometry(QtCore.QRect(0, 20, 101, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadnew.setIcon(icon1)
        self.loadnew.setFlat(True)
        self.loadnew.setObjectName(_fromUtf8("loadnew"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 10, 121, 81))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.loadopen = QtGui.QPushButton(self.centralwidget)
        self.loadopen.setGeometry(QtCore.QRect(30, 50, 111, 31))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadopen.setIcon(icon2)
        self.loadopen.setFlat(True)
        self.loadopen.setObjectName(_fromUtf8("loadopen"))
        self.recent = QtGui.QListWidget(self.centralwidget)
        self.recent.setGeometry(QtCore.QRect(120, 100, 111, 151))
        self.recent.setStyleSheet(_fromUtf8("QListView {\n"
"border : 0px;\n"
"}"))
        self.recent.setObjectName(_fromUtf8("recent"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 352, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.loadnew, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.LoadNew)
        QtCore.QObject.connect(self.loadopen, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.LoadOpen)
        QtCore.QObject.connect(self.recent, QtCore.SIGNAL(_fromUtf8("itemPressed(QListWidgetItem*)")), MainWindow.LoadRecent)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Scheduler GUI", None, QtGui.QApplication.UnicodeUTF8))
        self.loadnew.setText(QtGui.QApplication.translate("MainWindow", "New Project...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Welcome to Scheduler GUI, a program for fast and reliable scheduling for multiprocessors!", None, QtGui.QApplication.UnicodeUTF8))
        self.loadopen.setText(QtGui.QApplication.translate("MainWindow", "Open Project...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
