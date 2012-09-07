'''
Created on 15.12.2010

@author: juan
'''

from Schedules.System import System
from Methods.Scheduling.MethodWrapper import MethodWrapper
from Methods.Scheduling.SimulatedAnnealing import SimulatedAnnealing
from Methods.Scheduling.Genetics import Genetics
import pickle

class Project(object):
    
    system = None
    method = None
    name = None
    graph = {}
    annealing = None
    genetics = None
    
    def __init__(self, s="", name=""):
        self.system = System(s)
        self.method = MethodWrapper(self.system)
        self.annealing = SimulatedAnnealing(self.method)
        self.genetics = Genetics(self.method)
        self.method.algorithm = self.annealing
        self.method.Reset()
        self.name = name
        
    def Serialize(self, filename):
        fn = open(filename, "wb")
        dict = {"name": self.name, 
                "system": self.system,
                "method": self.method,
                "graph": self.graph,
                # This is a very weird bug. Somehow processors aren't saved as a part of system.
                # Without this system.processors is []
                "proc": self.system.processors,
                "trace":self.method.trace}
        pickle.dump(dict, fn)
        fn.close()
    
    def Deserialize(self, filename):
        fn = open(filename, "rb")
        dict = pickle.load(fn)
        fn.close()
        self.name = dict["name"]
        self.system = dict["system"]
        self.system.program._buildData()
        self.system.processors = dict["proc"]
        self.method = dict["method"]
        self.method.trace = dict["trace"]
        self.graph = dict["graph"]
        # TODO: get rid of this
        self.system.schedule.Consistency()
        # TODO: temporary workaround
        if isinstance(self.method.algorithm, SimulatedAnnealing):
            self.annealing = self.method.algorithm
        else:
            self.genetics = self.method.algorithm
        self.method.algorithm = self.annealing
        self.annealing.data = self.method
        self.genetics.data = self.method

    def UsesAnnealing(self):
        return True if self.annealing == self.method.algorithm else False
    
    def Step(self):
        self.method.Step()
        
    def GetSchedule(self):
        return self.method.system.schedule
    
    def ResetSchedule(self):
        self.method.Reset()
        
    def GetStats(self):
        # Either all three are None, or none of them is None
        if self.method.curTime != None:
            return [self.method.curTime, self.method.curRel, self.method.curProc]
        else:
            return [self.method.system.schedule.Interpret(),
                    self.method.system.schedule.GetReliability(),
                    self.method.system.schedule.GetProcessors()]
            
    def GetLastStep(self):
        return self.method.lastOperation
    
    def GetLimits(self):
        return self.system.tdir, self.system.rdir
    
    def SetTdir(self, t):
        self.system.tdir = t
        self.method.system = self.system

    def SetRdir(self, r):
        self.system.rdir = r
        self.method.system = self.system
    
    def GenerateRandomSystem(self, params):
        if not self.system:
            self.system = System()
        self.system.GenerateRandom(params)
        self.method.ChangeSystem(self.system)
        
    def ChangeSystem(self, s):
        self.system = System(s)
        self.method.ChangeSystem(self.system)
    
    def ChangeName(self, n):
        self.name = n
