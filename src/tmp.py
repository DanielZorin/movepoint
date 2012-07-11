from Schedules.System import *
from SchedulerGUI.Project import Project
    
def run(p, v, i, strategy, threshold):  
    p.method.strategies[1] = strategy
    p.method.threshold[1] = threshold
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/temperature_test_initial_" + str(v) + "_" + str(i) + "_" + \
        p.method.strategies[0][strategy] + "_" + p.method.threshold[0][threshold]  + ".proj")
    return p.method.trace.getBest()[1]

p = Project("program.xml", "temperature test")
p.GenerateRandomSystem({"n":50, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
res = ""
for i in range(100):        
    print (i)
    for s in [0]:
        res += str(i) + ";"
        for t in [0, 1, 2]:
            for init in range(5, 20):
                try:
                    best = run(p, init * 10.0, i, s, t)
                    res += str(best["processors"]) + ";" + str(best["time"]) + ";"
                except:
                    res += "ERROR;ERROR;"
        res += "\n"
f = open("results_temperature_initial_" + str(v) + ".txt", "w")
f.write(res)
f.close()