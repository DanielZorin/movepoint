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
for e in [0.2, 0.9, 1.5]:
    for i in range(5, 25):
        gen.vertices = i * 5
        gen.edges = e
        gen.k = 1.8
        ideal = gen.Generate(p.method.system)
        f = open("results_ideal.txt", "a")
        f.write(str(e) + "\n")
        f.close()
        for j in range(1, 6):
            for s in [0, 1, 2, 3]:
                try:
                    print(i, j)
                    ideal = run(p, i * 5, j, s)
                    p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                    metric = HMetric(ideal, p.method.system.schedule)
                    time =  p.method.trace.getBest()[1]["time"] 
                    iter = p.method.trace.current
                    proc = p.method.trace.getBest()[1]["processors"]                   
                except:
                    iter = -1
                    proc = -1
                f = open("results_ideal.txt", "a")
                f.write(str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + ";" + str(metric) + "\n")
                f.close()
