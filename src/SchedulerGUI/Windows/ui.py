from PyQt4 import uic

if __name__ == "__main__":
    fin = open("MainWindow.ui", "r")
    fout = open("ui_MainWindow.py", "w")
    uic.compileUi(fin, fout)
    
    fin = open("NewProjectDialog.ui", "r")
    fout = open("ui_NewProjectDialog.py", "w")
    uic.compileUi(fin, fout)
    
    fin = open("PreferencesDialog.ui", "r")
    fout = open("ui_PreferencesDialog.py", "w")
    uic.compileUi(fin, fout)
    
    fin = open("RandomSystemDialog.ui", "r")
    fout = open("ui_RandomSystemDialog.py", "w")
    uic.compileUi(fin, fout)