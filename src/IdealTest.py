from Schedules.System import *
from Schedules.Metrics import HMetric
from SchedulerGUI.Project import Project
from plugins.IdealProgram import *

gen = IdealProgramGenerator()

def run(p, v, i, strategy):  
    p.method.algorithm.strategies[1] = strategy
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/ideal_test_" + str(v) + "_vertices_" + str(i) + "_" + \
        p.method.algorithm.strategies[0][strategy]  + ".proj")
    return ideal

# Compare temperatures with each other
p = Project("program.xml", "temperature test")
for i in range(2, 160):
    gen.vertices = i * 5
    ideal = gen.Generate(p.method.system)
    for j in range(1, 100):
        for s in [0, 1, 2]:
            #try:
            ideal = run(p, i * 5, j, s)
            p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
            metric = HMetric(ideal, p.method.system.schedule)
            iter = p.method.trace.current
            proc = p.method.trace.getBest()[1]["processors"]           
            #except:
            #    iter = -1
            #    proc = -1
            f = open("ideal_results.txt", "a")
            f.write(str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + ";" + str(metric) + "\n")
            f.close()
