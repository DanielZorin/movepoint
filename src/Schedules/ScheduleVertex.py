'''
Created on 03.11.2010

@author: juan
'''
from Core.Processor import Processor
from Core.Version import Version
from Schedules.ProgramVertex import *

class ScheduleVertex(object):
    '''Represents an element of the schedule: a quadruple consisting of four objects given in the constructor.

    :param v: Task
    :param k: Version of the task
    :param m: Processor
    :param n: Number on the processor
    
    '''

    v = None
    ''':class:`~Schedules.ProgramVertex.ProgramVertex` object'''
    
    k = None
    ''':class:`~Core.Version.Version` object'''
    
    m = None
    ''':class:`~Core.Processor.Processor` object'''

    def __init__(self, v, k, m):
        self.v = v
        
        if k.__class__.__name__ == "Version":
            self.k = k
        else:
            self.k = Version(v, k)
        
        if m.__class__.__name__ == "Processor":
            self.m = m
        else:
            self.m = Processor(m)
        
    def __str__(self):
        return "{" + str(self.v) + str(self.k) + str(self.m) + "}\n" 
    
    def Task(self):
        ''' Getter for v provided for convenience '''
        return self.v
    
    def Version(self):
        ''' Getter for k provided for convenience '''
        return self.k
    
    def Processor(self):
        ''' Getter for m provided for convenience '''
        return self.m

