from Schedules.System import *
from SchedulerGUI.Project import Project

# Compare temperatures with each other
p1 = Project("program.xml", "temperature test")
p2 = Project("program.xml", "temperature test")
for y in [["Idle time reduction", "Delay reduction"],["Idle time reduction", "Mixed"],["Delay reduction","Mixed"]]:
    res = {}
    s1 = y[0]
    s2 = y[1]
    for i in range(1, 16):
        for j in range(1, 100):
            name = "results/temperature_test_" + str(i*10) + "_vertices_"+ str(j) + "_"
            bolz = name + s1 + "_Bolzmann.proj"
            cauchy = name + s2 + "_Bolzmann.proj"
        
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
    p.Serialize("results/strategies_test_" + instr + str(v) + "_vertices_" + str(i) + "_" + \
        p.method.strategies[0][strategy] + "_" + p.method.threshold[0][threshold]  + ".proj")
    return p.method.trace.getBest()[1]

# Run tests with all strategies and temperature functions
p = Project("program.xml", "temperature test") 
for v in [10,20,30,40,50,60,70,80,90,100]:
    res = ""  
    p.GenerateRandomSystem({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
    for i in range(100):
        print (v, i)
        res += str(i) + ";"
        for s in [0, 1, 2]:
            for t in [0]:
                for r in [0]:
                    try:
                        best = run(p, v, i, s, t, r)
                        res += str(best["processors"]) + ";"
                    except:
                        res += "ERROR;"
        res += "\n"
    f = open("results_strategies_stability_" + str(v) + ".txt", "w")
    f.write(res)
    f.close()