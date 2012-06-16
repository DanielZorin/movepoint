'''
Created on 15.12.2010

@author: juan
'''

from PyQt4.QtCore import QObject
from Schedules.System import System
from Methods.Scheduling.SimulatedAnnealing import SimulatedAnnealing
from Methods.Scheduling.RandomSimulatedAnnealing import RandomSimulatedAnnealing
import pickle

class Project(QObject):
    
    system = None
    method = None
    name = None
    graph = {}
    
    def __init__(self, s="", name=""):
        QObject.__init__(self)
        self.system = System(s)
        # TODO: think how to implement other methods
        self.method = SimulatedAnnealing(self.system)
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
                "proc": self.system.processors}
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
        self.graph = dict["graph"]
        self.system.schedule.Consistency()

    def GetMethodSettings(self):
        ''' Returns a dictionary of method settings with appropriate naming'''
        return [
        [self.tr("Number of iterations"),self.method.numberOfIterations],
        [self.tr("Strategy"),self.method.strategies],
        [self.tr("Temperature function"),self.method.threshold],
        [self.tr("Vertices limit"), self.method.choice_vertices],
        [self.tr("Positions limit"),self.method.choice_places],
        [self.tr("Operation probabilities: optimize reliability"), 
            {self.tr("Deadline not violated"): self.method.opt_reliability["time-normal"],
             self.tr("Deadline violated"): self.method.opt_reliability["time-exceed"]}],
        [self.tr("Operation probabilities: optimize time"), 
            {self.tr("Deadline not violated"): self.method.opt_time["time-normal"],
             self.tr("Deadline violated"): self.method.opt_time["time-exceed"]}]]
        
    def UpdateMethodSettings(self, dict):
        '''Deserializes the class from a dictionary of parameters'''
        self.method.opt_reliability["time-normal"] = dict[5][1][self.tr("Deadline not violated")]
        self.method.opt_reliability["time-exceed"] = dict[5][1][self.tr("Deadline violated")]
        self.method.opt_time["time-normal"] = dict[6][1][self.tr("Deadline not violated")]
        self.method.opt_time["time-exceed"] = dict[6][1][self.tr("Deadline violated")]
        self.method.choice_vertices = dict[3][1]
        self.method.choice_places = dict[4][1]
        self.method.strategies = dict[1][1]
        self.method.threshold = dict[2][1]
        self.method.numberOfIterations = dict[0][1]
    
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
