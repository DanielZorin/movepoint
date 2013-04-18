from Schedules.System import *
from Schedules.SimpleInterpreter import *
from SchedulerGUI.Project import Project
from plugins.Random import *
import time

s = System("program.xml")
gen = RandomProgramGenerator()
gen.n = 1000
gen.Generate(s)
int = SimpleInterpreter()
s.schedule.SetToDefault()
t0 = time.clock()
x0 = int.Interpret(s.schedule)
print(x0, time.clock() - t0)
#for v in int.executionTimes.keys():
#    print (v.v.number, int.executionTimes[v])
'''for v in int.delays:
    print (v[0].v.number, v[1])
for v in int.idletimes:
    print(v[0][0].number, v[0][1], v[1])'''
t0 = time.clock()
x1 = int.Interpret2(s.schedule)
print(x1, time.clock() - t0)
#for v in int.executionTimes.keys():
#    print (v.v.number, int.executionTimes[v])
'''for v in int.delays:
    print (v[0].v.number, v[1])
for v in int.idletimes:
    print(v[0][0].number, v[0][1], v[1])'''
