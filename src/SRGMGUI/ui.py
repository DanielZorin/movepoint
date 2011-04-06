from PyQt4 import uic

fin = file("main.ui", "r")
fout = file("ui_main.py", "w")
uic.compileUi(fin, fout)
