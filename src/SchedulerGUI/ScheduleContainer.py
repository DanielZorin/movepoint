'''
Created on 27.12.2010

@author: juan
'''

import copy

class ScheduleContainer(object):

    schedules = []
    stats = []
    operations = []
    current = -1

    def __init__(self):
        self.schedules = []
        self.stats = []
        self.operations = []
        self.current = -1
  
    def Add(self, s, stats, op):
        self.schedules.append(copy.deepcopy(s))
        self.stats.append(stats)
        self.operations.append(op)
        self.current = len(self.schedules) - 1
        
    def GetCurrent(self):
        return self.schedules[self.current]
    
    def GetCurrentStats(self):
        return self.stats[self.current]
    
    def GetCurrentOperation(self):
        # The button is disabled in the main window, so out of range error isn't possible
        return self.operations[self.current + 1]
    
    def GetTotal(self):
        return len(self.schedules)
    
    def IsLast(self):
        return self.current == len(self.schedules) - 1
    
    def Clear(self):
        self.schedules = []
        self.stats = []
        self.operations = []
        self.current = -1