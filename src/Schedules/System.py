'''
Created on 10.11.2010

@author: juan
'''

from Schedules.Program import Program
from Core.Processor import Processor
from Schedules.Schedule import Schedule
import xml.dom.minidom, copy

class System(object):

    program = None
    processors = []
    schedule = None
    tdir = 0
    rdir = 0.0
    
    defaultSettings = {"n":20, 
                    "t1":1, 
                    "t2":10, 
                    "v1":1, 
                    "v2":5}
    
    def __init__(self, filename=""):
        if filename == "":
            return
        self.program = Program(filename)
        self.LoadProcessors(filename)
        # TODO: exception in case of any errors         
        self.schedule = Schedule(self.program, self.processors)
        self.schedule.SetToDefault()
        
    def LoadProcessors(self, filename):
        f = open(filename)
        dom = xml.dom.minidom.parse(f)
        
        for node in dom.childNodes:
            if node.tagName == "program":
                self.tdir = int(node.getAttribute("tdir"))
                self.rdir = float(node.getAttribute("rdir"))
                #Parse vertices
                for vertex in node.childNodes:
                    if vertex.nodeName == "processor":
                        speed = int(vertex.getAttribute("speed"))
                        rel = float(vertex.getAttribute("reliability"))
                        p = Processor(0, rel, speed)
                        self.processors.append(p)
        f.close()

            
    def LocalOptimal(self):
        onestep = []
        
        for i in range(len(list(self.schedule.processors))):
            sch1 = copy.deepcopy(self.schedule)
            if sch1.AddProcessor(sch1.processors[i]):
                onestep.append(sch1)
            sch2 = copy.deepcopy(self.schedule)
            if sch2.DeleteProcessor(sch2.processors[i]):
                onestep.append(sch2)
        
        for i in range(len(self.schedule.vertices)):
            sch1 = copy.deepcopy(self.schedule)
            if sch1.AddVersion(sch1.vertices[i].v):
                onestep.append(sch1)
            sch2 = copy.deepcopy(self.schedule)
            if sch2.DeleteVersion(sch2.vertices[i].v):
                onestep.append(sch2)
        
        for i in range(len(self.schedule.vertices)):
            for j in range(len(self.schedule.vertices)):
                sch = copy.deepcopy(self.schedule)
                if sch.MoveVertex(sch.vertices[i], sch.vertices[j].m, sch.vertices[j].n):
                    onestep.append(sch)
            for j in range(len(list(self.schedule.processors))):
                sch = copy.deepcopy(self.schedule)
                if sch.MoveVertex(sch.vertices[i], sch.processors[j], len(self.schedule.FindAllVertices(m=sch.processors[j])) + 1):
                    onestep.append(sch)
        
        tcur = self.schedule.Interpret()
        rcur = self.schedule.GetReliability()
        pcur = self.schedule.GetProcessors()
        for sch in onestep:
            t = sch.Interpret()
            r = sch.GetReliability()
            p = sch.GetProcessors()
            #print(t, tcur, r, rcur, p, pcur)
            if not (p >= pcur or t > self.tdir or r < self.rdir):
                return False
        return True
     
    # Generates a random system
    # Now that the processors are fixed it merely creates a random program  
    def GenerateRandom(self, params):
        self.program = Program("")
        self.program.GenerateRandom(params)
        self.schedule = Schedule(self.program, self.processors)       
        self.schedule.SetToDefault()
        self.rdir = 0.0#self.schedule.GetReliability() * 1.05
        maxchain = self.program.FindMaxChain(True) 
        ss = sum([v.time for v in self.program.vertices])     
        # Types of constraints:
        # 0 = Impossible
        # 1 = Strict
        # 2 = Normal
        # 3 = Nonexisting
        # Numbers are used because strings in GUI can be translated
        self.tdir = {
                     0: 0,
                     1: maxchain,
                     2: int(maxchain + (ss - maxchain) / 3),
                     # TODO: replace this workaround
                     3: int(maxchain * 1000)
                     }[params["tdir"]]
                     
        relstrict, relnormal = self.program.GetReliabilityBoundaries()
        # TODO: this only works now that we have only one processor
        procrel = self.processors[0].reliability ** params["n"]
        relstrict *= procrel
        relnormal *= procrel
        self.rdir = {
                     0: 1.0,
                     1: relstrict,
                     2: relnormal,
                     3: 0.0
                     }[params["rdir"]]
                     
# Auxiliary functions used for testing.
# TODO: maybe move them somewhere
                     
def checkSubOptimal(t):
    ss = sum([v.time for v in t.program.vertices])
    print("Results:", t.schedule.GetProcessors(), t.schedule.Interpret(), t.tdir, ss, int(ss / t.tdir) + 1)
    if t.schedule.GetProcessors() <= int(ss / t.tdir) + 2:
        return 1
    else:
        return 0

def checkLocalOpt(t):
    if t.LocalOptimal():
        print("okay")
        return 1
    else:
        return 0

def checkOne(t):
    if t.schedule.GetProcessors() == 1:
        return 1
    else:
        return 0

# Compare the results of two methods passed as a tuple    
def compare(t):
    print("Results:", t[0].schedule.GetProcessors(), t[1].schedule.GetProcessors(),
          t[0].schedule.Interpret(), t[1].schedule.Interpret())
    if t[0].schedule.GetProcessors() <= t[1].schedule.GetProcessors():
        return 1
    else:
        return 0