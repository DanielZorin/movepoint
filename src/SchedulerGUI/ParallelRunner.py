from Schedules.SimpleInterpreter import SimpleInterpreter
from Schedules.System import *
from SchedulerGUI.Project import Project
import time, multiprocessing, copy

def RunParallel(project, count):
    def RunProcess(q, name, limits):
        p = Project(name, "")
        p.method.Reset(limits)
        p.method.Start(limits)
        q.put(p.method.trace.getBest()[1])

    p = project
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
    results = [result_queue.get() for t in threads]
    return results