'''
Created on 10.11.2010

@author: juan
'''

from Schedules.System import System
from Schedules.Threshold import Threshold
from Schedules.Operation import *
from Methods.Scheduling.Exceptions import SchedulerFileException, SchedulerXmlException
import xml.dom.minidom
import random
import logging

class SimulatedAnnealing(object):
    ''' Simulated Annealing method adapted for scheduling.
    
    .. warning:: Write details here'''
    
    system = None
    ''' System, program and schedule to optimize'''
    
    iteration = 0
    ''' Current iteration (see Simulated Annealing) '''
    
    temperature = 0
    ''' Current temperature (see Simulated Annealing) '''
    
    opt_reliability = { "time-normal":{}, "time-exceed":{} }
    opt_time = { "time-normal":{}, "time-exceed":{} }
    ''' Operation priorities (dictionary operation_name:priority) '''
    
    choice_vertices = 5
    ''' Maximum number of vertices among which the parameters for "MoveVertex" are chosen '''
    
    choice_places = 5
    ''' Maximum number of places among which the parameters for "MoveVertex" are chosen '''
    
    strategies = {}
    ''' Used strategies for MoveVertex and their probabilities '''
    
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

    def __init__(self, system):
        self.iteration = 0
        self.system = system
        self.numberOfIterations = len(self.system.program.vertices) * 10 + 1
        self.temperature = 0
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('SimulatedAnnealing')
    
    def write(self, *text):
        ''' Print debug information'''
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            self.logger.debug(" ".join(res))
    
    def ChangeSystem(self, s):
        ''' Replace the system'''
        self.numberOfIterations = len(self.system.program.vertices) * 10
        self.system = s
        self._prepare()
        
    def LoadConfig(self, filename):
        ''' Loads the config from XML
        
        .. warning:: Describe the format here'''
        def LoadPrioritiesList(node):
            tmp = {}
            for att in node.attributes.keys():
                tmp[att] = float(node.getAttribute(att))
            sum = 0.0
            for s in tmp.values():
                sum += s
            for s in tmp.keys():
                tmp[s] /= sum
            return tmp
        
        try:
            f = open(filename)
            dom = xml.dom.minidom.parse(f)
        
            for c in dom.childNodes:
                if c.tagName == "config":
                    # Parse priorities
                    pr = list(filter(lambda node: node.nodeName == "priorities", list(c.childNodes)))[0]
                    opt_rel = list(filter(lambda node: node.nodeName == "opt-reliability", list(pr.childNodes)))[0]
                    opt_time = list(filter(lambda node: node.nodeName == "opt-time", list(pr.childNodes)))[0]
                    tmp = list(filter(lambda node: node.nodeName == "time-normal", list(opt_rel.childNodes)))[0]
                    self.opt_reliability["time-normal"] = LoadPrioritiesList(tmp)
                    tmp = list(filter(lambda node: node.nodeName == "time-exceed", list(opt_rel.childNodes)))[0]
                    self.opt_reliability["time-exceed"] = LoadPrioritiesList(tmp)
                    tmp = list(filter(lambda node: node.nodeName == "time-normal", list(opt_time.childNodes)))[0]
                    self.opt_time["time-normal"] = LoadPrioritiesList(tmp)
                    tmp = list(filter(lambda node: node.nodeName == "time-exceed", list(opt_time.childNodes)))[0]
                    self.opt_time["time-exceed"] = LoadPrioritiesList(tmp)
                    
                    # Parse limits
                    lim = list(filter(lambda node: node.nodeName == "limits", list(c.childNodes)))[0]
                    for n in lim.childNodes:
                        if n.nodeName == "choice-vertices":
                            self.choice_vertices = int(n.getAttribute("n"))
                        elif n.nodeName == "choice-places":
                            self.choice_places = int(n.getAttribute("n"))
                            
                    # Parse strategies
                    lim = list(filter(lambda node: node.nodeName == "strategies", list(c.childNodes)))[0]  
                    self.strategies = LoadPrioritiesList(lim)
                              
            f.close()
            
        except IOError:
            raise SchedulerFileException(filename)
        except(ValueError):
            f.close()
            raise SchedulerXmlException(filename)
      
    def Serialize(self):
        ''' Serializes this class.
        The class is not picklable because f1, f2, f3 are lambda functions.
        Therefore, all necessaary information is stored in the following dictionary.'''
        return {
        "trace": self.trace,
        "opt_reliability": self.opt_reliability,
        "opt_time": self.opt_time,
        "choice_vertices": self.choice_vertices,
        "choice_places":self.choice_places,
        "strategies":self.strategies,
        "numberOfIterations":self.numberOfIterations}
        
    def Deserialize(self, dict):
        '''Deserializes the class from a dictionary of parameters'''
        self.trace = dict["trace"]
        self.opt_reliability = dict["opt_reliability"]
        self.opt_time = dict["opt_time"]
        self.choice_vertices = dict["choice_vertices"]
        self.choice_places = dict["choice_places"]
        self.strategies = dict["strategies"]
        self.numberOfIterations = dict["numberOfIterations"]
    
    def Reset(self):
        ''' Resets the method to the zero iteration'''
        self.system.schedule.SetToDefault()
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
        while self.iteration < self.numberOfIterations:
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
        self.temperature += 1
        op = self._chooseOperation()
        self._applyOperation(op)
        self._selectNewSchedule()

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
        while True:
            if len(s.delays) == 0:
                keys = [m for m in s.vertices.keys()]
                proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
                s2 = proc[random.randint(0, len(proc)-1)]
            else:
                s2 = s.delays[min(random.randint(0, self.choice_places), len(s.delays)-1)][0]
            target_proc = s2.m
            target_pos = s.vertices[s2.m.number].index(s2)
            ch = []
            for d in s.waiting:
                s1 = d[0]
                src_pos = s.vertices[s1.m.number].index(s1)
                if (s2 != s1) and s.TryMoveVertex(s1, src_pos, target_proc, target_pos) == True:
                    ch.append(s1)
                if len(ch) == self.choice_vertices:
                    break
            if len(ch) == 1:
                s1 = ch[0]
            elif len(ch) == 0:
                continue
            else:
                s1 = ch[random.randint(0, len(ch)-1)]
            src_pos = s.vertices[s1.m.number].index(s1)
            break

        return s1, src_pos, target_proc, target_pos

    def DelayStrategy(self):
        s = self.system.schedule
        while True:
            if len(s.waiting) == 0:
                keys = [m for m in s.vertices.keys()]
                proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
                s1 = proc[random.randint(0, len(proc)-1)]
            else:
                s1 = s.waiting[min(random.randint(0,self.choice_vertices), len(s.waiting)-1)][0]
        
            src_pos = s.vertices[s1.m.number].index(s1)
            ch = []
            timelimit = s.endtimes[s1] - s1.m.GetTime(s1.v.time)
            for d in s.waiting:
                s2 = d[0]
                proc = s2.m
                num = s.vertices[s2.m.number].index(s2)         
                if s.endtimes[s2] - s2.m.GetTime(s2.v.time) < timelimit:
                    if (s2 != s1) and s.TryMoveVertex(s1, src_pos, proc, num) == True:
                        ch.append(s2)
                if len(ch) == self.choice_places:
                    break
            if len(ch) == 0:
                continue
            else:
                if len(ch) == 1:
                    s2 = ch[0]
                else:
                    s2 = ch[random.randint(0, len(ch)-1)]
                target_proc = s2.m
                target_pos = s.vertices[s2.m.number].index(s2)
                break

        return s1, src_pos, target_proc, target_pos

    def MixedStrategy(self):
        s = self.system.schedule
        while True:
            # TODO: what should we do if there are no delays? Maybe stop the algorithm?
            if len(s.waiting) == 0:
                keys = [m for m in s.vertices.keys()]
                proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
                s1 = proc[random.randint(0, len(proc)-1)]
            else:
                s1 = s.waiting[min(random.randint(0,self.choice_vertices), len(s.waiting)-1)][0]
                src_pos = s.vertices[s1.m.number].index(s1)
            ch = []
            for d in s.delays:
                # If the delay is zero, we mustn't move anything there
                if d[1] == 0:
                    break
                s2 = d[0]
                if (s2 != s1) and s.TryMoveVertex(s1, src_pos, s2.m, s.vertices[s2.m.number].index(s2)) == True:
                    ch.append(s2)
                if len(ch) == self.choice_places:
                    break              
            if len(ch) == 1:
                s2 = ch[0]
            elif len(ch) == 0:
                continue
            else:
                s2 = ch[random.randint(0, len(ch)-1)]
            target_proc = s2.m
            target_pos = s.vertices[s2.m.number].index(s2)
            break

        return s1, src_pos, target_proc, target_pos

    def DoMoveVertex(self):
        s = self.system.schedule
        r = random.random()
        # TODO: think about a better way to select a strategy
        if r < self.strategies["mixed"]:
            s1, src_pos, target_proc, target_pos = self.MixedStrategy()
        elif r < self.strategies["mixed"] + self.strategies["delay"]:
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
            # TODO: implement temperature
            refuse()
