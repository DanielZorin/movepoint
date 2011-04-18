'''
Created on 03.11.2010

@author: juan
'''

from Core.Hardware import Hardware

class Processor(Hardware):

    number = None
    speed = None
    reserves = 1
    
    def __init__(self, n, r = 1.0, s = 1, res = 1):
        Hardware.__init__(self, r)
        self.number = n 
        self.speed = s  
        self.reserves = res
        
    def __eq__(self, other):
        if other.__class__.__name__ == self.__class__.__name__:
            return self.number == other.number
        else:
            return self.number == other
    
    #Makes Processor class hashable;
    #processors with the same number are identical.   
    def __hash__(self):
        return self.number
    
    def __str__(self):
        return "Processor: " + str(self.number) + "\n"
        
    def GetTime(self, n):
        return n
    
    def GetDeliveryTime(self, p, v):
        return v