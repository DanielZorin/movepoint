from Schedules.System import *
from SchedulerGUI.Project import Project
from plugins.Antenna import AntennaGenerator
import math

def run(p, v, i):
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/antenna_l_" + str(v) + "_m_" + str(i) + ".proj")
    return p.method.trace.getBest()[1]

# Run tests with all strategies and temperature functions
p = Project("program.xml", "temperature test") 
gen = AntennaGenerator()
gen.K = 8
res = ""
for l in range(1, 100):
    for m in range(1, 4): 
        gen.L = l + 1
        gen.Mtheta = m + 1 
        gen.B = 400
        gen.Generate(p.system)
        print (l + 1, m + 1)
        try:
            best = run(p, l, m)
            ratio = str(float(best["processors"]) / float(l + 1) / float(m + 1)) + ";"
        except:
            ratio = "ERROR;"
        f = open("results_antenna.txt", "a")
        f.write("b200;" + str(l) + ";" + str(m) + ";" + str(best["processors"]) + ";" + ratio + str(best["time"]) + "\n")
        f.close()

        gen.B = 900
        gen.Generate(p.system)
        print (l + 1, m + 1)
        try:
            best = run(p, l, m)
            ratio = str(float(best["processors"]) / float(l + 1) / float(m + 1)) + ";"
        except:
            ratio = "ERROR;"
        f = open("results_antenna.txt", "a")
        f.write("b900;" + str(l) + ";" + str(m) + ";" + str(best["processors"]) + ";" + ratio + str(best["time"]) + "\n")
        f.close()
    res += "\n"