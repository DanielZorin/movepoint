from Schedules.System import *
from SchedulerGUI.Project import Project
from plugins.Random import *

gen = RandomProgramGenerator()

def run(p, v, i, strategy):  
    p.method.algorithm.strategies[1] = strategy
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/final_test_" + str(v) + "_vertices_" + str(i) + "_" + \
        p.method.algorithm.strategies[0][strategy]  + ".proj")
    return p.method.trace.getBest()[1]

p = Project("program.xml", "temperature test")
for i in range(27, 50):
    print (i*5)
    gen.n = i * 5
    #Unlimited time, limited reliability
    '''gen.tdir[1] = 3
    gen.rdir[1] = 1
    gen.Generate(p.method.system)
    for j in range(1, 100):
        for s in [0, 1, 2, 3]:
            #try:
            run(p, i * 5, j, s)
            p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
            iter = p.method.trace.current
            proc = p.method.trace.getBest()[1]["processors"]
            #except:
            #    iter = -1
            #    proc = -1
            f = open("final_results.txt", "a")
            f.write("unlimited-time;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()
    # Both unlimited
    gen.tdir[1] = 3
    gen.rdir[1] = 3
    gen.Generate(p.method.system)
    for j in range(1, 101):
        for s in [0, 1, 2, 3]:
            try:
                run(p, i * 5, j, s)
                p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                iter = p.method.trace.current
                proc = p.method.trace.getBest()[1]["processors"]
            except:
                iter = -1
                proc = -1
            f = open("final_results.txt", "a")
            f.write("unlimited-both;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()
    #Impossible time
    gen.tdir[1] = 0
    gen.rdir[1] = 3
    gen.Generate(p.method.system)
    for j in range(1, 101):
        for s in [0, 1, 2, 3]:
            try:
                run(p, i * 5, j, s)
                p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                iter = p.method.trace.current
                proc = p.method.trace.getBest()[1]["processors"]
            except:
                iter = -1
                proc = -1
            f = open("final_results.txt", "a")
            f.write("impossible-time;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()'''
    # Very limited time
    gen.tdir[1] = 1
    gen.rdir[1] = 3
    gen.Generate(p.method.system)
    for j in range(1, 101):
        for s in [0, 1, 2, 3]:
            try:
                run(p, i * 5, j, s)
                p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                iter = p.method.trace.current
                proc = p.method.trace.getBest()[1]["processors"]
            except:
                iter = -1
                proc = -1
            f = open("final_results.txt", "a")
            f.write("limited-time;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()
    # No edges
    gen.tdir[1] = 2
    gen.rdir[1] = 2
    gen.q = 0.0
    gen.Generate(p.method.system)
    for j in range(1, 101):
        for s in [0, 1, 2, 3]:
            try:
                run(p, i * 5, j, s)
                p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                iter = p.method.trace.current
                proc = p.method.trace.getBest()[1]["processors"]
            except:
                iter = -1
                proc = -1
            f = open("final_results.txt", "a")
            f.write("no-edges;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()

    # Medium edges
    gen.q = 0.5
    gen.Generate(p.method.system)
    for j in range(1, 101):
        for s in [0, 1, 2, 3]:
            try:
                run(p, i * 5, j, s)
                p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                iter = p.method.trace.current
                proc = p.method.trace.getBest()[1]["processors"]
            except:
                iter = -1
                proc = -1
            f = open("final_results.txt", "a")
            f.write("medium-edges;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()

    # Many edges
    gen.tdir[1] = 2
    gen.rdir[1] = 2
    gen.q = 1.0
    gen.Generate(p.method.system)
    for j in range(1, 101):
        for s in [0, 1, 2, 3]:
            try:
                run(p, i * 5, j, s)
                p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                iter = p.method.trace.current
                proc = p.method.trace.getBest()[1]["processors"]
            except:
                iter = -1
                proc = -1
            f = open("final_results.txt", "a")
            f.write("many-edges;" + str(i * 5) + ";" + str(j) + ";" + str(s) + ";" + str(proc) + ";" + str(iter) + "\n")
            f.close()
