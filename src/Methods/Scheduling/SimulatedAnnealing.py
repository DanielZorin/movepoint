'''
Created on 10.11.2010

@author: juan
'''

from Schedules.System import System
from Schedules.Threshold import Threshold
from Methods.Scheduling.Exceptions import SchedulerFileException, SchedulerXmlException
import xml.dom.minidom
import random
import copy

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
    
    curTime = None
    curRel = None
    curProc = None
    ''' Parameters of the current approximation '''
    
    oldSchedule = None
    ''' Current approximation. A copy is saved here, and all changes are applied to the original '''
    
    bestSchedule = None
    bestTime = None
    bestRel = None
    bestProc = None
    ''' Current best solution and its characteristics '''
    
    numberOfIterations = 0
    ''' Number of iteration is 10 * number of vertices '''
    
    f1 = None
    f2 = None
    f3 = None
    ''' Threshold functions (see the paper) '''
    
    lastOperation = {"operation": "",
                        "parameters": [],
                        "result": False}
    ''' Here we keep the info about the last operation. It's used in GUI '''
    
    completeCutting = False
    ''' Turns on experimental feature: cut processors completely '''
    
    writeLog = False
    ''' Debug feature: print debug information '''

    def __init__(self, system):
        self.iteration = 0
        self.system = system
        self.numberOfIterations = len(self.system.program.vertices) * 5
        self.temperature = 0
    
    def write(self, *text):
        ''' Print debug information'''
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            print(" ".join(res))
    
    def ChangeSystem(self, s):
        ''' Replace the system'''
        self.system = s
        
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
        except(xml.parsers.expat.ExpatError, ValueError):
            f.close()
            raise SchedulerXmlException(filename)
      
    def Serialize(self):
        ''' Serializes this class.
        The class is not picklable because f1, f2, f3 are lambda functions.
        Therefore, all necessaary information is stored in the following dictionary.'''
        return {
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
        self.curTime = self.system.schedule.Interpret()
        self.curRel = self.system.schedule.GetReliability()
        self.curProc = self.system.schedule.GetProcessors()
        self.bestProc = self.curProc
        self.bestTime = self.curTime
        self.bestRel = self.curRel
        self.bestSchedule = self.system.schedule.GetCopy()
    
    # TODO: clean up this function    
    def Start(self):
        ''' Runs the algorithm with the given number of iterations'''
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
        self.system.schedule.RestoreFromCopy(self.bestSchedule)
        self.curTime = self.bestTime
        self.curRel = self.bestRel
        self.curProc = self.bestProc
        return self.system.schedule
            
    def Step(self):
        ''' Makes a single iteration of the algorithm'''
        self.write("---------------------------")
        self.write("iteration ", self.iteration)
        self.lastOperation = {}
        self.temperature += 1
        op = self._chooseOperation()
        self._applyOperation(op)
        self._selectNewSchedule()
     
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
            move_delay = False
            if self.curTime < self.system.tdir:
                # Cut from a certain processor
                if random.random() < self.cut_processor and self.curProc > 1:
                    mini = len(s.vertices)
                    proc = None
                    for m in s.processors:
                        f = len(s.FindAllVertices(m=m))
                        if f < mini:
                            mini = f
                            proc = m
                    ch = s.FindAllVertices(m=proc)
                    if self.completeCutting == False:
                        s1 = ch[random.randint(0, len(ch)-1)]
                        while True:
                            num = random.randint(0, len(s.processors)-1)
                            if s.processors[num] != proc:
                                target_proc = s.processors[num]
                                target_pos = len(s.FindAllVertices(m=s.processors[num]))
                                break
                    else:
                        # TODO: this is an experimental implementation of complete cutting
                        for s1 in ch:  
                            while True:
                                num = random.randint(0, len(s.processors)-1)
                                if s.processors[num] != proc:
                                    target_proc = s.processors[num]
                                    target_pos = random.randint(1, len(s.FindAllVertices(m=s.processors[num]))+1)                                       
                                    #self.write("CUT PROCESSOR", s1.v.number, s1.m.number, s1.n, target_proc, target_pos)
                                    if target_proc == None:
                                        self.lastOperation["parameters"] = [s1.v.number, s1.k.number, -1, target_pos]
                                    else:
                                        self.lastOperation["parameters"] = [s1.v.number, s1.k.number, target_proc.number, target_pos]
                                    if s.TryMoveVertex(s1, target_proc, target_pos):
                                        s.MoveVertex(s1, target_proc, target_pos)
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
                    else:
                        s1 = s.vertices[random.randint(0, len(s.vertices)-1)]
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
                        return
                        s1 = s.vertices[random.randint(0, len(s.vertices)-1)]
                    else:
                        s1 = s.waiting[min(random.randint(0,self.choice_vertices), len(s.waiting)-1)][0]
                    ch = []
                    for d in s.delays:
                        # If the delay is zero, we mustn't move anything there
                        if d[1] == 0:
                            break
                        s2 = d[0]
                        proc = s2.m
                        num = s2.n
                        if (s2 != s1) and s.TryMoveVertex(s1, proc, num):
                            ch.append(s2)
                        if len(ch) == self.choice_places:
                            break
                    if len(ch) == 1:
                        s2 = ch[0]
                    elif len(ch) == 0:
                        # TODO: get rid of random selection
                        s2 = s.vertices[random.randint(0, len(s.vertices)-1)]
                    else:
                        s2 = ch[random.randint(0, len(ch)-1)]
                    target_proc = s2.m
                    target_pos = s2.n
                # Delay strategy
                elif r < self.strategies["mixed"] + self.strategies["delay"]:
                    if len(s.waiting) == 0:
                        s1 = s.vertices[random.randint(0, len(s.vertices)-1)]
                    else:
                        s1 = s.waiting[min(random.randint(0,self.choice_vertices), len(s.waiting)-1)][0]
                    ch = []
                    timelimit = s.endtimes[s1] - s1.m.GetTime(s1.v.time)
                    for d in s.vertices:
                        s2 = d
                        proc = s2.m
                        num = s2.n
                        if s.endtimes[s2] - s2.m.GetTime(s2.v.time) < timelimit:
                            if (s2 != s1) and s.TryMoveVertex(s1, proc, num):
                                ch.append(s2)
                        if len(ch) == self.choice_places:
                            break
                    if len(ch) == 1:
                        s2 = ch[0]
                    elif len(ch) == 0:
                        # TODO: get rid of random selection
                        s2 = s.vertices[random.randint(0, len(s.vertices)-1)]
                    else:
                        s2 = ch[random.randint(0, len(ch)-1)]
                    target_proc = s2.m
                    target_pos = s2.n
                # Idle strategy
                else:
                    if len(s.delays) == 0:
                        s2 = s.vertices[random.randint(0, len(s.vertices)-1)]
                    else:
                        s2 = s.delays[min(random.randint(0,self.choice_places), len(s.delays)-1)][0]
                    target_proc = s2.m
                    target_pos = s2.n
                    ch = []
                    for d in s.waiting:
                        s1 = d[0]
                        if (s2 != s1) and s.TryMoveVertex(s1, target_proc, target_pos):
                            ch.append(s1)
                        if len(ch) == self.choice_vertices:
                            break
                    if len(ch) == 1:
                        s1 = ch[0]
                    elif len(ch) == 0:
                        # TODO: get rid of random selection
                        s1 = s.vertices[random.randint(0, len(s.vertices)-1)]
                    else:
                        s1 = ch[random.randint(0, len(ch)-1)]
                    
            self.write(s1.v.number, s1.m.number, s1.n, target_proc, target_pos)
            if target_proc == None:
                self.lastOperation["parameters"] = [s1.v.number, s1.k.number, -1, target_pos]
            else:
                self.lastOperation["parameters"] = [s1.v.number, s1.k.number, target_proc.number, target_pos]
            if s.TryMoveVertex(s1, target_proc, target_pos):
                s.MoveVertex(s1, target_proc, target_pos)
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
                    self.bestSchedule = self.system.schedule.GetCopy()
                    self.write("BEST SOLUTION:", self.bestTime, self.bestProc, self.system.tdir)
            
        def refuse():  
            self.write("Refuse")
            self.lastOperation["result"] = False
            #self.system.schedule = self.oldSchedule 
            self.system.schedule.RollBack()
            
        def choose(f1, f2, f3):
            self.write(f1(self.temperature), f2(self.temperature), f3(self.temperature))
            if (self.curTime > new_time) and (self.curRel < new_rel):
                if random.random() < f1(self.temperature):
                    accept()
                else:
                    refuse()
            elif (self.curTime > new_time) and not (self.curRel < new_rel):
                if random.random() < f2(self.temperature):
                    accept()
                else:
                    refuse()
            elif not (self.curTime > new_time) and (self.curRel < new_rel):
                if random.random() < f2(self.temperature):
                    accept()
                else:
                    refuse()
            elif not (self.curTime > new_time) and not (self.curRel < new_rel):
                if random.random() < f3(self.temperature):
                    accept()
                else:
                    refuse()              

        new_time = self.system.schedule.Interpret()
        new_rel = self.system.schedule.GetReliability()
        new_proc = self.system.schedule.GetProcessors()
        
        # Thresholds are implemented as described in the paper
        # The code might look a bit redundant, but it's easier to relate implementation with the
        # theoretical description.
        '''if self.curProc > new_proc:
            choose(lambda x: 1, self.f1.f, self.f2.f)
        elif self.curProc == new_proc:
            choose(self.f1.f, self.f2.f, self.f3.f)
        elif self.curProc < new_proc:
            choose(self.f2.f, self.f3.f, lambda x: 0)'''
        
        self.write("Old: ", self.curTime, self.curRel, self.curProc)    
        self.write("New: ", new_time, new_rel, new_proc)   
        if (self.curProc > new_proc) or (self.curTime > new_time) or (self.curRel < new_rel):
            accept()
        else:
            refuse()
           
ss = System("program.xml")
ss.GenerateRandom({"n":40, "t1":2, "t2":5, "v1":1, "v2":2, "tdir":2, "rdir":2})
s = SimulatedAnnealing(ss)
s.LoadConfig("config.xml")
s.Start()