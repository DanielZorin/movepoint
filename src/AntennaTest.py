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
for k in [16, 32, 64, 128]:
    for l in [8, 16, 32, 64]:
        for m in [1,2,3,4]: 
            gen.K = k
            gen.L = l
            gen.Mtheta = m 
            gen.B = 900
            gen.Generate(p.system)
            print (k, l, m)
            for i in [1]:
                try:
                    best = run(p, l, m)
                    ratio = str(float(best["processors"]) / float(l + 1) / float(m + 1)) + ";"
                except:
                    ratio = "ERROR;"
                f = open("results_antenna.txt", "a")
                f.write("b200;" + str(k) + ";" + str(l) + ";" + str(m) + ";" + str(i) + ";" + str(best["processors"]) + ";" + ratio + str(best["time"]) + "\n")
                f.close()
    res += "\n"