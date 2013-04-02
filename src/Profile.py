from Schedules.System import *
from SchedulerGUI.Project import Project
from plugins.Antenna import AntennaGenerator
import math

def run(p, v, i):
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/antenna_l_" + str(v) + "_m_" + str(i) + ".proj")
    return p.method.trace.getBest()[1]

p = Project("program.xml", "temperature test") 
gen = AntennaGenerator()

import time
t0 = time.clock()
res = ""
for l in range(1, 50):
    for m in range(1, 3): 
        gen.L = l + 1
        gen.Mtheta = m + 1 
        gen.Generate(p.system)
        print (l + 1, m + 1)
        try:
            pass
            #best = run(p, l, m)
        except:
            pass
        t1 = time.clock() - t0
        n = l*10
        res += "%d\t%f\t%f\t%f\t%f\n" % (n, t1, t1/(n**1), t1/(n**2), t1/(n**3))
        t0 = time.clock()
        print(res)
print(res)