'''
Created on 13.12.2010

@author: juan
'''

from Core.RedundancyTechnique import RedundancyTechnique
import itertools

class Reserve(RedundancyTechnique):
    
    pall = None
    pd = None
    prv = None
    
    def __init__(self, hard):
        RedundancyTechnique.__init__(self, "reserve", hard, [])
    
    def GetReliability(self):
        res = 1.0
        for p in self.hardware:
            res *= 1 - p.reliability
        return 1 - res