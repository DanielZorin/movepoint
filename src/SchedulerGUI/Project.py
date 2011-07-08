'''
Created on 15.12.2010

@author: juan
'''

from Schedules.System import System
from Methods.Scheduling.SimulatedAnnealing import SimulatedAnnealing
from Methods.Scheduling.RandomSimulatedAnnealing import RandomSimulatedAnnealing
import pickle

class Project(object):
    
    system = None
    method = None
    name = None
    
    def __init__(self, s=None, m=None, name=""):
        if s != None and m != None:
            # TODO: m can be None
            self.system = System(s)
            # TODO: think how to implement other methods
            self.method = SimulatedAnnealing(self.system)
            self.method.LoadConfig(m)
        self.name = name
        
    def Serialize(self, filename):
        # SimulatedAnnealing can't be serialized because it has undefined Threshold field
        # However, it's possible to make a config dump in SimulatedAnnelaing and serialize it.
        fn = open(filename, "wb")
        dict = {"name": self.name, 
                "system": self.system,
                "method": self.method.Serialize(),
                # This is a very weird bug. Somehow processors aren't saved as a part of system.
                # Without this system.processors is []
                "proc": self.system.processors}
        pickle.dump(dict, fn)
        fn.close()
    
    def Deserialize(self, filename):
        fn = open(filename, "rb")
        dict = pickle.load(fn)
        fn.close()
        self.name = dict["name"]
        self.system = dict["system"]
        self.system.processors = dict["proc"]
        self.method = SimulatedAnnealing(self.system)
        self.method.Deserialize(dict["method"])
    
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
    
    def SetLimits(self, t, r):
        self.system.tdir = t
        self.system.rdir = r
        self.method.system = self.system
    
    def GenerateRandomSystem(self, params):
        self.system.GenerateRandom(params)
        self.method.ChangeSystem(self.system)
        
    def ChangeSystem(self, s):
        self.system = System(s)
        self.method.ChangeSystem(self.system)
    
    def ChangeMethod(self, s):
        self.method.LoadConfig(s)
    
    def ChangeName(self, n):
        self.name = n
