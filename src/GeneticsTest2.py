from Schedules.System import *
from SchedulerGUI.Project import Project

def run(p, i):  
    p.method.Reset()
    p.method.numberOfIterations = 10
    p.method.Start()
    return p.method.trace.getBest()[1]

# Run tests with all strategies and temperature functions
p = Project("programc.xml", "temperature test")
p.method.algorithm = p.genetics
res = ""
for i in range(100):
    print ( i)
    res += str(i) + ";"
    #try:
    best = run(p, i)
    res += str(best["processors"]) + ";"
    #except:
    #    res += "ERROR;"
    print (res)
    res += "\n"
f = open("results_genetics_crash_" + str(100) + ".txt", "w")
f.write(res)
f.close()