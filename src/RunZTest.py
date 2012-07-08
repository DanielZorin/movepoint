'''
Created on 01.03.2011

@author: juan
'''

from Schedules.System import *
from Methods.Scheduling.Interface import RunMixed, RunIdle, RunDelay, RunRandomAndNormal
from Tests.ZTest import ZTest
        
s = System("program.xml")

# Test suboptimal
results = {"mixed":[], "delay":[], "idle":[]}    
for v in [10,20,30,40,50]:
    sample = []
    for i in range(100):
        s.GenerateRandom({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
        cur = copy.deepcopy(s)
        sample.append(cur)
    
    z = ZTest(RunMixed, sample, checkSubOptimal, "subopt_" + str(v) + "_mixed.txt")
    res = z.Test(0.9)
    results["mixed"].append(res)
    z = ZTest(RunIdle, sample, checkSubOptimal, "subopt_" + str(v) + "_idle.txt")
    res = z.Test(0.9)
    results["idle"].append(res)
    z = ZTest(RunDelay, sample, checkSubOptimal, "subopt_" + str(v) + "_delay.txt")
    res = z.Test(0.9)
    results["delay"].append(res)
f = open("subopt_final_results.txt", "w")
f.write(str(results))
    
# Test one
results = {"mixed":[], "delay":[], "idle":[]}
for v in [10,20,30,40,50]:
    sample = []
    for i in range(100):
        s.GenerateRandom({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":3, "rdir":3})
        cur = copy.deepcopy(s)
        sample.append(cur)
    
    z = ZTest(RunMixed, sample, checkOne, "one_" + str(v) + "_mixed.txt")
    res = z.Test(0.9)
    results["mixed"].append(res)
    z = ZTest(RunIdle, sample, checkOne, "one_" + str(v) + "_idle.txt")
    res = z.Test(0.9)
    results["idle"].append(res)
    z = ZTest(RunDelay, sample, checkOne, "one_" + str(v) + "_delay.txt")
    res = z.Test(0.9)
    results["delay"].append(res)
f = open("one_final_results.txt", "w")
f.write(str(results))
    
# Test local optimal 
results = {"mixed":[], "delay":[], "idle":[]}
for v in [10,20,30,40,50]:
    sample = []
    for i in range(100):
        s.GenerateRandom({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
        cur = copy.deepcopy(s)
        sample.append(cur)
    
    z = ZTest(RunMixed, sample, checkLocalOpt, "localopt_" + str(v) + "_mixed.txt")
    res = z.Test(0.9)
    results["mixed"].append(res)
    z = ZTest(RunIdle, sample, checkLocalOpt, "localopt_" + str(v) + "_idle.txt")
    res = z.Test(0.9)
    results["idle"].append(res)
    z = ZTest(RunDelay, sample, checkLocalOpt, "localopt_" + str(v) + "_delay.txt")
    res = z.Test(0.9)
    results["delay"].append(res)
f = open("localopt_final_results.txt", "w")
f.write(str(results))

# Compare with RandomSimulatedAnnealing
results = {"three":[]}
for v in [10,20,30,40,50]:
    sample = []
    for i in range(100):
        s.GenerateRandom({"n":v, "t1":2, "t2":6, "v1":1, "v2":2, "tdir":2, "rdir":2})
        cur = copy.deepcopy(s)
        sample.append(cur)
    
    z = ZTest(RunRandomAndNormal, sample, compare, "compare_" + str(v) + "_three.txt")
    res = z.Test(0.9)
    results["three"].append(res)
f = open("compare_final_results.txt", "w")
f.write(str(results))