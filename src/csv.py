from Schedules.System import *
from SchedulerGUI.Project import Project

p1 = Project("program.xml", "temperature test")
p2 = Project("program.xml", "temperature test")
res = []
for i in range(2, 5):
    for j in range(1, 5):
        name = "results/temperature_test_" + str(i*10) + "_vertices_"+ str(j) + "_Idle time reduction_"
        bolz = name + "Bolzmann.proj"
        cauchy = name + "Bolzmann.proj"
        
        p2.Deserialize(cauchy)
        p1.Deserialize(bolz)
        if p1.method.trace.getBest()[1]["processors"] < p2.method.trace.getBest()[1]["processors"]:
            best = p1
            worst = p2
            sign = 1
        else:
            best = p2
            worst = p1
            sign = -1
        worstiter = worst.method.trace.best
        worstproc = worst.method.trace.getCurrent()[1]["processors"] 
        best.method.ScrollTrace(best.method.trace.best - best.method.trace.current)
        while best.method.trace.getCurrent()[1]["processors"] != worstproc:
            best.method.ScrollTrace(-1)
        bestiter = best.method.trace.current
        result = int(bestiter / worstiter * sign * 100)
        if result in res:
            res[result] += 1
        else:
            res[result] = 1

for k in res.keys():
    print (k) 
for k in res.keys():
    print (res[k])