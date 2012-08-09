
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(320, 430)
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
"}a"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 59, 320, 371))
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.projectname = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectname.sizePolicy().hasHeightForWidth())
        self.projectname.setSizePolicy(sizePolicy)
        self.projectname.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.projectname.setFont(font)
        self.projectname.setObjectName(_fromUtf8("projectname"))
        self.horizontalLayout.addWidget(self.projectname)
        self.editname = QtGui.QPushButton(self.centralwidget)
        self.editname.setMaximumSize(QtCore.QSize(16777215, 24))
        self.editname.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page_edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.editname.setIcon(icon1)
        self.editname.setFlat(True)
        self.editname.setObjectName(_fromUtf8("editname"))
        self.horizontalLayout.addWidget(self.editname)
        spacerItem = QtGui.QSpacerItem(40, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.vertices = QtGui.QLabel(self.groupBox)
        self.vertices.setObjectName(_fromUtf8("vertices"))
        self.gridLayout.addWidget(self.vertices, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.edges = QtGui.QLabel(self.groupBox)
        self.edges.setObjectName(_fromUtf8("edges"))
        self.gridLayout.addWidget(self.edges, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.tdir = QtGui.QLabel(self.groupBox)
        self.tdir.setMinimumSize(QtCore.QSize(24, 24))
        self.tdir.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tdir.setObjectName(_fromUtf8("tdir"))
        self.gridLayout.addWidget(self.tdir, 2, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.rdir = QtGui.QLabel(self.groupBox)
        self.rdir.setMinimumSize(QtCore.QSize(24, 24))
        self.rdir.setObjectName(_fromUtf8("rdir"))
        self.gridLayout.addWidget(self.rdir, 3, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.tracelen = QtGui.QLabel(self.groupBox)
        self.tracelen.setObjectName(_fromUtf8("tracelen"))
        self.gridLayout.addWidget(self.tracelen, 4, 1, 1, 1)
        self.editprogram = QtGui.QPushButton(self.groupBox)
        self.editprogram.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/graph.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
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
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.runbutton = QtGui.QPushButton(self.centralwidget)
        self.runbutton.setMaximumSize(QtCore.QSize(16777215, 32))
        self.runbutton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.runbutton.setIcon(icon4)
        self.runbutton.setIconSize(QtCore.QSize(24, 24))
        self.runbutton.setFlat(True)
        self.runbutton.setObjectName(_fromUtf8("runbutton"))
        self.horizontalLayout_2.addWidget(self.runbutton)
        spacerItem2 = QtGui.QSpacerItem(40, 32, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.progress = QtGui.QProgressBar(self.centralwidget)
        self.progress.setMaximumSize(QtCore.QSize(16777215, 24))
        self.progress.setProperty("value", 0)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.verticalLayout.addWidget(self.progress)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.hideerrors = QtGui.QPushButton(self.centralwidget)
        self.hideerrors.setMaximumSize(QtCore.QSize(16, 16))
        self.hideerrors.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/minimize.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideerrors.setIcon(icon5)
        self.hideerrors.setFlat(True)
        self.hideerrors.setObjectName(_fromUtf8("hideerrors"))
        self.horizontalLayout_3.addWidget(self.hideerrors)
        self.showerrors = QtGui.QPushButton(self.centralwidget)
        self.showerrors.setMaximumSize(QtCore.QSize(16, 16))
        self.showerrors.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/maximize.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showerrors.setIcon(icon6)
        self.showerrors.setFlat(True)
        self.showerrors.setObjectName(_fromUtf8("showerrors"))
        self.horizontalLayout_3.addWidget(self.showerrors)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.errors = QtGui.QTableWidget(self.centralwidget)
        self.errors.setShowGrid(True)
        self.errors.setColumnCount(0)
        self.errors.setObjectName(_fromUtf8("errors"))
        self.errors.setRowCount(0)
        self.verticalLayout.addWidget(self.errors)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 22))
        self.menubar.setStyleSheet(_fromUtf8(""))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuMethod = QtGui.QMenu(self.menubar)
        self.menuMethod.setObjectName(_fromUtf8("menuMethod"))
        self.menuAlgorithm = QtGui.QMenu(self.menuMethod)
        self.menuAlgorithm.setObjectName(_fromUtf8("menuAlgorithm"))
        self.menuPlugins = QtGui.QMenu(self.menuMethod)
        self.menuPlugins.setObjectName(_fromUtf8("menuPlugins"))
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuExport = QtGui.QMenu(self.menubar)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setGeometry(QtCore.QRect(0, 22, 320, 37))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionNew_Project = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionNew_Project.setIcon(icon7)
        self.actionNew_Project.setObjectName(_fromUtf8("actionNew_Project"))
        self.actionOpen_Project = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionOpen_Project.setIcon(icon8)
        self.actionOpen_Project.setObjectName(_fromUtf8("actionOpen_Project"))
        self.actionSave_Project = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/cd.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionSave_Project.setIcon(icon9)
        self.actionSave_Project.setObjectName(_fromUtf8("actionSave_Project"))
        self.actionSave_Project_As = QtGui.QAction(MainWindow)
        self.actionSave_Project_As.setObjectName(_fromUtf8("actionSave_Project_As"))
        self.actionStart = QtGui.QAction(MainWindow)
        self.actionStart.setEnabled(True)
        self.actionStart.setIcon(icon4)
        self.actionStart.setObjectName(_fromUtf8("actionStart"))
        self.actionParameters = QtGui.QAction(MainWindow)
        self.actionParameters.setObjectName(_fromUtf8("actionParameters"))
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
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/chart.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionLaunch_Viewer.setIcon(icon10)
        self.actionLaunch_Viewer.setObjectName(_fromUtf8("actionLaunch_Viewer"))
        self.actionTrace = QtGui.QAction(MainWindow)
        self.actionTrace.setObjectName(_fromUtf8("actionTrace"))
        self.actionResult = QtGui.QAction(MainWindow)
        self.actionResult.setObjectName(_fromUtf8("actionResult"))
        self.actionGenerate_Code = QtGui.QAction(MainWindow)
        self.actionGenerate_Code.setObjectName(_fromUtf8("actionGenerate_Code"))
        self.actionSettings = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon11)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionEdit_Program_Graph = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/graph.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit_Program_Graph.setIcon(icon12)
        self.actionEdit_Program_Graph.setObjectName(_fromUtf8("actionEdit_Program_Graph"))
        self.actionAnnealing = QtGui.QAction(MainWindow)
        self.actionAnnealing.setCheckable(True)
        self.actionAnnealing.setChecked(True)
        self.actionAnnealing.setObjectName(_fromUtf8("actionAnnealing"))
        self.actionGenetics = QtGui.QAction(MainWindow)
        self.actionGenetics.setCheckable(True)
        self.actionGenetics.setObjectName(_fromUtf8("actionGenetics"))
        self.actionDefault = QtGui.QAction(MainWindow)
        self.actionDefault.setObjectName(_fromUtf8("actionDefault"))
        self.actionPluginSettings = QtGui.QAction(MainWindow)
        self.actionPluginSettings.setObjectName(_fromUtf8("actionPluginSettings"))
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addAction(self.actionSave_Project_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAlgorithm.addAction(self.actionAnnealing)
        self.menuAlgorithm.addAction(self.actionGenetics)
        self.menuMethod.addAction(self.menuPlugins.menuAction())
        self.menuMethod.addAction(self.actionPluginSettings)
        self.menuMethod.addAction(self.menuAlgorithm.menuAction())
        self.menuMethod.addAction(self.actionParameters)
        self.menuMethod.addAction(self.actionStart)
        self.menuMethod.addAction(self.actionReset)
        self.menuMethod.addAction(self.actionLaunch_Viewer)
        self.menuMethod.addAction(self.actionEdit_Program_Graph)
        self.menuWindow.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionContents)
        self.menuHelp.addAction(self.actionAbout)
        self.menuExport.addAction(self.actionTrace)
        self.menuExport.addAction(self.actionResult)
        self.menuExport.addAction(self.actionGenerate_Code)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMethod.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew_Project)
        self.toolBar.addAction(self.actionOpen_Project)
        self.toolBar.addAction(self.actionSave_Project)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEdit_Program_Graph)
        self.toolBar.addAction(self.actionLaunch_Viewer)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionSettings)

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
        QtCore.QObject.connect(self.actionParameters, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.Parameters)
        QtCore.QObject.connect(self.actionLaunch_Viewer, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.LaunchViewer)
        QtCore.QObject.connect(self.actionTrace, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ExportTrace)
        QtCore.QObject.connect(self.runbutton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionStart.trigger)
        QtCore.QObject.connect(self.editname, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.EditName)
        QtCore.QObject.connect(self.edittime, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.EditTdir)
        QtCore.QObject.connect(self.editrel, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.EditRdir)
        QtCore.QObject.connect(self.editprogram, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionEdit_Program_Graph.trigger)
        QtCore.QObject.connect(self.hideerrors, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.HideErrors)
        QtCore.QObject.connect(self.showerrors, QtCore.SIGNAL(_fromUtf8("clicked()")), self.errors.show)
        QtCore.QObject.connect(self.actionResult, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ExportSchedule)
        QtCore.QObject.connect(self.actionGenerate_Code, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.GenerateCode)
        QtCore.QObject.connect(self.actionSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.Settings)
        QtCore.QObject.connect(self.actionEdit_Program_Graph, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.EditProgram)
        QtCore.QObject.connect(self.actionAnnealing, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SetAnnealing)
        QtCore.QObject.connect(self.actionGenetics, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.SetGenetics)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), MainWindow.ChangeAlgorithm)
        QtCore.QObject.connect(self.actionPluginSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.PluginSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Scheduler GUI", None, QtGui.QApplication.UnicodeUTF8))
        self.projectname.setText(QtGui.QApplication.translate("MainWindow", "Project name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Program info", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Vertices", None, QtGui.QApplication.UnicodeUTF8))
        self.vertices.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Edges", None, QtGui.QApplication.UnicodeUTF8))
        self.edges.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Deadline", None, QtGui.QApplication.UnicodeUTF8))
        self.tdir.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Reliability limit", None, QtGui.QApplication.UnicodeUTF8))
        self.rdir.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Trace length", None, QtGui.QApplication.UnicodeUTF8))
        self.tracelen.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Launch search", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Simulated Annealing", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "Genetics", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Error list", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMethod.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAlgorithm.setTitle(QtGui.QApplication.translate("MainWindow", "Algorithm", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlugins.setTitle(QtGui.QApplication.translate("MainWindow", "Time Computation Method", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionStart.setText(QtGui.QApplication.translate("MainWindow", "Launch Search", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionParameters.setText(QtGui.QApplication.translate("MainWindow", "Algorithm Parameters...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionContents.setText(QtGui.QApplication.translate("MainWindow", "Contents...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Scheduler.setText(QtGui.QApplication.translate("MainWindow", "About Scheduler", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset.setShortcut(QtGui.QApplication.translate("MainWindow", "F10", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_name.setText(QtGui.QApplication.translate("MainWindow", "Change Name...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_New_System.setText(QtGui.QApplication.translate("MainWindow", "Load New System...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_New_Method.setText(QtGui.QApplication.translate("MainWindow", "Load New Parameters...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Random_System.setText(QtGui.QApplication.translate("MainWindow", "Generate Random System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Random_System.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLanguage.setText(QtGui.QApplication.translate("MainWindow", "Language...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_Limits.setText(QtGui.QApplication.translate("MainWindow", "Change Limits...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLaunch_Viewer.setText(QtGui.QApplication.translate("MainWindow", "Launch Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLaunch_Viewer.setShortcut(QtGui.QApplication.translate("MainWindow", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTrace.setText(QtGui.QApplication.translate("MainWindow", "Trace...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResult.setText(QtGui.QApplication.translate("MainWindow", "Result...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Code.setText(QtGui.QApplication.translate("MainWindow", "Generate Code...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setShortcut(QtGui.QApplication.translate("MainWindow", "F12", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Program_Graph.setText(QtGui.QApplication.translate("MainWindow", "Edit Program Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Program_Graph.setShortcut(QtGui.QApplication.translate("MainWindow", "F3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnnealing.setText(QtGui.QApplication.translate("MainWindow", "Simulated Annealing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenetics.setText(QtGui.QApplication.translate("MainWindow", "Genetics", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDefault.setText(QtGui.QApplication.translate("MainWindow", "default", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPluginSettings.setText(QtGui.QApplication.translate("MainWindow", "Time Computation Parameters...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
