'''
Created on 17.03.2011

@author: juan
'''

from Schedules.System import System
from Methods.Scheduling.Exceptions import SchedulerFileException, SchedulerXmlException
import xml.dom.minidom
import random
import copy

class RandomSimulatedAnnealing(object):

    # System, program and schedule to optimize
    system = None
    
    # Current iteration and temperature (see Simulated Annealing)
    iteration = 0
    temperature = 0
    
    # Operation priorities (dictionary operation name:priority)
    opt_reliability = { "time-normal":{}, "time-exceed":{} }
    opt_time = { "time-normal":{}, "time-exceed":{} }
    
    # Parameters of the current approximation
    curTime = None
    curRel = None
    curProc = None
    
    # Current approximation. A copy is saved here, and all changes are applied to the original
    oldSchedule = None
    
    # Current best solution and its characteristics
    bestSchedule = None
    bestTime = None
    bestRel = None
    bestProc = None
    
    # Number of iteration is 10 * number of vertices
    numberOfIterations = 0
    
    # Here we keep the last operation. It's used in GUI
    lastOperation = {"operation": "",
                        "parameters": [],
                        "result": False}
    
    # Debug feature: print debug information
    writeLog = False

    def __init__(self, system):
        self.iteration = 0
        self.system = system
        self.numberOfIterations = len(self.system.program.vertices) * 1
        self.temperature = 0
    
    def write(self, *text):
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            print(" ".join(res))
            
    def ChangeSystem(self, s):
        self.system = s
      
    def Serialize(self):
        return {"opt_reliability": self.opt_reliability,
            "opt_time": self.opt_time,
            "numberOfIterations":self.numberOfIterations}
        
    def Deserialize(self, dict):
        self.opt_reliability = dict["opt_reliability"]
        self.opt_time = dict["opt_time"]
        self.numberOfIterations = dict["numberOfIterations"]
    
    def Reset(self):
        self.system.schedule.SetToDefault()
        self.curTime = self.system.schedule.Interpret()
        self.curRel = self.system.schedule.GetReliability()
        self.curProc = self.system.schedule.GetProcessors()
        self.bestProc = self.curProc
        self.bestTime = self.curTime
        self.bestRel = self.curRel
        self.bestSchedule = copy.deepcopy(self.system.schedule)
    
    # TODO: clean up this function    
    def Start(self):
        self.bestSchedule = self.system.schedule
        self.curTime = self.system.schedule.Interpret()
        self.curRel = self.system.schedule.GetReliability()
        self.curProc = self.system.schedule.GetProcessors()
        self.bestProc = self.curProc
        self.bestTime = self.curTime
        self.bestRel = self.curRel
        while self.iteration < self.numberOfIterations:
            self.Step()
            self.iteration += 1
            if (self.curProc == 1) and (self.curTime <= self.system.tdir) and (self.curRel >= self.system.rdir):
                print ("Early end: ", self.iteration)
                return self.system.schedule
            #print(self.iteration)         
        self.system.schedule = self.bestSchedule
        self.curTime = self.bestTime
        self.curRel = self.bestRel
        self.curProc = self.bestProc
        return self.system.schedule
            
    def Step(self):
        self.write("---------------------------")
        self.write("iteration ", self.iteration)
        self.lastOperation = {}
        self.temperature += 1
        op = self._chooseOperation()
        #TODO: reconsider this implementation: maybe we should apply changes to the copy?
        self.oldSchedule = copy.deepcopy(self.system.schedule) 
        self._applyOperation(op)
        self._selectNewSchedule()
     
    # Dict is key:probability. A key is chosen according to this distribution
    def _chooseRandomKey(self, dict):
        v = random.random()
        sum = 0.0
        # Sum can be less than 1 if some operations are impossible on the current step.
        for k in dict.keys():
            sum += dict[k]
        v = v * sum
        sum = 0.0
        for k in dict.keys():
            if v < sum + dict[k]:
                return k
            sum += dict[k]
        
       
    def _chooseOperation(self):
        self.curTime = self.system.schedule.Interpret()
        self.curRel = self.system.schedule.GetReliability()
        self.curProc = self.system.schedule.GetProcessors()
        if self.curRel < self.system.rdir:
            if self.curTime > self.system.tdir:
                vector = self.opt_reliability["time-exceed"]
            else:
                vector = self.opt_reliability["time-normal"]
        else:
            if self.curTime > self.system.tdir:
                vector = self.opt_time["time-exceed"]
            else:
                vector = self.opt_time["time-normal"]
        
        # Delete impossible operations
        if not self.system.schedule.CanDeleteProcessor():
            vector.pop("DeleteProcessor", True)
            
        if not self.system.schedule.CanDeleteVersions():
            vector.pop("DeleteVersion", True)
            
        if not self.system.schedule.CanAddVersions():
            vector.pop("AddVersion", True)
          
        return self._chooseRandomKey(vector)
        
        # Delete impossible operations
        if not self.system.schedule.CanDeleteProcessor():
            vector.pop("DeleteProcessor", True)
            
        if not self.system.schedule.CanDeleteVersions():
            vector.pop("DeleteVersion", True)
            
        if not self.system.schedule.CanAddVersions():
            vector.pop("AddVersion", True)
          
        return self._chooseRandomKey(vector)
    
    # Selects parameters for the operation and applies it whenever possible
    def _applyOperation(self, op):
        self.write(op)
        self.lastOperation["operation"] = op
        if op == "AddProcessor":
            proc = list(self.system.schedule.processors)
            proc.sort(key=lambda x: x.reserves)
            total = sum([p.reserves for p in proc])
            dict = {}
            for p in proc:
                dict[p] = float(p.reserves)/float(total)
            m = self._chooseRandomKey(dict)
            self.system.schedule.AddProcessor(m)
            self.lastOperation["parameters"] = [m.number]
            self.write(m)
        elif op == "DeleteProcessor":
            proc = list(self.system.schedule.processors)
            proc.sort(key=lambda x: x.reserves)
            total = sum([p.reserves for p in list(filter(lambda p: p.reserves > 1, proc))])
            dict = {}
            for p in proc:
                if p.reserves > 1:
                    dict[p] = float(p.reserves)/float(total)
            if len(dict.keys()) > 0:
                m = self._chooseRandomKey(dict)
                self.system.schedule.DeleteProcessor(m)
                self.lastOperation["parameters"] = [m.number]
                self.write(m)
                
        elif op == "AddVersion":
            vers = list(filter(lambda v: len(v.versions) >= len(self.system.schedule.FindAllVertices(v=v)) + 2, \
                self.system.schedule.program.vertices))
            vers.sort(key=lambda v: len(v.versions))
            if len(vers) != 0:
                self.system.schedule.AddVersion(vers[0])
                self.lastOperation["parameters"] = [vers[0].number]
                self.write(vers[0].number)                         
        elif op == "DeleteVersion":
            vers = list(filter(lambda v: len(self.system.schedule.FindAllVertices(v=v)) > 1, \
                self.system.schedule.program.vertices))
            vers.sort(key=lambda v: len(v.versions))
            if len(vers) != 0:
                self.system.schedule.DeleteVersion(vers[len(vers)-1]) 
                self.lastOperation["parameters"] = [vers[0].number]  
                self.write(vers[len(vers)-1].number)
                
        elif op == "MoveVertex":
            s = self.system.schedule
            s1 = None
            target_proc = None
            target_pos = None
            
            if random.random() < 0.3 and self.curProc > 1:
                mini = len(s.vertices)
                proc = None
                for m in s.processors:
                    f = len(s.FindAllVertices(m=m))
                    if f < mini:
                        mini = f
                        proc = m
                ch = s.FindAllVertices(m=proc)
                for s1 in ch:  
                    while True:
                        num = random.randint(0, len(s.processors)-1)
                        if s.processors[num] != proc:
                            target_proc = s.processors[num]
                            target_pos = random.randint(1, len(s.FindAllVertices(m=s.processors[num]))+1)                                       
                            if target_proc == None:
                                self.lastOperation["parameters"] = [s1.v.number, s1.k.number, -1, target_pos]
                            else:
                                self.lastOperation["parameters"] = [s1.v.number, s1.k.number, target_proc.number, target_pos]
                            if s.MoveVertex(s1, target_proc, target_pos):
                                break
                    return    
            
            s1 = s.vertices[random.randint(0, len(s.vertices)-1)]
            s2 = s.vertices[random.randint(0, len(s.vertices)-1)]
            target_proc = s2.m
            target_pos = s2.n
            if random.random() < 0.1:
                target_proc = None
                target_pos = 1
                
            self.write(s1.v.number, s1.m.number, s1.n, target_proc, target_pos)
            if target_proc == None:
                self.lastOperation["parameters"] = [s1.v.number, s1.k.number, -1, target_pos]
            else:
                self.lastOperation["parameters"] = [s1.v.number, s1.k.number, target_proc.number, target_pos]
            if not s.MoveVertex(s1, target_proc, target_pos):
                # TODO: handle this situation
                pass

    
    def _selectNewSchedule(self):
        def accept():
            self.write("Accept")
            self.lastOperation["result"] = True
            self.curTime = new_time
            self.curRel = new_rel
            self.curProc = new_proc
            if self.curTime <= self.system.tdir and self.curRel >= self.system.rdir:
                if self.bestProc == None or self.curProc < self.bestProc or (self.curProc == self.bestProc and self.curTime < self.bestTime):
                    self.bestProc = self.curProc
                    self.bestTime = self.curTime
                    self.bestRel = self.curRel
                    self.bestSchedule = copy.deepcopy(self.system.schedule)
                    self.write("BEST SOLUTION:", self.bestTime, self.bestProc, self.system.tdir)
            
        def refuse():  
            self.write("Refuse")
            self.lastOperation["result"] = False
            self.system.schedule = self.oldSchedule              

        new_time = self.system.schedule.Interpret()
        new_rel = self.system.schedule.GetReliability()
        new_proc = self.system.schedule.GetProcessors()
        
        self.write("Old: ", self.curTime, self.curRel, self.curProc)    
        self.write("New: ", new_time, new_rel, new_proc)   
        if (self.curProc > new_proc) or (self.curTime > new_time) or (self.curRel < new_rel):
            accept()
        else:
            refuse()