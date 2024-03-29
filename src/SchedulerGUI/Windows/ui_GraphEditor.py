
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GraphEditor(object):
    def setupUi(self, GraphEditor):
        GraphEditor.setObjectName(_fromUtf8("GraphEditor"))
        GraphEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        GraphEditor.resize(427, 312)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/graph.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GraphEditor.setWindowIcon(icon)
        GraphEditor.setStyleSheet(_fromUtf8("QWidget, QMenuBar::item {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #c5d8ef, stop: 1 #89a5c3);\n"
"}\n"
"\n"
"QLabel, QSlider {\n"
"    background-color: transparent;\n"
"}"))
        self.centralwidget = QtGui.QWidget(GraphEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphArea = QtGui.QScrollArea(self.centralwidget)
        self.graphArea.setWidgetResizable(False)
        self.graphArea.setObjectName(_fromUtf8("graphArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 398, 230))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.graphArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.graphArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        GraphEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(GraphEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 427, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuGenerate = QtGui.QMenu(self.menubar)
        self.menuGenerate.setObjectName(_fromUtf8("menuGenerate"))
        GraphEditor.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(GraphEditor)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        GraphEditor.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSelect = QtGui.QAction(GraphEditor)
        self.actionSelect.setCheckable(True)
        self.actionSelect.setChecked(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/select.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon1)
        self.actionSelect.setObjectName(_fromUtf8("actionSelect"))
        self.actionVertex = QtGui.QAction(GraphEditor)
        self.actionVertex.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/vertex.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVertex.setIcon(icon2)
        self.actionVertex.setObjectName(_fromUtf8("actionVertex"))
        self.actionEdge = QtGui.QAction(GraphEditor)
        self.actionEdge.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/edge.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdge.setIcon(icon3)
        self.actionEdge.setObjectName(_fromUtf8("actionEdge"))
        self.actionNew_System = QtGui.QAction(GraphEditor)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew_System.setIcon(icon4)
        self.actionNew_System.setObjectName(_fromUtf8("actionNew_System"))
        self.actionOpen_System = QtGui.QAction(GraphEditor)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_System.setIcon(icon5)
        self.actionOpen_System.setObjectName(_fromUtf8("actionOpen_System"))
        self.actionSave_System = QtGui.QAction(GraphEditor)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/cd.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_System.setIcon(icon6)
        self.actionSave_System.setObjectName(_fromUtf8("actionSave_System"))
        self.actionSave_System_As = QtGui.QAction(GraphEditor)
        self.actionSave_System_As.setObjectName(_fromUtf8("actionSave_System_As"))
        self.actionExit = QtGui.QAction(GraphEditor)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionNew_System)
        self.menuFile.addAction(self.actionOpen_System)
        self.menuFile.addAction(self.actionSave_System)
        self.menuFile.addAction(self.actionSave_System_As)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGenerate.menuAction())
        self.toolBar.addAction(self.actionNew_System)
        self.toolBar.addAction(self.actionOpen_System)
        self.toolBar.addAction(self.actionSave_System)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSelect)
        self.toolBar.addAction(self.actionVertex)
        self.toolBar.addAction(self.actionEdge)

        self.retranslateUi(GraphEditor)
        QtCore.QObject.connect(self.actionSelect, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.toggleSelect)
        QtCore.QObject.connect(self.actionVertex, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.toggleVertex)
        QtCore.QObject.connect(self.actionEdge, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.toggleEdge)
        QtCore.QObject.connect(self.actionNew_System, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.New)
        QtCore.QObject.connect(self.actionOpen_System, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.Open)
        QtCore.QObject.connect(self.actionSave_System, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.Save)
        QtCore.QObject.connect(self.actionSave_System_As, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.SaveAs)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), GraphEditor.close)
        QtCore.QMetaObject.connectSlotsByName(GraphEditor)

    def retranslateUi(self, GraphEditor):
        GraphEditor.setWindowTitle(QtGui.QApplication.translate("GraphEditor", "Program Graph Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("GraphEditor", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGenerate.setTitle(QtGui.QApplication.translate("GraphEditor", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("GraphEditor", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect.setText(QtGui.QApplication.translate("GraphEditor", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect.setShortcut(QtGui.QApplication.translate("GraphEditor", "Alt+1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionVertex.setText(QtGui.QApplication.translate("GraphEditor", "Add Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.actionVertex.setShortcut(QtGui.QApplication.translate("GraphEditor", "Alt+2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdge.setText(QtGui.QApplication.translate("GraphEditor", "Add Edge", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdge.setShortcut(QtGui.QApplication.translate("GraphEditor", "Alt+3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_System.setText(QtGui.QApplication.translate("GraphEditor", "New System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_System.setShortcut(QtGui.QApplication.translate("GraphEditor", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_System.setText(QtGui.QApplication.translate("GraphEditor", "Open System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_System.setShortcut(QtGui.QApplication.translate("GraphEditor", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_System.setText(QtGui.QApplication.translate("GraphEditor", "Save System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_System.setShortcut(QtGui.QApplication.translate("GraphEditor", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_System_As.setText(QtGui.QApplication.translate("GraphEditor", "Save System As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_System_As.setShortcut(QtGui.QApplication.translate("GraphEditor", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("GraphEditor", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("GraphEditor", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
