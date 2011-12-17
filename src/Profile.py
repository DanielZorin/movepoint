'''
Created on 07.07.2011

@author: juan
'''
from Schedules.System import System
from Methods.Scheduling.SimulatedAnnealing import SimulatedAnnealing

import time
t0 = time.clock()
for i in range(1,11):
    for j in range(10):
        ss = System("program.xml")
        ss.GenerateRandom({"n":i*10, "t1":2, "t2":5, "v1":1, "v2":2, "tdir":2, "rdir":1})
        s = SimulatedAnnealing(ss)
        s.LoadConfig("config.xml")
        s.Start()
        t1 = time.clock() - t0
        n = i*10
        print("==================================================")
        print("%d\t%f\t%f\t%f\t%f" % (n, t1, t1/(n**1), t1/(n**2), t1/(n**3)))
        t0 = time.clock()