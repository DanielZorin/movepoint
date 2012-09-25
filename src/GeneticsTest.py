from Schedules.System import *
from SchedulerGUI.Project import Project

def run(p, v, i):  
    p.method.Reset()
    p.method.numberOfIterations = 10
    p.method.Start()
    return p.method.trace.getBest()[1]

# Run tests with all strategies and temperature functions
p = Project("program.xml", "temperature test")
p.method.algorithm = p.genetics
for v in [10,20]:
    res = ""  
    p.GenerateRandomSystem({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
    for i in range(100):
        print (v, i)
        res += str(i) + ";"
        #try:
        best = run(p, v, i)
        res += str(best["processors"]) + ";"
        #except:
        #    res += "ERROR;"
        print (res)
        res += "\n"
    f = open("results_genetics_" + str(v) + ".txt", "w")
    f.write(res)
    f.close()