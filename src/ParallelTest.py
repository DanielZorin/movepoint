from Schedules.System import *
from Schedules.SimpleInterpreter import *
from SchedulerGUI.Project import Project
from SchedulerGUI.ParallelRunner import RunParallel
from plugins.Random import *
from Schedules.Metrics import HMetric
import time, multiprocessing, copy

def run(p, v, i, strategy):  
    p.method.algorithm.strategies[1] = strategy
    p.method.Reset()
    p.method.Start()
    p.Serialize("results/parallel_test_" + str(v) + "_vertices_" + str(i) + "_" + \
        p.method.algorithm.strategies[0][strategy]  + ".proj")
    return p.method.trace.getBest()[1]

def RunProcess(q, name, limits):
    p = Project(name, "")
    try:
        p.method.Reset(limits)
        p.method.Start(limits)
        q.put(p.method.trace.getBest()[1])
    except:
        q.put({"processors":-1, "time":-1})

if __name__ == '__main__':
    gen = RandomProgramGenerator()
    p = Project("program.xml", "temperature test")
    for n in range(3, 50):
        gen.n = n * 5
        gen.q = 0
        gen.Generate(p.method.system)
        for j in range(1, 101):
            for s in [0, 1, 2]:
                for count in [1, 3, 5, 7]:
                    try:
                        if count == 1:
                            run(p, n * 5, j, s)
                            p.method.ScrollTrace(p.method.trace.best - p.method.trace.current)
                            iter = p.method.trace.current
                            proc = p.method.trace.getBest()[1]["processors"]
                            time = p.method.trace.getBest()[1]["time"]
                        else:
                            limits = p.method.system.program.GenerateLimits(count)
                            p.method.system.Export(".tmp_parallel_run.xml")
                            threads = []
                            result_queue = multiprocessing.Queue()
                            for i in range(count):
                                t = multiprocessing.Process(target=RunProcess, args=(result_queue, ".tmp_parallel_run.xml", limits[i]))
                                threads.append(t)
                                t.start()
                            for t in threads:
                                t.join()
                            res = [result_queue.get() for t in threads]
                            proc = res[0]["processors"]
                            time = res[0]["time"]
                            for r in res:
                                if r["processors"] < proc:
                                    proc = r["processors"]
                                if r["processors"] == proc:
                                    if r["time"] < time:
                                        time = r["time"]
                    except:
                        iter = -1
                        proc = -1
                        time = -1
                    f = open("results_parallel.txt", "a")
                    f.write(str(n * 5) + ";" + str(j) + ";" + str(s) + ";" + str(count) + ";" + str(proc) + ";" + str(time) + "\n")
                    f.close()
