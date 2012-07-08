from Schedules.System import *
from SchedulerGUI.Project import Project
    
def run(p, v, i, strategy, threshold):  
    p.method.strategies[1] = strategy
    p.method.threshold[1] = threshold
    p.method.Reset()
    p.method.Start()
    p.Serialize("temperature_test_" + str(v) + "_vertices_" + p.method.strategies[0][strategy] + "_" + \
        p.method.threshold[0][threshold] + "_" + str(i) + ".proj")
    return p.method.trace.getBest()[1]

p = Project("program.xml", "temperature test") 
for v in [10,20,30,40,50]:
    res = ""
    for i in range(100):       
        p.GenerateRandomSystem({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
        print (v, i)
        for s in [0, 1, 2]:
            res += str(i) + " " + str(s) + ":"
            for t in [0, 1, 2]:
                try:
                    best = run(p, v, i, s, t)
                    res += str(best["processors"]) + " " + str(best["time"]) + "/"
                except:
                    res += "ERROR/"
            res += "\n"
    f = open("results_temperature_" + str(v) + ".txt", "w")
    f.write(res)
    f.close()