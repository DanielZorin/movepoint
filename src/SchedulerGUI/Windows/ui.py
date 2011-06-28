from PyQt4 import uic
import os

if __name__ == "__main__":
    fin = open("MainWindow.ui", "r")
    fout = open("ui_MainWindow.py", "w")
    uic.compileUi(fin, fout)
    fin.close()
    fout.close()
    
    fin = open("NewProjectDialog.ui", "r")
    fout = open("ui_NewProjectDialog.py", "w")
    uic.compileUi(fin, fout)
    fin.close()
    fout.close()
    
    fin = open("PreferencesDialog.ui", "r")
    fout = open("ui_PreferencesDialog.py", "w")
    uic.compileUi(fin, fout)
    fin.close()
    fout.close()
    
    fin = open("RandomSystemDialog.ui", "r")
    fout = open("ui_RandomSystemDialog.py", "w")
    uic.compileUi(fin, fout)
    fin.close()
    fout.close()
    
    if 0 == 1:
        os.chdir("..")
        os.system("pylupdate4 SchedulerGUI.pro")
        