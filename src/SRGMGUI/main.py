from PyQt4 import QtGui
import sys

from mymainwindow import MyMainWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
