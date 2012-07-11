'''
Created on 10.11.2010

@author: juan
'''

from Schedules.System import System
from Schedules.Threshold import Threshold
from Schedules.Operation import *
from Methods.Scheduling.Exceptions import SchedulerFileException, SchedulerXmlException
import xml.dom.minidom
import random, math
import logging

class SimulatedAnnealing(object):
    ''' Simulated Annealing method adapted for scheduling.
    
    .. warning:: Write details here'''
    
    system = None
    ''' System, program and schedule to optimize'''
    
    iteration = 1
    ''' Current iteration (see Simulated Annealing) '''
    
    opt_reliability = { "time-normal":{"AddVersion":0.5, "AddProcessor":0.33, "MoveVertex":0.16}, 
                        "time-exceed":{"AddVersion":0.33, "AddProcessor":0.5, "MoveVertex":0.16} }
    opt_time = { "time-normal":{"DeleteVersion":0.33, "DeleteProcessor":0.5, "MoveVertex":0.5}, 
                 "time-exceed":{"DeleteVersion":0.5, "DeleteProcessor":0.33, "MoveVertex":0.5} }
    ''' Operation priorities (dictionary operation_name:priority) '''
    
    choice_vertices = 5
    ''' Maximum number of vertices among which the parameters for "MoveVertex" are chosen '''
    
    choice_places = 5
    ''' Maximum number of places among which the parameters for "MoveVertex" are chosen '''
    
    strategies = [["Idle time reduction", "Delay reduction", "Mixed"], 0]
    ''' Used strategies for MoveVertex and their probabilities '''

    threshold = [["Bolzmann", "Cauchy", "Combined"], 0]
    
    oldSchedule = None
    ''' Current approximation. A copy is saved here, and all changes are applied to the original '''
    
    numberOfIterations = 0
    ''' Number of iteration is 10 * number of vertices '''
    
    lastOperation = VoidOperation()
    ''' Here we keep the info about the last operation. It's used in GUI '''
    
    trace = Trace()
    
    writeLog = False
    ''' Debug feature: print debug information '''
    
    multioperation = False

    initialTemperature = 100.0

    def __init__(self, system):
        self.iteration = 1
        self.system = system
        self.numberOfIterations = len(self.system.program.vertices) * 10 + 1
        logging.basicConfig(level=logging.DEBUG)
        self._prepare()
    
    def write(self, *text):
        ''' Print debug information'''
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            logger = logging.getLogger('SimulatedAnnealing')
            logger.debug(" ".join(res))
    
    def ChangeSystem(self, s):
        ''' Replace the system'''
        self.numberOfIterations = len(self.system.program.vertices) * 10
        self.system = s
        self._prepare()
    
    def Reset(self):
        ''' Resets the method to the zero iteration'''
        self.system.schedule.SetToDefault()
        self.numberOfIterations = 10 * len(self.system.program.vertices)
        self._prepare()
    
    def _prepare(self):
        self.trace.clear()
        self.lastOperation = VoidOperation()
        data = {"time":self.system.schedule.Interpret(),
                "reliability":self.system.schedule.GetReliability(),
                "processors":self.system.schedule.GetProcessors()
                }
        self.trace.addStep(self.lastOperation, data)
        self.trace.setBest(0)
        
    def Start(self):
        ''' Runs the algorithm with the given number of iterations'''
        self.iteration = 1
        while self.iteration <= self.numberOfIterations:
            #print(self.iteration)
            self.Step()
            self.iteration += 1
            if (self.trace.getLast()[1]["processors"] == 1) and \
                (self.trace.getLast()[1]["time"]  <= self.system.tdir) and \
                (self.trace.getLast()[1]["reliability"]  >= self.system.rdir):
                self.write("Early end: ", self.iteration)
                return  
        return    
            
    def Step(self):
        ''' Makes a single iteration of the algorithm'''
        self.write("---------------------------")
        self.write("iteration ", self.iteration)
        self.lastOperation = VoidOperation()
        op = self._chooseOperation()
        self._applyOperation(op)
        self._selectNewSchedule()

    def ScrollTrace(self, diff):
        ''' Scrolls diff operations along the trace'''
        if diff == 0:
            return
        if diff > 0:
            if self.trace.current + diff >= self.trace.length():
                diff = self.trace.length() - self.trace.current - 1
            for i in range(diff):
                self.trace.current += 1
                op = self.trace.getCurrent()
                self.system.schedule.ApplyOperation(op[0])
        if diff < 0:
            if self.trace.current + diff < 0:
                diff = -self.trace.current
            for i in range(-diff):
                op = self.trace.getCurrent()
                self.system.schedule.ApplyOperation(op[0].Reverse())
                self.trace.current -= 1

    def ManualStep(self, op, **params):
        ''' Callback for applying operations from the outside of this class, i.e. when the operation is defined by GUI'''
        if op == "MoveVertex":
            v = params["v"]
            n1 = params["n1"]
            n2 = params["n2"]
            m2 = params["m2"]
            res = self.system.schedule.TryMoveVertex(v, n1, m2, n2)
            if res != True:
                return res
            else:
                self.lastOperation = MoveVertex(v, v.m, n1, m2, n2)
                self.system.schedule.ApplyOperation(self.lastOperation)
        elif op == "AddProcessor":
            m = params["m"]
            self.lastOperation = AddProcessor(m)
            self.system.schedule.ApplyOperation(self.lastOperation)
        elif op == "DeleteProcessor":
            m = params["m"]
            self.lastOperation = DeleteProcessor(m)
            self.system.schedule.ApplyOperation(self.lastOperation)
        elif op == "AddVersion":
            v = params["v"]
            newproc = self.system.schedule.AddVersion(v)
            self.lastOperation = AddVersion(v, newproc, 1, newproc, 2)
        elif op == "DeleteVersion":
            v = params["v"]
            (m1, m2, n1, n2) = self.system.schedule.DeleteVersion(v) 
            self.lastOperation = DeleteVersion(v, m1, n1, m2, n2)
        
        cur = self.trace.getLast()[1]
        curTime = cur["time"]
        curRel = cur["reliability"]
        curProc = cur["processors"]
        self.lastOperation.result = True
        new_time = self.system.schedule.Interpret()
        new_rel = self.system.schedule.GetReliability()
        new_proc = self.system.schedule.GetProcessors()
        self.trace.deleteTail()
        self.trace.addStep(self.lastOperation, {"time":new_time, "reliability":new_rel, "processors":new_proc})
        best = self.trace.ops[0][1]
        bestindex = 0
        for i in range(1, self.trace.length()):
            cur = self.trace.ops[i][1]
            if cur["time"] <= self.system.tdir and cur["reliability"] >= self.system.rdir:
                if cur["processors"] < best["processors"] or (cur["processors"] == best["processors"] and cur["time"] < best["time"]):
                    bestindex = i
                    best = cur
        self.trace.setBest(bestindex)
        return True
   
    def _chooseRandomKey(self, dict):
        ''' Dict is key:probability. A key is chosen according to this distribution'''
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
        if self.trace.getLast()[1]["reliability"]  < self.system.rdir:
            if self.trace.getLast()[1]["time"] > self.system.tdir:
                vector = self.opt_reliability["time-exceed"]
            else:
                vector = self.opt_reliability["time-normal"]
        else:
            if self.trace.getLast()[1]["time"]  > self.system.tdir:
                vector = self.opt_time["time-exceed"]
            else:
                vector = self.opt_time["time-normal"]
        ops = {}
        for v in vector.keys():
            ops[v] = vector[v]
        
        # Delete impossible operations
        if not self.system.schedule.CanDeleteProcessor():
            ops.pop("DeleteProcessor", True)
            
        if not self.system.schedule.CanDeleteAnyVersions():
            ops.pop("DeleteVersion", True)
            
        if not self.system.schedule.CanAddAnyVersions():
            ops.pop("AddVersion", True)
                 
        return self._chooseRandomKey(ops)

    def DoAddProcessor(self):
        proc = list(self.system.schedule.processors)
        proc.sort(key=lambda x: x.reserves)
        total = sum([p.reserves for p in proc])
        dict = {}
        for p in proc:
            dict[p] = float(p.reserves)/float(total)
        m = self._chooseRandomKey(dict)
        self.lastOperation = AddProcessor(m)
        self.system.schedule.ApplyOperation(self.lastOperation)
        self.write(m)

    def DoDeleteProcessor(self):
        proc = list(self.system.schedule.processors)
        proc.sort(key=lambda x: x.reserves)
        total = sum([p.reserves for p in list(filter(lambda p: p.reserves > 1, proc))])
        dict = {}
        for p in proc:
            if p.reserves > 1:
                dict[p] = float(p.reserves)/float(total)
        if len(dict.keys()) > 0:
            m = self._chooseRandomKey(dict)
            self.lastOperation = DeleteProcessor(m)
            self.system.schedule.ApplyOperation(self.lastOperation)
            self.write(m)
        else:
            raise "Error"   
        
    def DoAddVersion(self):
        vers = list(filter(lambda v: len(v.versions) >= len(self.system.schedule.FindAllVertices(v=v)) + 2, \
            self.system.schedule.program.vertices))
        vers.sort(key=lambda v: len(v.versions))
        if len(vers) != 0:
            newproc = self.system.schedule.AddVersion(vers[0])
            self.lastOperation = AddVersion(vers[0], newproc, 1, newproc, 2)
            self.write(vers[0].number)
        else:
            raise "Error"
    
    def DoDeleteVersion(self):
        vers = list(filter(lambda v: len(self.system.schedule.FindAllVertices(v=v)) > 1, \
            self.system.schedule.program.vertices))
        vers.sort(key=lambda v: len(v.versions))
        if len(vers) != 0:
            (m1, m2, n1, n2) = self.system.schedule.DeleteVersion(vers[len(vers)-1]) 
            self.lastOperation = DeleteVersion(vers[len(vers)-1], m1, n1, m2, n2)
            self.write(vers[len(vers)-1].number)
        else:
            raise "Error"  

    def CutProcessor(self):
        s = self.system.schedule
        mini = len(s.program.vertices)
        proc = None
        for m in s.processors:
            f = len(s.vertices[m.number])
            if f < mini:
                mini = f
                proc = m
        ch = [v for v in s.vertices[proc.number]]
        self.multioperation = True
        self.lastOperation = MultiOperation()
        src_pos = 0
        for s1 in ch:
            flag = True
            for num in [n for n in s.vertices.keys() if n != proc.number]:
                target_proc = s.GetProcessor(num)
                for i in range(len(s.vertices[num]) + 1):
                    target_pos = i
                    if s.TryMoveVertex(s1, 0, target_proc, target_pos) == True:
                        s.MoveVertex(s1, 0, target_proc, target_pos)
                        self.lastOperation.Add(MoveVertex(s1, proc, 0, target_proc, target_pos))
                        flag = False
                        break
                if not flag:
                    break
            if flag:
                raise "Error"
                break
        return   
    
    def IdleStrategy(self):
        s = self.system.schedule
        if len(s.idletimes) == 0:
            keys = [m for m in s.vertices.keys()]
            proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
            s2 = proc[random.randint(0, len(proc)-1)]
        else:
            s2 = s.idletimes[min(random.randint(0, self.choice_places), len(s.idletimes)-1)][0]
        target_proc = s2.m
        target_pos = s.vertices[s2.m.number].index(s2)
        ch = []
        for d in s.delays:
            s1 = d[0]
            src_pos = s.vertices[s1.m.number].index(s1)
            if (s2 != s1) and s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
                ch.append(s1)
            if len(ch) == self.choice_vertices:
                break
        if len(ch) == 1:
            s1 = ch[0]
        elif len(ch) == 0:
            return self._findVertexToMove()
        else:
            s1 = ch[random.randint(0, len(ch)-1)]
        src_pos = s.vertices[s1.m.number].index(s1)

        return s1, src_pos, target_proc, target_pos

    def DelayStrategy(self):
        s = self.system.schedule
        if len(s.delays) == 0:
            keys = [m for m in s.vertices.keys()]
            proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
            s1 = proc[random.randint(0, len(proc)-1)]
        else:
            s1 = s.delays[min(random.randint(0,self.choice_vertices), len(s.delays)-1)][0]
        
        src_pos = s.vertices[s1.m.number].index(s1)
        ch = []
        timelimit = s.endtimes[s1] - s1.m.GetTime(s1.v.time)
        for s2 in s.endtimes.keys():
            proc = s2.m
            num = s.vertices[s2.m.number].index(s2) 
            if s.endtimes[s2] - s2.m.GetTime(s2.v.time) < timelimit:
                if (s2 != s1) and s.TryMoveVertex(s1, src_pos, proc, num) == True:
                    ch.append(s2)
            if len(ch) == self.choice_places:
                break
        if len(ch) == 0:
            return self._findVertexToMove()
        else:
            if len(ch) == 1:
                s2 = ch[0]
            else:
                s2 = ch[random.randint(0, len(ch)-1)]
            target_proc = s2.m
            target_pos = s.vertices[s2.m.number].index(s2)

        return s1, src_pos, target_proc, target_pos

    def _findVertexToMove(self):
        s = self.system.schedule
        keys = [m for m in s.vertices.keys()]
        for m1 in keys:
            for s1 in s.vertices[m1]:
                src_pos = s.vertices[m1].index(s1)
                for m2 in keys:
                    for i in range(len(s.vertices[m2])):
                        s2 = s.vertices[m2][i]
                        if (s2 != s1) and s.TryMoveVertex(s1, src_pos, s2.m, i) == True:
                            target_proc = s2.m
                            target_pos = s.vertices[s2.m.number].index(s2)
                            return s1, src_pos, target_proc, target_pos

    def MixedStrategy(self):
        s = self.system.schedule
        # TODO: what should we do if there are no delays? Maybe stop the algorithm?
        if len(s.delays) == 0:
            return self._findVertexToMove()
        else:
            s1 = s.delays[min(random.randint(0,self.choice_vertices), len(s.delays)-1)][0]
        src_pos = s.vertices[s1.m.number].index(s1)
        ch = []
        if len(s.idletimes) == 0:
            return self._findVertexToMove()
        for d in s.idletimes:
            # If the delay is zero, we mustn't move anything there
            if d[1] == 0:
                # TODO: change
                pass
            s2 = d[0]
            if (s2 != s1) and s.TryMoveVertex(s1, src_pos, s2.m, s.vertices[s2.m.number].index(s2)) == True:
                ch.append(s2)
            if len(ch) == self.choice_places:
                break              
        if len(ch) == 1:
            s2 = ch[0]
        elif len(ch) == 0:
            return self._findVertexToMove()
        else:
            s2 = ch[random.randint(0, len(ch)-1)]
        target_proc = s2.m
        target_pos = s.vertices[s2.m.number].index(s2)
        return s1, src_pos, target_proc, target_pos

    def DoMoveVertex(self):
        s = self.system.schedule
        r = random.random()
        if self.strategies[1] == 2:
            s1, src_pos, target_proc, target_pos = self.MixedStrategy()
        elif self.strategies[1] == 1:
            s1, src_pos, target_proc, target_pos = self.DelayStrategy()
        else:
            s1, src_pos, target_proc, target_pos = self.IdleStrategy()
                    
        self.write(s1.v.number, s1.m.number, src_pos, target_proc, target_pos)
        if s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
            self.lastOperation = MoveVertex(s1, s1.m, src_pos, target_proc, target_pos)
            s.ApplyOperation(self.lastOperation)
            self.lastOperation.pos2 = (s1.m, s.vertices[s1.m.number].index(s1))
        else:
            print ([p for p in ch])
            for p in ch:
                print (s.TryMoveVertex(s1, p.m, p.n))
            raise "Something went wrong"          
                         
    # Selects parameters for the operation and applies it whenever possible
    def _applyOperation(self, op):
        self.write(op)
        self.multioperation = False
        if op == "AddProcessor":
            self.DoAddProcessor()
        elif op == "DeleteProcessor":
            self.DoDeleteProcessor()              
        elif op == "AddVersion":
            self.DoAddVersion()
        elif op == "DeleteVersion":
            self.DoDeleteVersion()        
        elif op == "MoveVertex":
            if self.trace.getLast()[1]["time"]  < self.system.tdir and self.trace.getLast()[1]["processors"] > 1:
                self.CutProcessor()
            else:
                self.DoMoveVertex()
    
    def _selectNewSchedule(self):
        def accept():
            self.write("Accept")
            self.lastOperation.result = True
            self.trace.addStep(self.lastOperation, {"time":new_time, "reliability":new_rel, "processors":new_proc})
            best = self.trace.getBest()[1]
            if new_time <= self.system.tdir and new_rel >= self.system.rdir:
                if curProc < best["processors"]  or (curProc == best["processors"] and curTime < best["time"]):
                    self.trace.setBest(self.trace.length() - 1)
                    self.write("BEST SOLUTION:", self.trace.getLast()[1])
            
        def refuse():  
            self.write("Refuse")
            self.lastOperation.result = False
            self.system.schedule.ApplyOperation(self.lastOperation.Reverse())

        def checkThreshold():
            r = random.random()
            if self.threshold[1] == 0:
                #Bolzmann
                t = self.initialTemperature / math.log(1 + self.iteration)
            elif self.threshold[1] == 1:
                #Cauchy
                t = self.initialTemperature / float(1 + self.iteration)
            else:
                #Combined
                t = self.initialTemperature * math.log(1 + self.iteration) / (1 + self.iteration)
            threshold = math.exp(-1 / t)
            if r > threshold:
                accept()
            else:
                refuse()
        
        new_time = self.system.schedule.Interpret()
        new_rel = self.system.schedule.GetReliability()
        new_proc = self.system.schedule.GetProcessors()
        
        cur = self.trace.getLast()[1]
        curTime = cur["time"]
        curRel = cur["reliability"]
        curProc = cur["processors"]
        
        self.write("Old: ", curTime, curRel, curProc)    
        self.write("New: ", new_time, new_rel, new_proc)   
        if (curProc > new_proc) or (curTime > new_time) or (curRel < new_rel):
            accept()
        else:
            checkThreshold()
