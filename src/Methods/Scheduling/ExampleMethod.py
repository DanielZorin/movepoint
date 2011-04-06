'''
Created on 07.11.2010

@author: juan
'''
from Schedules.Schedule import Schedule
from Schedules.Program import Program
from Core.Processor import Processor
import random

p = Program()
p.LoadFromXML("program2.xml")
s = Schedule(p, [Processor(0, 0.99)])
s.SetToDefault()
v1 = s.FindVertex(m=1)
v2 = s.FindVertex(m=2)
v3 = s.FindVertex(m=3)
v4 = s.FindVertex(m=4)
v5 = s.FindVertex(m=5)
s.AddVersion(v1.v)
s.AddVersion(v1.v)
s.AddVersion(v1.v)
print(s)
raise 8
s.MoveVertex(v2, v1.m, 2)
s.MoveVertex(v4, v1.m, 1)
s.MoveVertex(v2, v1.m, 1)
print(s.GetTime())
print(s.GetReliability())
print(s.GetProcessors())
#print(s)
fails = 0
for iter in range(1000):
    op = random.randint(1,5)
    if op == 1:
        proc = random.randint(0,len(s.processors)-1)
        if not s.AddProcessor(s.processors[proc]):
            fails += 1
    elif op == 2:
        proc = random.randint(0,len(s.processors)-1)
        if not s.DeleteProcessor(s.processors[proc]):
            fails += 1   
    elif op == 3:
        vers = random.randint(0,len(s.vertices)-1)
        if not s.AddVersion(s.vertices[vers].v):
            fails += 1
    elif op == 4:
        vers = random.randint(0,len(s.vertices)-1)
        if not s.DeleteVersion(s.vertices[vers].v):
            fails += 1  
    elif op == 5:
        s1 = s.vertices[random.randint(0,len(s.vertices)-1)]
        if random.random() > 0.5:
            m = s.processors[random.randint(0,len(s.processors)-1)]
            m_tasks = s.FindAllVertices(m=m)
            if m == s1.m:
                n = random.randint(1, len(m_tasks))
            else:
                n = random.randint(1, len(m_tasks)+1)
        else:
            m = s1.m
            m_tasks = s.FindAllVertices(m=m)
            n = random.randint(1, len(m_tasks))
        if not s.MoveVertex(s1, m, n):
            fails += 1

print("-----------------------------------------")    
if s.GetProcessorsWithoutDoubles() < 4:
    print(s)
    
print(s.GetTime())
print(s.GetReliability())
print(s.GetProcessors())