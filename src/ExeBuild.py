'''
Created on 07.01.2011

@author: juan
'''
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

if sys.argv[-1] != "build":
    sys.argv.append("build")
    
setup(name = "scheduler", version = "0.1", description = "scheduler", executables = [Executable("SchedulerGUI-launch.py", base=base)])