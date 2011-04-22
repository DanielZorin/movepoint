'''
Created on 13.12.2010

@author: juan
'''

from Core.RedundancyTechnique import RedundancyTechnique
import itertools

class Reserve(RedundancyTechnique):
    ''' Represents hardware reserve technique. Several identical CPUs work simultaneously,
    if at least one doesn't fail, then the system doesn't fail.'''
    
    def __init__(self, hard):
        RedundancyTechnique.__init__(self, "reserve", hard, [])
    
    def GetReliability(self):
        ''' Calculates the reliability'''
        res = 1.0
        for p in self.hardware:
            res *= 1 - p.reliability
        return 1 - res