'''
Created on 10.11.2010

@author: juan
'''

from Schedules.Operation import *
import random, math
import logging

class SimulatedAnnealing(object):
    ''' Simulated Annealing method adapted for scheduling.
    
    .. warning:: Write details here'''
    
    opt_reliability = { "time-normal":{"AddVersion":0.5, "AddProcessor":0.33, "MoveVertex":0.16}, 
                        "time-exceed":{"AddVersion":0.33, "AddProcessor":0.5, "MoveVertex":0.16} }
    opt_time = { "time-normal":{"DeleteVersion":0.33, "DeleteProcessor":0.5, "MoveVertex":0.5}, 
                 "time-exceed":{"DeleteVersion":0.5, "DeleteProcessor":0.33, "MoveVertex":0.5} }
    ''' Operation priorities (dictionary operation_name:priority) '''
    
    choice_vertices = 5
    ''' Maximum number of vertices among which the parameters for "MoveVertex" are chosen '''
    
    choice_places = 5
    ''' Maximum number of places among which the parameters for "MoveVertex" are chosen '''
    
    strategies = [["Idle time reduction", "Delay reduction", "Mixed"], 2]
    ''' Used strategies for MoveVertex and their probabilities '''

    threshold = [["Bolzmann", "Cauchy", "Combined"], 0]
    '''Temperature function'''

    raiseTemperature = [["Yes", "No"], 0]
    ''' Raise temperature temporarily'''
    
    oldSchedule = None
    ''' Current approximation. A copy is saved here, and all changes are applied to the original '''
    
    writeLog = False

    def __init__(self, data):
        self.data = data
        logging.basicConfig(level=logging.DEBUG)
    
    def write(self, *text):
        ''' Print debug information'''
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            logger = logging.getLogger('SimulatedAnnealing')
            logger.debug(" ".join(res))
            
    def Step(self):
        ''' Makes a single iteration of the algorithm'''
        self.write("---------------------------")
        self.write("iteration ", self.data.iteration)
        self.data.lastOperation = VoidOperation()
        op = self._chooseOperation()
        self._applyOperation(op)
        self._selectNewSchedule()

    def Prepare(self):
        pass
   
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
        if self.data.trace.getLast()[1]["reliability"]  < self.data.system.rdir:
            if self.data.trace.getLast()[1]["time"] > self.data.system.tdir:
                vector = self.opt_reliability["time-exceed"]
            else:
                vector = self.opt_reliability["time-normal"]
        else:
            if self.data.trace.getLast()[1]["time"]  > self.data.system.tdir:
                vector = self.opt_time["time-exceed"]
            else:
                vector = self.opt_time["time-normal"]
        ops = {}
        for v in vector.keys():
            ops[v] = vector[v]
        
        # Delete impossible operations
        if not self.data.system.schedule.CanDeleteProcessor():
            ops.pop("DeleteProcessor", True)
            
        if not self.data.system.schedule.CanDeleteAnyVersions():
            ops.pop("DeleteVersion", True)
            
        if not self.data.system.schedule.CanAddAnyVersions():
            ops.pop("AddVersion", True)
                 
        return self._chooseRandomKey(ops)

    def DoAddProcessor(self):
        proc = list(self.data.system.schedule.processors)
        proc.sort(key=lambda x: x.reserves)
        total = sum([p.reserves for p in proc])
        dict = {}
        for p in proc:
            dict[p] = float(p.reserves)/float(total)
        m = self._chooseRandomKey(dict)
        self.data.lastOperation = AddProcessor(m)
        self.data.system.schedule.ApplyOperation(self.data.lastOperation)
        self.write(m)

    def DoDeleteProcessor(self):
        proc = list(self.data.system.schedule.processors)
        proc.sort(key=lambda x: x.reserves)
        total = sum([p.reserves for p in list(filter(lambda p: p.reserves > 1, proc))])
        dict = {}
        for p in proc:
            if p.reserves > 1:
                dict[p] = float(p.reserves)/float(total)
        if len(dict.keys()) > 0:
            m = self._chooseRandomKey(dict)
            self.data.lastOperation = DeleteProcessor(m)
            self.data.system.schedule.ApplyOperation(self.data.lastOperation)
            self.write(m)
        else:
            raise "Error"   
        
    def DoAddVersion(self):
        vers = list(filter(lambda v: len(v.versions) >= len(self.data.system.schedule.FindAllVertices(v=v)) + 2, \
            self.data.system.schedule.program.vertices))
        vers.sort(key=lambda v: len(v.versions))
        if len(vers) != 0:
            newproc = self.data.system.schedule.AddVersion(vers[0])
            self.data.lastOperation = AddVersion(vers[0], newproc, 1, newproc, 2)
            self.write(vers[0].number)
        else:
            raise "Error"
    
    def DoDeleteVersion(self):
        vers = list(filter(lambda v: len(self.data.system.schedule.FindAllVertices(v=v)) > 1, \
            self.data.system.schedule.program.vertices))
        vers.sort(key=lambda v: len(v.versions))
        if len(vers) != 0:
            (m1, m2, n1, n2) = self.data.system.schedule.DeleteVersion(vers[len(vers)-1]) 
            self.data.lastOperation = DeleteVersion(vers[len(vers)-1], m1, n1, m2, n2)
            self.write(vers[len(vers)-1].number)
        else:
            raise "Error"  

    def CutProcessor(self):
        s = self.data.system.schedule
        mini = len(s.program.vertices)
        proc = None
        for m in s.processors:
            f = len(s.vertices[m.number])
            if f < mini:
                mini = f
                proc = m
            if f == mini:
                maxdelay1 = 0
                maxdelay2 = 0
                for v in s.vertices[m.number]:
                    for v1 in self.data.interpreter.delays:
                        if v1[0] == v and v1[1] > maxdelay1:
                            maxdelay1 = v1[1]
                for v in s.vertices[proc.number]:
                    for v1 in self.data.interpreter.delays:
                        if v1[0] == v and v1[1] > maxdelay2:
                            maxdelay2 = v1[1]
                if maxdelay2 < maxdelay1:
                    proc = m
        ch = [v for v in s.vertices[proc.number]][::-1]
        self.data.lastOperation = MultiOperation()
        src_pos = len(ch) - 1
        for s1 in ch:
            flag = True
            edges = s.program.FindAllEdges(v1=s1.v)
            if len(edges) > 0:
                e = edges[0]
                for m in s.vertices.keys():
                    for v in s.vertices[m]:
                        if v.v == e.destination:
                            s2 = v
                            break
                target_proc = s2.m
                target_pos = s.vertices[s2.m.number].index(s2)
                if s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
                    s.MoveVertex(s1, src_pos, target_proc, target_pos)
                    self.data.lastOperation.Add(MoveVertex(s1, proc, src_pos, target_proc, target_pos))
                    src_pos -= 1
                    continue
            int = self.data.interpreter
            procs = [m for m in s.vertices.keys() if m != proc.number]
            for m in procs:
                for v in range(len(s.vertices[m]) + 1):
                    target_proc = s.GetProcessor(m)
                    target_pos = v
                    if target_proc != proc:
                        if s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
                            s.MoveVertex(s1, src_pos, target_proc, target_pos)
                            self.data.lastOperation.Add(MoveVertex(s1, proc, src_pos, target_proc, target_pos))
                            flag = False
                            src_pos -= 1
                            break
                if not flag:
                    break
            if flag:
                raise "Error"
                break
        return   

    def _getRandomVertex(self):
        s = self.data.system.schedule
        keys = [k for k in s.vertices.keys()]
        m = random.randint(0, len(keys) - 1)
        m = keys[m]
        proc = s.vertices[m]
        src_pos = random.randint(0, len(proc) - 1)
        s1 = proc[src_pos]
        return s1, src_pos

    def _getRandomPosition(self):
        s = self.data.system.schedule
        keys = [k for k in s.vertices.keys()]
        m = random.randint(0, len(keys) - 1)
        m = keys[m]
        proc = s.vertices[m]
        pos = random.randint(0, len(proc))
        return s.GetProcessor(m), pos

    def IdleStrategy(self):
        s = self.data.system.schedule
        int = self.data.interpreter
        i = 0
        while True:
            if len(int.idletimes) == 0:
                yield self._findVertexToMove()
                continue
            if self.data.lastOperation.result == True:
                i = 0
            pos = int.idletimes[i % len(int.idletimes)][0]
            target_proc = pos[0]
            target_pos = pos[1]
            found = False
            for i in range(len(s.program.vertices)):
                s1, src_pos = self._getRandomVertex()
                if s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
                    found = True
                    break
            if found:
                yield s1, src_pos, target_proc, target_pos
            else:
                yield self._findVertexToMove()
            i += 1

    def DelayStrategy(self):
        s = self.data.system.schedule
        int = self.data.interpreter
        i = 0
        while True:
            if len(int.delays) == 0:
                yield self._findVertexToMove()
                continue
            if self.data.lastOperation.result == True:
                i = 0
            s1 = int.delays[i % len(int.delays)][0]
            src_pos = s.vertices[s1.m.number].index(s1)
            if src_pos > 0:
                src_pos -= 1
                s1 = s.vertices[s1.m.number][src_pos]
            found = False
            for i in range(len(s.program.vertices)):
                target_proc, target_pos = self._getRandomPosition()
                if s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
                    found = True
                    break
            if found:
                yield s1, src_pos, target_proc, target_pos
            else:
                yield self._findVertexToMove()
            i += 1

    def _findVertexToMove(self):
        s = self.data.system.schedule
        keys = [m for m in s.vertices.keys()]
        for m1 in keys:
            for s1 in s.vertices[m1]:
                src_pos = s.vertices[m1].index(s1)
                for m2 in keys:
                    for i in range(len(s.vertices[m2])):
                        s2 = s.vertices[m2][i]
                        target_proc = s2.m
                        target_pos = s.vertices[s2.m.number].index(s2)
                        if (s2 != s1) and s.TryMoveVertex(s1, src_pos, s2.m, i) == True:
                            return s1, src_pos, target_proc, target_pos
        return s1, src_pos, target_proc, target_pos

    def MixedStrategy(self):
        r = random.random()
        if r < 0.5:
            return next(self.IdleStrategy())
        else:
            return next(self.DelayStrategy())

    def DoMoveVertex(self):
        s = self.data.system.schedule
        r = random.random()
        if self.strategies[1] == 2:
            s1, src_pos, target_proc, target_pos = self.MixedStrategy()
        elif self.strategies[1] == 1:
            s1, src_pos, target_proc, target_pos = next(self.DelayStrategy())
        else:
            s1, src_pos, target_proc, target_pos = next(self.IdleStrategy())
                    
        self.write(s1.v.number, s1.m.number, src_pos, target_proc, target_pos)
        if s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
            self.data.lastOperation = MoveVertex(s1, s1.m, src_pos, target_proc, target_pos)
            s.ApplyOperation(self.data.lastOperation)
            self.data.lastOperation.pos2 = (s1.m, s.vertices[s1.m.number].index(s1))
        else:
            print ([p for p in ch])
            for p in ch:
                print (s.TryMoveVertex(s1, p.m, p.n))
            raise "Something went wrong"          
                         
    # Selects parameters for the operation and applies it whenever possible
    def _applyOperation(self, op):
        self.write(op)
        if op == "AddProcessor":
            self.DoAddProcessor()
        elif op == "DeleteProcessor":
            self.DoDeleteProcessor()              
        elif op == "AddVersion":
            self.DoAddVersion()
        elif op == "DeleteVersion":
            self.DoDeleteVersion()        
        elif op == "MoveVertex":
            if self.data.trace.getLast()[1]["time"]  < self.data.system.tdir and self.data.trace.getLast()[1]["processors"] > 1:
                self.CutProcessor()
            else:
                self.DoMoveVertex()

    def _selectNewSchedule(self):
        def accept():
            self.write("Accept")
            self.data.lastOperation.result = True
            self.data.trace.addStep(self.data.lastOperation, {"time":new_time, "reliability":new_rel, "processors":new_proc})
            best = self.data.trace.getBest()[1]
            if new_time <= self.data.system.tdir and new_rel >= self.data.system.rdir:
                if new_proc < best["processors"]  or (new_proc == best["processors"] and new_time < best["time"]):
                    self.data.trace.setBest(self.data.trace.length() - 1)
                    self.write("BEST SOLUTION:", self.data.trace.getLast()[1])

            
        def refuse():  
            self.write("Refuse")
            self.data.lastOperation.result = False
            self.data.system.schedule.ApplyOperation(self.data.lastOperation.Reverse())

        def checkThreshold():
            r = random.random()
            number = self.data.iteration
            if self.raiseTemperature[1] == 0:
                number = max(number - self.data.trace.best, 1)
            if self.threshold[1] == 0:
                #Bolzmann
                t = self.data.initialTemperature / math.log(1 + number)
            elif self.threshold[1] == 1:
                #Cauchy
                t = self.data.initialTemperature * 20 / float(1 + number)
            elif self.threshold[1] == 2:
                #Combined
                t = self.data.initialTemperature * 20 * math.log(1 + number) / (1 + number)
            threshold = math.exp(-1 / t)
            if r < threshold:
                accept()
            else:
                refuse()
        
        new_time = self.data.interpreter.Interpret(self.data.system.schedule)
        new_rel = self.data.system.schedule.GetReliability()
        new_proc = self.data.system.schedule.GetProcessors()
        
        cur = self.data.trace.getLast()[1]
        curTime = cur["time"]
        curRel = cur["reliability"]
        curProc = cur["processors"]
        
        self.write("Old: ", curTime, curRel, curProc)    
        self.write("New: ", new_time, new_rel, new_proc)
        #print (curTime, curProc)
        if (curProc > new_proc) or (curTime > new_time) or (curRel < new_rel):
            accept()
        else:
            checkThreshold()


