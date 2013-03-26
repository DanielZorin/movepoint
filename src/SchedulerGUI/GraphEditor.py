from SchedulerGUI.Windows.ui_GraphEditor import Ui_GraphEditor
from SchedulerGUI.GraphCanvas import GraphCanvas, State
from SchedulerGUI.SettingsDialog import SettingsDialog
from PyQt4.QtGui import QFileDialog, QActionGroup, QMainWindow, QAction, QFileDialog, QDialog
from PyQt4.QtCore import SIGNAL, QObject
import sys, os

class GraphEditor(QMainWindow):
    xmlfile = None
    generators = {}

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_GraphEditor()
        self.ui.setupUi(self)
        self.canvas = GraphCanvas(self.ui.graphArea)
        self.ui.graphArea.setWidget(self.canvas)
        self.loadPlugins()

    def setData(self, data):
        self.system = data
        self.canvas.Visualize(self.system.program)

    def toggleSelect(self):
        self.ui.actionSelect.setChecked(True)
        self.ui.actionVertex.setChecked(False)
        self.ui.actionEdge.setChecked(False)
        self.canvas.state = State.Select

    def toggleVertex(self):
        self.ui.actionSelect.setChecked(False)
        self.ui.actionVertex.setChecked(True)
        self.ui.actionEdge.setChecked(False)
        self.canvas.state = State.Vertex

    def toggleEdge(self):
        self.ui.actionSelect.setChecked(False)
        self.ui.actionVertex.setChecked(False)
        self.ui.actionEdge.setChecked(True)
        self.canvas.state = State.Edge

    def resizeEvent(self, e):
        super(QMainWindow, self).resizeEvent(e)
        self.canvas.ResizeCanvas()

    def showEvent(self, e):
        super(QMainWindow, self).showEvent(e)
        self.canvas.ResizeCanvas()

    def LoadPositions(self, lst):
        if lst == {}:
            # TODO: dirty
            return
        self.canvas.vertices = lst
        self.canvas.ResizeCanvas()
        self.canvas.repaint()

    def SavePositions(self):
        return self.canvas.vertices

    def New(self):
        self.system.program.vertices = []
        self.system.program.edges = []
        self.system.program._buildData()
        self.canvas.Clear()
        self.canvas.Visualize(self.system.program)
        self.canvas.changed = True

    def Open(self):
        name = QFileDialog.getOpenFileName(filter="*.xml")
        if name == None or name == '':
            return
        self.system.Reload(name)
        self.canvas.Clear()
        self.canvas.Visualize(self.system.program)
        self.canvas.changed = True
        self.xmlfile = name

    def Save(self):
        if self.xmlfile == None:
            self.SaveAs()
        else:
            self.system.Export(self.xmlfile)

    def SaveAs(self):
        self.xmlfile = QFileDialog.getSaveFileName(directory=".xml", filter="*.xml")
        if self.xmlfile != '':
            self.system.Export(self.xmlfile)

    def loadPlugins(self):
        sys.path.append(os.curdir + os.sep + "plugins")
        plugins = QActionGroup(self)
        plugins.setExclusive(True)
        for s in os.listdir("plugins"):
            # TODO: check all errors
            if s.endswith(".py"):
                plugin = __import__(s[:-3])
                if "pluginMain" in dir(plugin):
                    pluginClass = plugin.pluginMain()
                    type = pluginClass.GetType()
                    if type != "generator":
                        continue
                    name = pluginClass.GetName()
                    action = QAction(name, self)
                    action.setCheckable(False)
                    QObject.connect(action, SIGNAL("triggered()"), self.LaunchGenerator)
                    plugins.addAction(action)
                    self.ui.menuGenerate.addAction(action)
                    self.generators[action] = pluginClass()
                else:
                    print("pluginMain not found in " + s)

    def LaunchGenerator(self):
        generator = self.generators[self.sender()]
        data = generator.GetSettings()
        d = SettingsDialog(data, self)
        d.exec_()
        if d.result() == QDialog.Accepted:
            generator.UpdateSettings(d.data)
            self.system = generator.Generate()
            self.system.program._buildData()
            self.canvas.Clear()
            self.canvas.Visualize(self.system.program)
            self.canvas.changed = True