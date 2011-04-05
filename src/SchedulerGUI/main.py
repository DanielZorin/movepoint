from PyQt4 import QtGui
import sys

from MainWindow import MainWindow

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
