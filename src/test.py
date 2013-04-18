from Schedules.System import *
from Schedules.SimpleInterpreter import *
from SchedulerGUI.Project import Project
from plugins.Random import *
import time

s = System("program.xml")
gen = RandomProgramGenerator()
gen.n = 3000
gen.Generate(s)
int = SimpleInterpreter()
s.schedule.SetToDefault()
t0 = time.clock()
x0 = int.Interpret2(s.schedule)
print(x0, time.clock() - t0)
#for v in int.executionTimes.keys():
#    print (v.v.number, int.executionTimes[v])
t0 = time.clock()
x1 = int.Interpret(s.schedule)
print(x1, time.clock() - t0)
#for v in int.executionTimes.keys():
#    print (v.v.number, int.executionTimes[v])
z = 5