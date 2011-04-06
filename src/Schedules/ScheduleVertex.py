'''
Created on 03.11.2010

@author: juan
'''
from Core.Processor import Processor
from Core.Version import Version
from Schedules.ProgramVertex import *

class ScheduleVertex(object):
    '''Represents an element of the schedule: a quadruple consisting of four objects given in the constructor.

        * v - Task
        * k - Version of the task
        * m - Processor
        * n - Number on the processor
    
    '''

    v = None
    '''ProgramVertex'''
    
    k = None
    '''Version'''
    
    m = None
    '''Processor'''
    
    n = None
    '''Number on the processor'''

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
        ''' Getter for v provided for convenience '''
        return self.v
    
    def Version(self):
        ''' Getter for k provided for convenience '''
        return self.k
    
    def Processor(self):
        ''' Getter for m provided for convenience '''
        return self.m
    
    def Order(self):
        ''' Getter for n provided for convenience '''
        return self.n
