# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Thu Jan 12 17:32:23 2012
#      by: PyQt4 UI code generator 4.8.4
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
        MainWindow.resize(307, 327)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
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
"}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.editname = QtGui.QPushButton(self.centralwidget)
        self.editname.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page_edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.editname.setIcon(icon1)
        self.editname.setFlat(True)
        self.editname.setObjectName(_fromUtf8("editname"))
        self.horizontalLayout.addWidget(self.editname)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(20, 0))
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 3, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 4, 1, 1, 1)
        self.editprogram = QtGui.QPushButton(self.groupBox)
        self.editprogram.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/computer.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.editprogram.setIcon(icon2)
        self.editprogram.setIconSize(QtCore.QSize(32, 32))
        self.editprogram.setFlat(True)
        self.editprogram.setObjectName(_fromUtf8("editprogram"))
        self.gridLayout.addWidget(self.editprogram, 0, 2, 2, 1)
        self.edittime = QtGui.QPushButton(self.groupBox)
        self.edittime.setMaximumSize(QtCore.QSize(16, 16777215))
        self.edittime.setText(_fromUtf8(""))
        self.edittime.setIcon(icon1)
        self.edittime.setFlat(True)
        self.edittime.setObjectName(_fromUtf8("edittime"))
        self.gridLayout.addWidget(self.edittime, 2, 2, 1, 1)
        self.editrel = QtGui.QPushButton(self.groupBox)
        self.editrel.setMaximumSize(QtCore.QSize(16, 16777215))
        self.editrel.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page_edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editrel.setIcon(icon3)
        self.editrel.setFlat(True)
        self.editrel.setObjectName(_fromUtf8("editrel"))
        self.gridLayout.addWidget(self.editrel, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.runbutton = QtGui.QPushButton(self.centralwidget)
        self.runbutton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.runbutton.setIcon(icon4)
        self.runbutton.setIconSize(QtCore.QSize(24, 24))
        self.runbutton.setFlat(True)
        self.runbutton.setObjectName(_fromUtf8("runbutton"))
        self.horizontalLayout_2.addWidget(self.runbutton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.progress = QtGui.QProgressBar(self.centralwidget)
        self.progress.setProperty(_fromUtf8("value"), 0)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.verticalLayout_2.addWidget(self.progress)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 307, 21))
        self.menubar.setStyleSheet(_fromUtf8(""))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuMethod = QtGui.QMenu(self.menubar)
        self.menuMethod.setObjectName(_fromUtf8("menuMethod"))
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName(_fromUtf8("menuProject"))
        self.menuExport = QtGui.QMenu(self.menubar)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionNew_Project = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionNew_Project.setIcon(icon5)
        self.actionNew_Project.setObjectName(_fromUtf8("actionNew_Project"))
        self.actionOpen_Project = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionOpen_Project.setIcon(icon6)
        self.actionOpen_Project.setObjectName(_fromUtf8("actionOpen_Project"))
        self.actionSave_Project = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/cd.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionSave_Project.setIcon(icon7)
        self.actionSave_Project.setObjectName(_fromUtf8("actionSave_Project"))
        self.actionSave_Project_As = QtGui.QAction(MainWindow)
        self.actionSave_Project_As.setObjectName(_fromUtf8("actionSave_Project_As"))
        self.actionStart = QtGui.QAction(MainWindow)
        self.actionStart.setEnabled(True)
        self.actionStart.setIcon(icon4)
        self.actionStart.setObjectName(_fromUtf8("actionStart"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionContents = QtGui.QAction(MainWindow)
        self.actionContents.setObjectName(_fromUtf8("actionContents"))
        self.actionAbout_Scheduler = QtGui.QAction(MainWindow)
        self.actionAbout_Scheduler.setObjectName(_fromUtf8("actionAbout_Scheduler"))
        self.actionReset = QtGui.QAction(MainWindow)
        self.actionReset.setEnabled(True)
        self.actionReset.setObjectName(_fromUtf8("actionReset"))
        self.actionChange_name = QtGui.QAction(MainWindow)
        self.actionChange_name.setObjectName(_fromUtf8("actionChange_name"))
        self.actionLoad_New_System = QtGui.QAction(MainWindow)
        self.actionLoad_New_System.setObjectName(_fromUtf8("actionLoad_New_System"))
        self.actionLoad_New_Method = QtGui.QAction(MainWindow)
        self.actionLoad_New_Method.setObjectName(_fromUtf8("actionLoad_New_Method"))
        self.actionGenerate_Random_System = QtGui.QAction(MainWindow)
        self.actionGenerate_Random_System.setObjectName(_fromUtf8("actionGenerate_Random_System"))
        self.actionLanguage = QtGui.QAction(MainWindow)
        self.actionLanguage.setObjectName(_fromUtf8("actionLanguage"))
        self.actionChange_Limits = QtGui.QAction(MainWindow)
        self.actionChange_Limits.setObjectName(_fromUtf8("actionChange_Limits"))
        self.actionLaunch_Viewer = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/chart.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionLaunch_Viewer.setIcon(icon8)
        self.actionLaunch_Viewer.setObjectName(_fromUtf8("actionLaunch_Viewer"))
        self.actionTrace = QtGui.QAction(MainWindow)
        self.actionTrace.setObjectName(_fromUtf8("actionTrace"))
        self.actionResult = QtGui.QAction(MainWindow)
        self.actionResult.setObjectName(_fromUtf8("actionResult"))
        self.actionGenerate_Code = QtGui.QAction(MainWindow)
        self.actionGenerate_Code.setObjectName(_fromUtf8("actionGenerate_Code"))
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addAction(self.actionSave_Project_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuMethod.addAction(self.actionStart)
        self.menuMethod.addAction(self.actionReset)
        self.menuMethod.addAction(self.actionLoad_New_Method)
        self.menuMethod.addAction(self.actionSettings)
        self.menuMethod.addAction(self.actionLaunch_Viewer)
        self.menuWindow.addAction(self.actionLanguage)
        self.menuHelp.addAction(self.actionContents)
        self.menuHelp.addAction(self.actionAbout)
        self.menuProject.addAction(self.actionChange_name)
        self.menuProject.addAction(self.actionChange_Limits)
        self.menuProject.addAction(self.actionLoad_New_System)
        self.menuProject.addAction(self.actionGenerate_Random_System)
        self.menuExport.addAction(self.actionTrace)
        self.menuExport.addAction(self.actionResult)
        self.menuExport.addAction(self.actionGenerate_Code)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuMethod.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew_Project)
        self.toolBar.addAction(self.actionOpen_Project)
        self.toolBar.addAction(self.actionSave_Project)
        self.toolBar.addAction(self.actionLaunch_Viewer)
        self.toolBar.addAction(self.actionStart)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.Exit)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.About)
        QtCore.QObject.connect(self.actionNew_Project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.NewProject)
        QtCore.QObject.connect(self.actionOpen_Project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.OpenProject)
        QtCore.QObject.connect(self.actionSave_Project, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SaveProject)
        QtCore.QObject.connect(self.actionSave_Project_As, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SaveProjectAs)
        QtCore.QObject.connect(self.actionStart, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.Run)
        QtCore.QObject.connect(self.actionReset, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ResetSchedule)
        QtCore.QObject.connect(self.actionGenerate_Random_System, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.GenerateRandomSystem)
        QtCore.QObject.connect(self.actionLoad_New_System, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.LoadSystem)
        QtCore.QObject.connect(self.actionLoad_New_Method, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.LoadMethod)
        QtCore.QObject.connect(self.actionChange_name, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ChangeName)
        QtCore.QObject.connect(self.actionSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.Settings)
        QtCore.QObject.connect(self.actionLanguage, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ChangeLanguage)
        QtCore.QObject.connect(self.actionChange_Limits, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ChangeLimits)
        QtCore.QObject.connect(self.actionLaunch_Viewer, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.LaunchViewer)
        QtCore.QObject.connect(self.actionTrace, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ExportTrace)
        QtCore.QObject.connect(self.runbutton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionStart.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Scheduler GUI", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Project name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Program info", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Vertices", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Edges", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Deadline", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Reliability limit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Trace length", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Launch search", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMethod.setTitle(QtGui.QApplication.translate("MainWindow", "Method", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Window", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport.setTitle(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About Scheduler", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionContents.setText(QtGui.QApplication.translate("MainWindow", "Contents...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Scheduler.setText(QtGui.QApplication.translate("MainWindow", "About Scheduler", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset.setShortcut(QtGui.QApplication.translate("MainWindow", "F10", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_name.setText(QtGui.QApplication.translate("MainWindow", "Change Name...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_New_System.setText(QtGui.QApplication.translate("MainWindow", "Load New System...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_New_Method.setText(QtGui.QApplication.translate("MainWindow", "Load New Method...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Random_System.setText(QtGui.QApplication.translate("MainWindow", "Generate Random System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Random_System.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLanguage.setText(QtGui.QApplication.translate("MainWindow", "Language...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_Limits.setText(QtGui.QApplication.translate("MainWindow", "Change Limits...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLaunch_Viewer.setText(QtGui.QApplication.translate("MainWindow", "Launch Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTrace.setText(QtGui.QApplication.translate("MainWindow", "Trace...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResult.setText(QtGui.QApplication.translate("MainWindow", "Result...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Code.setText(QtGui.QApplication.translate("MainWindow", "Generate Code...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
