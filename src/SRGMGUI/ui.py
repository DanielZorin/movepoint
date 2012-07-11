from PyQt4 import uic

if __name__ == "__main__":
    fin = open("main.ui", "r")
    fout = open("ui_main.py", "w")
    uic.compileUi(fin, fout, from_imports=True)
    