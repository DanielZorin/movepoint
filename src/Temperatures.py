from Schedules.System import *
from SchedulerGUI.Project import Project
    
def run(p, v, i, strategy, threshold, raising):  
    p.method.strategies[1] = strategy
    p.method.threshold[1] = threshold
    p.method.raiseTemperature[1] = raising
    p.method.Reset()
    p.method.Start()
    if raising == 0:
        instr = "raise_"
    else:
        instr = ""
    p.Serialize("results/temperature_test_" + instr + str(v) + "_vertices_" + str(i) + "_" + \
        p.method.strategies[0][strategy] + "_" + p.method.threshold[0][threshold]  + ".proj")
    return p.method.trace.getBest()[1]

# Run tests with all strategies and temperature functions
p = Project("program.xml", "temperature test") 
for v in [10,20,30,40,50]:
    res = ""
    for i in range(100):       
        p.GenerateRandomSystem({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
        print (v, i)
        for s in [0, 1, 2]:
            res += str(i) + ";"
            for t in [0, 1, 2]:
                for r in [0, 1]:
                    try:
                        best = run(p, v, i, s, t)
                        res += str(best["processors"]) + ";" + str(best["time"]) + ";"
                    except:
                        res += "ERROR;ERROR;"
        res += "\n"
    f = open("results_temperature_raise_" + str(v) + ".txt", "w")
    f.write(res)
    f.close()

# Compare temperatures with each other
p1 = Project("program.xml", "temperature test")
p2 = Project("program.xml", "temperature test")
for y in [["Bolzmann", "Cauchy"],["Bolzmann", "Combined"],["Cauchy","Combined"]]:
    res = {}
    s1 = y[0]
    s2 = y[1]
    for i in range(2, 5):
        for j in range(1, 5):
            name = "results/temperature_test_" + str(i*10) + "_vertices_"+ str(j) + "_Idle time reduction_"
            bolz = name + s1 + ".proj"
            cauchy = name + s2 + ".proj"
        
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
            worstproc = worst.method.trace.getBest()[1]["processors"] 
            best.method.ScrollTrace(best.method.trace.best - best.method.trace.current)
            while best.method.trace.getCurrent()[1]["processors"] != worstproc:
                best.method.ScrollTrace(-1)
            bestiter = best.method.trace.current
            result = int(float(bestiter) / float(worstiter) * sign * 100.0)
            if result in res:
                res[result] += 1
            else:
                res[result] = 1

    f = open(s1 + "_" + s2 + ".txt", "w")
    for k in res.keys():
        f.write(str(k) + "," + str(res[k]) + "\n")
    f.close()

# Compare initial temperatures
def runinit(p, temp, i, strategy, threshold):  
    p.method.strategies[1] = strategy
    p.method.threshold[1] = threshold
    p.initialTemperature = tempz
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
                    best = runinit(p, init * 10.0, i, s, t)
                    res += str(best["processors"]) + ";" + str(best["time"]) + ";"
                except:
                    res += "ERROR;ERROR;"
        res += "\n"
f = open("results_temperature_initial.txt", "w")
f.write(res)
f.close()