from PyQt4.QtGui import QMainWindow
from SchedulerGUI.Windows.ui_GraphEditor import Ui_GraphEditor
from SchedulerGUI.GraphCanvas import GraphCanvas, State

class GraphEditor(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_GraphEditor()
        self.ui.setupUi(self)
        self.canvas = GraphCanvas(self.ui.graphArea)

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