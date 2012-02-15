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
    
    cut_processor = 0.5
    ''' Probability of the special operation "Cut processor" '''
    
    new_processor = 0.5
    ''' Probability of the special operation "Cut processor" '''
    
    strategies = {}
    ''' Used strategies for MoveVertex and their probabilities '''
    
    oldSchedule = None
    ''' Current approximation. A copy is saved here, and all changes are applied to the original '''
    
    numberOfIterations = 0
    ''' Number of iteration is 10 * number of vertices '''
    
    # TODO: default values
    f1 = None
    f2 = None
    f3 = None
    ''' Threshold functions (see the paper) '''
    
    lastOperation = VoidOperation()
    ''' Here we keep the info about the last operation. It's used in GUI '''
    
    trace = Trace()

    completeCutting = True
    ''' Turns on experimental feature: cut processors completely '''
    
    writeLog = False
    ''' Debug feature: print debug information '''
    
    multioperation = False
    noOperation = False

    def __init__(self, system):
        self.iteration = 0
        self.system = system
        self.numberOfIterations = len(self.system.program.vertices) * 10
        self.temperature = 0
        self.system.schedule.SetToDefault()
        self._prepare()
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
                        elif n.nodeName == "cut-processor":
                            self.choice_vertice = float(n.getAttribute("p"))
                        elif n.nodeName == "new-processor":
                            self.choice_vertice = float(n.getAttribute("p"))
                            
                    # Parse strategies
                    lim = list(filter(lambda node: node.nodeName == "strategies", list(c.childNodes)))[0]  
                    self.strategies = LoadPrioritiesList(lim)
                          
                    # Parse thresholds
                    threshold = list(filter(lambda node: node.nodeName == "thresholds", list(c.childNodes)))[0]
                    for n in threshold.childNodes:
                        if n.nodeName == "threshold":
                            id = n.getAttribute("id")
                            type = n.getAttribute("type")
                            # TODO: if some threshold function needs more parameters,
                            # we'll have to implement a more complicated parser here
                            param = float(n.getAttribute("param"))
                            if type == "linear":
                                th = Threshold(type=type, a=-param/self.numberOfIterations, b=1)
                            else:
                                # Implement other types here
                                pass
                            if id == "1":
                                self.f1 = th
                            elif id == "2":
                                self.f2 = th
                            elif id == "3":
                                self.f3 = th     
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
        "cut_processor":self.cut_processor,
        "new_processor":self.new_processor,
        "strategies":self.strategies,
        "numberOfIterations":self.numberOfIterations,
        "f1":(self.f1.type, self.f1.params),
        "f2":(self.f2.type, self.f2.params),
        "f3":(self.f3.type, self.f3.params)}
        
    def Deserialize(self, dict):
        '''Deserializes the class from a dictionary of parameters'''
        self.trace = dict["trace"]
        self.opt_reliability = dict["opt_reliability"]
        self.opt_time = dict["opt_time"]
        self.choice_vertices = dict["choice_vertices"]
        self.choice_places = dict["choice_places"]
        self.cut_processor = dict["cut_processor"]
        self.new_processor = dict["new_processor"]
        self.strategies = dict["strategies"]
        self.numberOfIterations = dict["numberOfIterations"]
        self.f1 = Threshold(type=dict["f1"][0], cachedparams=dict["f1"][1])
        self.f2 = Threshold(type=dict["f2"][0], cachedparams=dict["f2"][1])
        self.f3 = Threshold(type=dict["f3"][0], cachedparams=dict["f3"][1])
    
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
        self.trace.addStep(self.lastOperation, {"time":new_time, "reliability":new_rel, "processors":new_proc})
        best = self.trace.getBest()[1]
        if new_time <= self.system.tdir and new_rel >= self.system.rdir:
            if curProc < best["processors"]  or (curProc == best["processors"] and curTime < best["time"]):
                self.trace.setBest(self.trace.length())
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
    
    # Selects parameters for the operation and applies it whenever possible
    def _applyOperation(self, op):
        self.write(op)
        self.multioperation = False
        self.noOperation = False
        if op == "AddProcessor":
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
                self.lastOperation = DeleteProcessor(m)
                self.system.schedule.ApplyOperation(self.lastOperation)
                self.write(m)
            else:
                raise "Error"
                
        elif op == "AddVersion":
            vers = list(filter(lambda v: len(v.versions) >= len(self.system.schedule.FindAllVertices(v=v)) + 2, \
                self.system.schedule.program.vertices))
            vers.sort(key=lambda v: len(v.versions))
            if len(vers) != 0:
                newproc = self.system.schedule.AddVersion(vers[0])
                self.lastOperation = AddVersion(vers[0], newproc, 1, newproc, 2)
                self.write(vers[0].number)
            else:
                raise "Error"
        elif op == "DeleteVersion":
            vers = list(filter(lambda v: len(self.system.schedule.FindAllVertices(v=v)) > 1, \
                self.system.schedule.program.vertices))
            vers.sort(key=lambda v: len(v.versions))
            if len(vers) != 0:
                (m1, m2, n1, n2) = self.system.schedule.DeleteVersion(vers[len(vers)-1]) 
                self.lastOperation = DeleteVersion(vers[len(vers)-1], m1, n1, m2, n2)
                self.write(vers[len(vers)-1].number)
            else:
                raise "Error"
                
        elif op == "MoveVertex":
            s = self.system.schedule
            s1 = None
            src_proc = None
            src_pos = None
            target_proc = None
            target_pos = None
            move_delay = False
            noOp = False
            if self.trace.getLast()[1]["time"]  < self.system.tdir:
                # Cut from a certain processor
                if random.random() < self.cut_processor and self.trace.getLast()[1]["processors"] > 1:
                    mini = len(s.program.vertices)
                    proc = None
                    for m in s.processors:
                        f = len(s.vertices[m.number])
                        if f < mini:
                            mini = f
                            proc = m
                    ch = [v for v in s.vertices[proc.number]]
                    if self.completeCutting == False:
                        s1 = ch[random.randint(0, len(ch)-1)]
                        while True:
                            num = random.randint(0, len(s.processors)-1)
                            if s.processors[num] != proc:
                                target_proc = s.processors[num]
                                target_pos = len(s.vertices[s.processors[num]])
                                break
                    else:
                        # TODO: this is an experimental implementation of complete cutting
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
                # Move the task with the highest delay
                else:
                    move_delay = True
            else:    
                # New processor
                if random.random() < self.new_processor:
                    if len(s.delays) > 0:
                        s1 = s.waiting[min(random.randint(0,self.choice_vertices), len(s.waiting)-1)][0]
                        src_proc = s1.m.number
                        src_pos = s.vertices[src_proc].index(s1)
                    else:
                        keys = [m for m in s.vertices.keys()]
                        proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
                        src_pos = random.randint(0, len(proc)-1)
                        s1 = proc[src_pos]
                    target_proc = None
                    target_pos = 1
                else:
                    move_delay = True
            if move_delay:
                r = random.random()
                # TODO: think about a better way to select a strategy
                #Mixed strategy
                if r < self.strategies["mixed"]:
                    # TODO: what should we do if there are no delays? Maybe stop the algorithm?
                    if len(s.waiting) == 0:
                        noOp = True
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
                        noOp = True
                        s2 = None
                    else:
                        s2 = ch[random.randint(0, len(ch)-1)]
                    if s2:
                        target_proc = s2.m
                        target_pos = s.vertices[s2.m.number].index(s2)
                # Delay strategy
                elif r < self.strategies["mixed"] + self.strategies["delay"]:
                    if len(s.waiting) == 0:
                        keys = [m for m in s.vertices.keys()]
                        proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
                        s1 = proc[random.randint(0, len(proc)-1)]
                    else:
                        s1 = s.waiting[min(random.randint(0,self.choice_vertices), len(s.waiting)-1)][0]
                    ch = []
                    timelimit = s.endtimes[s1] - s1.m.GetTime(s1.v.time)
                    for d in s.waiting:
                        s2 = d[0]
                        proc = s2.m
                        num = s.vertices[s2.m.number].index(s2)
                        src_pos = s.vertices[s1.m.number].index(s1)
                        if s.endtimes[s2] - s2.m.GetTime(s2.v.time) < timelimit:
                            if (s2 != s1) and s.TryMoveVertex(s1, src_pos, proc, num) == True:
                                ch.append(s2)
                        if len(ch) == self.choice_places:
                            break
                    if len(ch) == 0:
                        s2 = None
                        noOp = True
                    else:
                        if len(ch) == 1:
                            s2 = ch[0]
                        else:
                            s2 = ch[random.randint(0, len(ch)-1)]
                        target_proc = s2.m
                        target_pos = s.vertices[s2.m.number].index(s2)
                # Idle strategy
                else:
                    if len(s.delays) == 0:
                        keys = [m for m in s.vertices.keys()]
                        proc = s.vertices[keys[random.randint(0, len(s.vertices.keys())-1)]]
                        s2 = proc[random.randint(0, len(proc)-1)]
                    else:
                        s2 = s.delays[min(random.randint(0,self.choice_places), len(s.delays)-1)][0]
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
                        s1 = None
                        noOp = True
                    else:
                        s1 = ch[random.randint(0, len(ch)-1)]
                    if s1:
                        src_pos = s.vertices[s1.m.number].index(s1)
            
            if noOp:
                self.noOperation = True
                return
                    
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
    
    def _selectNewSchedule(self):
        def accept():
            self.write("Accept")
            self.lastOperation.result = True
            self.trace.addStep(self.lastOperation, {"time":new_time, "reliability":new_rel, "processors":new_proc})
            best = self.trace.getBest()[1]
            if new_time <= self.system.tdir and new_rel >= self.system.rdir:
                if curProc < best["processors"]  or (curProc == best["processors"] and curTime < best["time"]):
                    self.trace.setBest(self.trace.length())
                    self.write("BEST SOLUTION:", self.trace.getLast()[1])
            
        def refuse():  
            self.write("Refuse")
            self.lastOperation.result = False
            self.system.schedule.ApplyOperation(self.lastOperation.Reverse())
            
        def choose(f1, f2, f3):
            self.write(f1(self.temperature), f2(self.temperature), f3(self.temperature))
            if (curTime > new_time) and (curRel < new_rel):
                if random.random() < f1(self.temperature):
                    accept()
                else:
                    refuse()
            elif (curTime > new_time) and not (curRel < new_rel):
                if random.random() < f2(self.temperature):
                    accept()
                else:
                    refuse()
            elif not (curTime > new_time) and (curRel < new_rel):
                if random.random() < f2(self.temperature):
                    accept()
                else:
                    refuse()
            elif not (curTime > new_time) and not (curRel < new_rel):
                if random.random() < f3(self.temperature):
                    accept()
                else:
                    refuse()              

        if self.noOperation:
            return
        
        new_time = self.system.schedule.Interpret()
        new_rel = self.system.schedule.GetReliability()
        new_proc = self.system.schedule.GetProcessors()
        
        cur = self.trace.getLast()[1]
        curTime = cur["time"]
        curRel = cur["reliability"]
        curProc = cur["processors"]

        # Thresholds are implemented as described in the paper
        # The code might look a bit redundant, but it's easier to relate implementation with the
        # theoretical description.
        '''if curProc > new_proc:
            choose(lambda x: 1, self.f1.f, self.f2.f)
        elif curProc == new_proc:
            choose(self.f1.f, self.f2.f, self.f3.f)
        elif curProc < new_proc:
            choose(self.f2.f, self.f3.f, lambda x: 0)'''
        
        self.write("Old: ", curTime, curRel, curProc)    
        self.write("New: ", new_time, new_rel, new_proc)   
        if (curProc > new_proc) or (curTime > new_time) or (curRel < new_rel):
            accept()
        else:
            refuse()
