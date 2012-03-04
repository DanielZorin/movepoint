from PyQt4 import uic
import os

if __name__ == "__main__":
    for s in os.listdir(os.curdir):
        if s.endswith(".ui"):
            fin = open(s, "r")
            fout = open("ui_" + s.replace(".ui", ".py"), "w")
            print("Building " + s + "...")
            uic.compileUi(fin, fout, from_imports=True)
            fin.close()
            fout.close()

    os.system("pyrcc4 -py3 resources.qrc -o resources_rc.py")
    
    if 1 == 1:
        os.chdir("..")
        os.system("pylupdate4 SchedulerGUI.pro")
        