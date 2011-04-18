from PyQt4 import uic

fin = open("main.ui", "r")
fout = open("ui_main.py", "w")
uic.compileUi(fin, fout)
