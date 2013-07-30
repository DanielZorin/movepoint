from Schedules.System import *
from SchedulerGUI.Project import Project
from plugins.Random import *

gen = RandomProgramGenerator()

def run(p, v, i, strategy):
    gen.n = v
    gen.Generate(p.method.system)  
    p.method.algorithm.strategies[1] = strategy
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/final_test_" + str(v) + "_vertices_" + str(i) + "_" + \
        p.method.algorithm.strategies[0][strategy]  + ".proj")
    return p.method.trace.getBest()[1]

# Compare temperatures with each other
p = Project("program.xml", "temperature test")
for i in range(1, 160):
    for j in range(1, 100):
        for s in [0, 1, 2]:
            #try:
            run(p, i * 5, j, s)
            while p.method.trace.getCurrent()[1]["processors"] != p.method.trace.getBest()[1]["processors"]:
                p.method.ScrollTrace(-1)
            iter = p.method.trace.current
            proc = p.method.trace.getBest()[1]["processors"]
            #except:
            #    iter = -1
            #    proc = -1
            f = open("final_results.txt", "a")
            f.write(str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()
