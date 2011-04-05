'''
Created on 03.11.2010

@author: juan
'''
from Core.Processor import Processor
from Core.Version import Version
from Schedules.ProgramVertex import *

class ScheduleVertex(object):

    v = None
    k = None
    m = None
    n = None

    def __init__(self, v, k, m, n):
        self.v = v
        
        if k.__class__.__name__ == "Version":
            self.k = k
        else:
            self.k = Version(v, k)
        
        if m.__class__.__name__ == "Processor":
            self.m = m
        else:
            self.m = Processor(m)
        
        self.n = n
        
    def __str__(self):
        return "{" + str(self.v) + str(self.k) + str(self.m) + str(self.n) + "}\n" 
    
    def Task(self):
        return self.v
    
    def Version(self):
        return self.k
    
    def Processor(self):
        return self.m
    
    def Order(self):
        return self.n
