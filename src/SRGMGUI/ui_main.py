# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Fri Apr 22 21:44:57 2011
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
        MainWindow.resize(820, 453)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 22, 820, 410))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 30, 221, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 90, 331, 271))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.estimate = QtGui.QLabel(self.groupBox)
        self.estimate.setGeometry(QtCore.QRect(180, 20, 101, 16))
        self.estimate.setObjectName(_fromUtf8("estimate"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 181, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.mttf = QtGui.QLabel(self.groupBox)
        self.mttf.setGeometry(QtCore.QRect(180, 40, 71, 20))
        self.mttf.setObjectName(_fromUtf8("mttf"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.conf1 = QtGui.QLabel(self.groupBox)
        self.conf1.setGeometry(QtCore.QRect(140, 60, 51, 16))
        self.conf1.setObjectName(_fromUtf8("conf1"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(200, 60, 16, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.conf2 = QtGui.QLabel(self.groupBox)
        self.conf2.setGeometry(QtCore.QRect(220, 60, 61, 16))
        self.conf2.setObjectName(_fromUtf8("conf2"))
        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(10, 160, 171, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.afterMonth = QtGui.QLabel(self.groupBox)
        self.afterMonth.setGeometry(QtCore.QRect(180, 160, 61, 16))
        self.afterMonth.setObjectName(_fromUtf8("afterMonth"))
        self.label_17 = QtGui.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(10, 80, 141, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.numberOfFaults = QtGui.QLabel(self.groupBox)
        self.numberOfFaults.setGeometry(QtCore.QRect(180, 80, 81, 16))
        self.numberOfFaults.setObjectName(_fromUtf8("numberOfFaults"))
        self.label_19 = QtGui.QLabel(self.groupBox)
        self.label_19.setGeometry(QtCore.QRect(10, 180, 131, 16))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.month = QtGui.QLabel(self.groupBox)
        self.month.setGeometry(QtCore.QRect(180, 180, 61, 16))
        self.month.setObjectName(_fromUtf8("month"))
        self.label_21 = QtGui.QLabel(self.groupBox)
        self.label_21.setGeometry(QtCore.QRect(10, 100, 121, 16))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.testingTime = QtGui.QLabel(self.groupBox)
        self.testingTime.setGeometry(QtCore.QRect(180, 100, 91, 16))
        self.testingTime.setObjectName(_fromUtf8("testingTime"))
        self.label_23 = QtGui.QLabel(self.groupBox)
        self.label_23.setGeometry(QtCore.QRect(10, 200, 161, 16))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.afterYear = QtGui.QLabel(self.groupBox)
        self.afterYear.setGeometry(QtCore.QRect(180, 200, 61, 16))
        self.afterYear.setObjectName(_fromUtf8("afterYear"))
        self.label_25 = QtGui.QLabel(self.groupBox)
        self.label_25.setGeometry(QtCore.QRect(10, 220, 151, 16))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.year = QtGui.QLabel(self.groupBox)
        self.year.setGeometry(QtCore.QRect(180, 220, 61, 16))
        self.year.setObjectName(_fromUtf8("year"))
        self.label_27 = QtGui.QLabel(self.groupBox)
        self.label_27.setGeometry(QtCore.QRect(10, 120, 161, 16))
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.afterWeek = QtGui.QLabel(self.groupBox)
        self.afterWeek.setGeometry(QtCore.QRect(180, 120, 131, 16))
        self.afterWeek.setObjectName(_fromUtf8("afterWeek"))
        self.label_29 = QtGui.QLabel(self.groupBox)
        self.label_29.setGeometry(QtCore.QRect(10, 140, 151, 16))
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.week = QtGui.QLabel(self.groupBox)
        self.week.setGeometry(QtCore.QRect(180, 140, 61, 16))
        self.week.setObjectName(_fromUtf8("week"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 30, 101, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.graph = Graph(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(440, 110, 300, 300))
        self.graph.setObjectName(_fromUtf8("graph"))
        self.label_11 = QtGui.QLabel(self.graph)
        self.label_11.setGeometry(QtCore.QRect(230, 260, 31, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(440, 80, 5, 311))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(390, 50, 81, 21))
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setWordWrap(False)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(430, 370, 16, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.graphY = QtGui.QLabel(self.centralwidget)
        self.graphY.setGeometry(QtCore.QRect(410, 80, 51, 16))
        self.graphY.setObjectName(_fromUtf8("graphY"))
        self.graphX = QtGui.QLabel(self.centralwidget)
        self.graphX.setGeometry(QtCore.QRect(760, 370, 41, 16))
        self.graphX.setObjectName(_fromUtf8("graphX"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(410, 360, 361, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0, 432, 820, 21))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionNew_Project = QtGui.QAction(MainWindow)
        self.actionNew_Project.setObjectName(_fromUtf8("actionNew_Project"))
        self.actionOpen_Project = QtGui.QAction(MainWindow)
        self.actionOpen_Project.setObjectName(_fromUtf8("actionOpen_Project"))
        self.actionSave_Project = QtGui.QAction(MainWindow)
        self.actionSave_Project.setObjectName(_fromUtf8("actionSave_Project"))
        self.actionSave_Project_As = QtGui.QAction(MainWindow)
        self.actionSave_Project_As.setObjectName(_fromUtf8("actionSave_Project_As"))
        self.actionChange_models_list = QtGui.QAction(MainWindow)
        self.actionChange_models_list.setObjectName(_fromUtf8("actionChange_models_list"))
        self.actionLoad_new_XML_file = QtGui.QAction(MainWindow)
        self.actionLoad_new_XML_file.setObjectName(_fromUtf8("actionLoad_new_XML_file"))
        self.actionAdd_data_to_current_project = QtGui.QAction(MainWindow)
        self.actionAdd_data_to_current_project.setObjectName(_fromUtf8("actionAdd_data_to_current_project"))
        self.actionSetup_data_selection = QtGui.QAction(MainWindow)
        self.actionSetup_data_selection.setObjectName(_fromUtf8("actionSetup_data_selection"))
        self.actionBatch_data_load = QtGui.QAction(MainWindow)
        self.actionBatch_data_load.setObjectName(_fromUtf8("actionBatch_data_load"))
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addAction(self.actionSave_Project_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionChange_models_list)
        self.menuEdit.addAction(self.actionLoad_new_XML_file)
        self.menuEdit.addAction(self.actionSetup_data_selection)
        self.menuEdit.addAction(self.actionAdd_data_to_current_project)
        self.menuEdit.addAction(self.actionBatch_data_load)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.Exit)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.About)
        QtCore.QObject.connect(self.actionNew_Project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.NewProject)
        QtCore.QObject.connect(self.actionOpen_Project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.OpenProject)
        QtCore.QObject.connect(self.actionSave_Project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SaveProject)
        QtCore.QObject.connect(self.actionSave_Project_As, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SaveProjectAs)
        QtCore.QObject.connect(self.actionAdd_data_to_current_project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.AddData)
        QtCore.QObject.connect(self.actionBatch_data_load, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.BatchAddData)
        QtCore.QObject.connect(self.actionChange_models_list, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ChangeModelsList)
        QtCore.QObject.connect(self.actionLoad_new_XML_file, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.LoadNewXml)
        QtCore.QObject.connect(self.actionSetup_data_selection, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SelectData)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.Compute)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Software Reliability Growth Models Computer", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.estimate.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Total number of faults estimate:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Mean time to fault:", None, QtGui.QApplication.UnicodeUTF8))
        self.mttf.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Confidence interval:", None, QtGui.QApplication.UnicodeUTF8))
        self.conf1.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.conf2.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("MainWindow", "Errors after one month estimate:", None, QtGui.QApplication.UnicodeUTF8))
        self.afterMonth.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "Current number of faults:", None, QtGui.QApplication.UnicodeUTF8))
        self.numberOfFaults.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("MainWindow", "Errors during next month:", None, QtGui.QApplication.UnicodeUTF8))
        self.month.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("MainWindow", "Current testing time:", None, QtGui.QApplication.UnicodeUTF8))
        self.testingTime.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("MainWindow", "Errors after one year estimate:", None, QtGui.QApplication.UnicodeUTF8))
        self.afterYear.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("MainWindow", "Errors during next year:", None, QtGui.QApplication.UnicodeUTF8))
        self.year.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("MainWindow", "Errors after one week estimate:", None, QtGui.QApplication.UnicodeUTF8))
        self.afterWeek.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("MainWindow", "Errors during next week:", None, QtGui.QApplication.UnicodeUTF8))
        self.week.setText(QtGui.QApplication.translate("MainWindow", "Undefined", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Compute", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Number of faults", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.graphY.setText(QtGui.QApplication.translate("MainWindow", "n", None, QtGui.QApplication.UnicodeUTF8))
        self.graphX.setText(QtGui.QApplication.translate("MainWindow", "n", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_models_list.setText(QtGui.QApplication.translate("MainWindow", "Change models list", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_new_XML_file.setText(QtGui.QApplication.translate("MainWindow", "Load new XML file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_data_to_current_project.setText(QtGui.QApplication.translate("MainWindow", "Add data to current project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetup_data_selection.setText(QtGui.QApplication.translate("MainWindow", "Setup data selection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBatch_data_load.setText(QtGui.QApplication.translate("MainWindow", "Batch data load", None, QtGui.QApplication.UnicodeUTF8))

from Graph import Graph