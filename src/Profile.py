'''
Created on 07.07.2011

@author: juan
'''
from Schedules.System import System
from Methods.Scheduling.SimulatedAnnealing import SimulatedAnnealing
'''
i = 0
while True:
    print(i)
    i += 1
    ss = System("program.xml")
    ss.GenerateRandom({"n":10, "t1":2, "t2":5, "v1":1, "v2":2, "tdir":2, "rdir":3})
    s = SimulatedAnnealing(ss)
    s.LoadConfig("config.xml")
    s.Start()
exit()'''

import time
t0 = time.clock()
res = ""
for i in range(1,11):
    for j in range(1):
        ss = System("program.xml")
        ss.GenerateRandom({"n":i*10, "t1":2, "t2":5, "v1":1, "v2":2, "tdir":2, "rdir":3})
        s = SimulatedAnnealing(ss)
        s.Start()
        t1 = time.clock() - t0
        n = i*10
        res += "%d\t%f\t%f\t%f\t%f\n" % (n, t1, t1/(n**1), t1/(n**2), t1/(n**3))
        t0 = time.clock()
        print(res)
print(res)