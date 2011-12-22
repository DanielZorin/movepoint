from PyQt4 import uic
import os

if __name__ == "__main__":
    fin = open("MainWindow.ui", "r")
    fout = open("ui_MainWindow.py", "w")
    uic.compileUi(fin, fout, from_imports=True)
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

    fin = open("Viewer.ui", "r")
    fout = open("ui_Viewer.py", "w")
    uic.compileUi(fin, fout, from_imports=True)
    fin.close()
    fout.close()

    os.system("pyrcc4 -py3 resources.qrc -o resources_rc.py")
    
    if 0 == 1:
        os.chdir("..")
        os.system("pylupdate4 SchedulerGUI.pro")
        