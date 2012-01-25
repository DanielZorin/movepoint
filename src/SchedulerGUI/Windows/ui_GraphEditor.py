# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphEditor.ui'
#
# Created: Wed Jan 25 17:14:38 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GraphEditor(object):
    def setupUi(self, GraphEditor):
        GraphEditor.setObjectName(_fromUtf8("GraphEditor"))
        GraphEditor.resize(420, 332)
        GraphEditor.setStyleSheet(_fromUtf8("QWidget, QMenuBar::item {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #c5d8ef, stop: 1 #89a5c3);\n"
"}\n"
"\n"
"QLabel, QSlider {\n"
"    background-color: transparent;\n"
"}"))
        self.centralwidget = QtGui.QWidget(GraphEditor)
        self.centralwidget.setGeometry(QtCore.QRect(0, 59, 420, 252))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphArea = GraphCanvas(self.centralwidget)
        self.graphArea.setWidgetResizable(True)
        self.graphArea.setObjectName(_fromUtf8("graphArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget(self.graphArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 318, 230))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.graphArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.graphArea)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        GraphEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(GraphEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 420, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        GraphEditor.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(GraphEditor)
        self.statusbar.setGeometry(QtCore.QRect(0, 311, 420, 21))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        GraphEditor.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(GraphEditor)
        self.toolBar.setGeometry(QtCore.QRect(0, 22, 420, 37))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        GraphEditor.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSelect = QtGui.QAction(GraphEditor)
        self.actionSelect.setCheckable(True)
        self.actionSelect.setChecked(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/select.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon)
        self.actionSelect.setObjectName(_fromUtf8("actionSelect"))
        self.actionVertex = QtGui.QAction(GraphEditor)
        self.actionVertex.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/vertex.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVertex.setIcon(icon1)
        self.actionVertex.setObjectName(_fromUtf8("actionVertex"))
        self.actionEdge = QtGui.QAction(GraphEditor)
        self.actionEdge.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/edge.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdge.setIcon(icon2)
        self.actionEdge.setObjectName(_fromUtf8("actionEdge"))
        self.actionNew_System = QtGui.QAction(GraphEditor)
        self.actionNew_System.setObjectName(_fromUtf8("actionNew_System"))
        self.actionOpen_System = QtGui.QAction(GraphEditor)
        self.actionOpen_System.setObjectName(_fromUtf8("actionOpen_System"))
        self.actionSave_System = QtGui.QAction(GraphEditor)
        self.actionSave_System.setObjectName(_fromUtf8("actionSave_System"))
        self.menuFile.addAction(self.actionNew_System)
        self.menuFile.addAction(self.actionOpen_System)
        self.menuFile.addAction(self.actionSave_System)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionSelect)
        self.toolBar.addAction(self.actionVertex)
        self.toolBar.addAction(self.actionEdge)

        self.retranslateUi(GraphEditor)
        QtCore.QObject.connect(self.actionSelect, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.toggleSelect)
        QtCore.QObject.connect(self.actionVertex, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.toggleVertex)
        QtCore.QObject.connect(self.actionEdge, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.toggleEdge)
        QtCore.QMetaObject.connectSlotsByName(GraphEditor)

    def retranslateUi(self, GraphEditor):
        GraphEditor.setWindowTitle(QtGui.QApplication.translate("GraphEditor", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("GraphEditor", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("GraphEditor", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("GraphEditor", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect.setText(QtGui.QApplication.translate("GraphEditor", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.actionVertex.setText(QtGui.QApplication.translate("GraphEditor", "Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdge.setText(QtGui.QApplication.translate("GraphEditor", "Edge", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_System.setText(QtGui.QApplication.translate("GraphEditor", "New System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_System.setText(QtGui.QApplication.translate("GraphEditor", "Open System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_System.setText(QtGui.QApplication.translate("GraphEditor", "Save System", None, QtGui.QApplication.UnicodeUTF8))

from SchedulerGUI.GraphCanvas import GraphCanvas
from . import resources_rc
