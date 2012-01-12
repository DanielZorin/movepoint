# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Viewer.ui'
#
# Created: Thu Jan 12 21:09:15 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Viewer(object):
    def setupUi(self, Viewer):
        Viewer.setObjectName(_fromUtf8("Viewer"))
        Viewer.resize(584, 336)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Viewer.sizePolicy().hasHeightForWidth())
        Viewer.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/chart.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Viewer.setWindowIcon(icon)
        Viewer.setStyleSheet(_fromUtf8("QWidget, QMenuBar::item {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #c5d8ef, stop: 1 #89a5c3);\n"
"}\n"
"\n"
"QLabel, QSlider {\n"
"    background-color: transparent;\n"
"}"))
        self.centralwidget = QtGui.QWidget(Viewer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.visualizerArea = QtGui.QScrollArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.visualizerArea.sizePolicy().hasHeightForWidth())
        self.visualizerArea.setSizePolicy(sizePolicy)
        self.visualizerArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.visualizerArea.setWidgetResizable(False)
        self.visualizerArea.setObjectName(_fromUtf8("visualizerArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget(self.visualizerArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 452, 221))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.visualizerArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.visualizerArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.rewind = QtGui.QPushButton(self.centralwidget)
        self.rewind.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rewind.sizePolicy().hasHeightForWidth())
        self.rewind.setSizePolicy(sizePolicy)
        self.rewind.setMaximumSize(QtCore.QSize(31, 16777215))
        self.rewind.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/rewind.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rewind.setIcon(icon1)
        self.rewind.setIconSize(QtCore.QSize(32, 32))
        self.rewind.setFlat(True)
        self.rewind.setObjectName(_fromUtf8("rewind"))
        self.horizontalLayout_2.addWidget(self.rewind)
        self.stepback = QtGui.QPushButton(self.centralwidget)
        self.stepback.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stepback.sizePolicy().hasHeightForWidth())
        self.stepback.setSizePolicy(sizePolicy)
        self.stepback.setMaximumSize(QtCore.QSize(31, 16777215))
        self.stepback.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/skip_backward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stepback.setIcon(icon2)
        self.stepback.setIconSize(QtCore.QSize(32, 32))
        self.stepback.setFlat(True)
        self.stepback.setObjectName(_fromUtf8("stepback"))
        self.horizontalLayout_2.addWidget(self.stepback)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(30, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_2.addWidget(self.label_7)
        self.labelTotal = QtGui.QLabel(self.centralwidget)
        self.labelTotal.setObjectName(_fromUtf8("labelTotal"))
        self.horizontalLayout_2.addWidget(self.labelTotal)
        self.stepforth = QtGui.QPushButton(self.centralwidget)
        self.stepforth.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stepforth.sizePolicy().hasHeightForWidth())
        self.stepforth.setSizePolicy(sizePolicy)
        self.stepforth.setMaximumSize(QtCore.QSize(31, 16777215))
        self.stepforth.setStyleSheet(_fromUtf8(""))
        self.stepforth.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/skip_forward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stepforth.setIcon(icon3)
        self.stepforth.setIconSize(QtCore.QSize(32, 32))
        self.stepforth.setFlat(True)
        self.stepforth.setObjectName(_fromUtf8("stepforth"))
        self.horizontalLayout_2.addWidget(self.stepforth)
        self.replay = QtGui.QPushButton(self.centralwidget)
        self.replay.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replay.sizePolicy().hasHeightForWidth())
        self.replay.setSizePolicy(sizePolicy)
        self.replay.setMaximumSize(QtCore.QSize(31, 16777215))
        self.replay.setStyleSheet(_fromUtf8(""))
        self.replay.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/fast_forward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.replay.setIcon(icon4)
        self.replay.setIconSize(QtCore.QSize(32, 32))
        self.replay.setFlat(True)
        self.replay.setObjectName(_fromUtf8("replay"))
        self.horizontalLayout_2.addWidget(self.replay)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.info = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info.sizePolicy().hasHeightForWidth())
        self.info.setSizePolicy(sizePolicy)
        self.info.setMinimumSize(QtCore.QSize(100, 0))
        self.info.setMaximumSize(QtCore.QSize(100, 16777215))
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.info)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_3 = QtGui.QLabel(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.labeltime = QtGui.QLabel(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labeltime.sizePolicy().hasHeightForWidth())
        self.labeltime.setSizePolicy(sizePolicy)
        self.labeltime.setObjectName(_fromUtf8("labeltime"))
        self.verticalLayout_3.addWidget(self.labeltime)
        self.label_2 = QtGui.QLabel(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.labelrel = QtGui.QLabel(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelrel.sizePolicy().hasHeightForWidth())
        self.labelrel.setSizePolicy(sizePolicy)
        self.labelrel.setObjectName(_fromUtf8("labelrel"))
        self.verticalLayout_3.addWidget(self.labelrel)
        self.label = QtGui.QLabel(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.labelproc = QtGui.QLabel(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelproc.sizePolicy().hasHeightForWidth())
        self.labelproc.setSizePolicy(sizePolicy)
        self.labelproc.setObjectName(_fromUtf8("labelproc"))
        self.verticalLayout_3.addWidget(self.labelproc)
        self.label_4 = QtGui.QLabel(self.info)
        self.label_4.setStyleSheet(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.tdir = QtGui.QLabel(self.info)
        self.tdir.setObjectName(_fromUtf8("tdir"))
        self.verticalLayout_3.addWidget(self.tdir)
        self.label_6 = QtGui.QLabel(self.info)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_3.addWidget(self.label_6)
        self.rdir = QtGui.QLabel(self.info)
        self.rdir.setObjectName(_fromUtf8("rdir"))
        self.verticalLayout_3.addWidget(self.rdir)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalSlider = QtGui.QSlider(self.info)
        self.verticalSlider.setSliderPosition(50)
        self.verticalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.verticalLayout_3.addWidget(self.verticalSlider)
        self.horizontalLayout_3.addWidget(self.info)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        Viewer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Viewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 584, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSchedule = QtGui.QMenu(self.menubar)
        self.menuSchedule.setObjectName(_fromUtf8("menuSchedule"))
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        Viewer.setMenuBar(self.menubar)
        self.actionColors = QtGui.QAction(Viewer)
        self.actionColors.setObjectName(_fromUtf8("actionColors"))
        self.actionStep_Forward = QtGui.QAction(Viewer)
        self.actionStep_Forward.setObjectName(_fromUtf8("actionStep_Forward"))
        self.actionStep_Backward = QtGui.QAction(Viewer)
        self.actionStep_Backward.setObjectName(_fromUtf8("actionStep_Backward"))
        self.menuSchedule.addAction(self.actionStep_Forward)
        self.menuSchedule.addAction(self.actionStep_Backward)
        self.menuWindow.addAction(self.actionColors)
        self.menubar.addAction(self.menuSchedule.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())

        self.retranslateUi(Viewer)
        QtCore.QObject.connect(self.actionColors, QtCore.SIGNAL(_fromUtf8("triggered()")), Viewer.Colors)
        QtCore.QObject.connect(self.actionStep_Backward, QtCore.SIGNAL(_fromUtf8("triggered()")), Viewer.StepBackward)
        QtCore.QObject.connect(self.actionStep_Forward, QtCore.SIGNAL(_fromUtf8("triggered()")), Viewer.StepForward)
        QtCore.QObject.connect(self.stepback, QtCore.SIGNAL(_fromUtf8("clicked()")), Viewer.StepBackward)
        QtCore.QObject.connect(self.stepforth, QtCore.SIGNAL(_fromUtf8("clicked()")), Viewer.StepForward)
        QtCore.QObject.connect(self.replay, QtCore.SIGNAL(_fromUtf8("clicked()")), Viewer.Replay)
        QtCore.QObject.connect(self.rewind, QtCore.SIGNAL(_fromUtf8("clicked()")), Viewer.Rewind)
        QtCore.QMetaObject.connectSlotsByName(Viewer)

    def retranslateUi(self, Viewer):
        Viewer.setWindowTitle(QtGui.QApplication.translate("Viewer", "Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Viewer", "/", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTotal.setText(QtGui.QApplication.translate("Viewer", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Viewer", "Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.labeltime.setText(QtGui.QApplication.translate("Viewer", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Viewer", "Reliability:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelrel.setText(QtGui.QApplication.translate("Viewer", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Viewer", "Processors:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelproc.setText(QtGui.QApplication.translate("Viewer", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Viewer", "Time Limit:", None, QtGui.QApplication.UnicodeUTF8))
        self.tdir.setText(QtGui.QApplication.translate("Viewer", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Viewer", "Reliability Limit:", None, QtGui.QApplication.UnicodeUTF8))
        self.rdir.setText(QtGui.QApplication.translate("Viewer", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSchedule.setTitle(QtGui.QApplication.translate("Viewer", "Schedule", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("Viewer", "Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionColors.setText(QtGui.QApplication.translate("Viewer", "Colors...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep_Forward.setText(QtGui.QApplication.translate("Viewer", "Step Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep_Forward.setShortcut(QtGui.QApplication.translate("Viewer", "PgDown", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep_Backward.setText(QtGui.QApplication.translate("Viewer", "Step Backward", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep_Backward.setShortcut(QtGui.QApplication.translate("Viewer", "PgUp", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
