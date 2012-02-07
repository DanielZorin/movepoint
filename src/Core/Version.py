'''
Created on 03.11.2010

@author: juan
'''

from Core.Software import Software

class Version(Software):
    ''' Represents a version of a certain program run in NVP structures.
    
    :param task: A :class:`~Schedules.ProgramVertex.ProgramVertex` object referencing to the instance of the program
    :param number: Ordinal number to identify this version among all versions of this task
    :param reliability: Reliability - a float in [0,1]'''
    
    number = None
    ''' Ordinal number to identify this version among all versions of this task '''
    
    reliability = None
    ''' Reliability - a float in [0,1]'''
    
    task = None
    ''' A :class:`~Schedules.ProgramVertex.ProgramVertex` object referencing to the instance of the program '''  

    def __init__(self, task, number, reliability = 1.0):
        Software.__init__(self, reliability)
        self.number = number
        self.task = task
        
    def __str__(self):
        return "Version: " + str(self.number) + "\n"