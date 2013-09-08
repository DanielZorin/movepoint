from Schedules.System import *
from Schedules.SimpleInterpreter import *
from SchedulerGUI.Project import Project
from plugins.Random import *
from Schedules.Metrics import HMetric
import time, multiprocessing, copy

count = 5

def RunProcess(q, name, limits):
    p = Project(name, "temperature test")
    p.method.Reset(limits)
    p.method.Start(limits)
    q.put(p.method.trace.getBest()[1])

if __name__ == '__main__':
    gen = RandomProgramGenerator()
    gen.n = 20
    p = Project("program.xml", "temperature test")
    gen.Generate(p.method.system)
    limits = p.method.system.program.GenerateLimits(count)
    p.method.system.Export("test.xml")
    threads = []
    result_queue = multiprocessing.Queue()
    for i in range(count):
        t = multiprocessing.Process(target=RunProcess, args=(result_queue, "test.xml", limits[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    results = [result_queue.get() for t in threads]
    print (results)
    x = 99
