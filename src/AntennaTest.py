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
res = ""
for l in range(1, 10):
    for m in range(1, 4): 
        gen.L = l + 1
        gen.Mtheta = m + 1 
        gen.Generate(p.system)
        print (l + 1, m + 1)
        try:
            best = run(p, l, m)
            res += str(float(best["processors"]) / float(l + 1) / float(m + 1)) + ";"
        except:
            res += "ERROR;"
        f = open("results_antenna.txt", "w")
        f.write(res)
        f.close()
    res += "\n"