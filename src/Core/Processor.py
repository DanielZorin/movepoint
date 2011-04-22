'''
Created on 03.11.2010

@author: juan
'''

from Core.Hardware import Hardware

class Processor(Hardware):
    ''' Represents a single CPU.
    
    :param n: Ordinal number to identify this processor
    :param r: Reliability - a float in [0,1]
    :param s: Speed/efficiency of this processor. It's assumed that it doesn't depend on the program executed.
    :param res: Number of reserves. This will be deprecated when a more complex scheme is implemented'''
    
    number = None
    ''' Ordinal number to identify this processor '''
    
    speed = None
    ''' Speed/efficiency of this processor. '''
    
    reserves = 1
    ''' Number of reserves.'''
    
    def __init__(self, n, r = 1.0, s = 1.0, res = 1):
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
        ''' Returns the time of execution of a program with length n
        
        .. warning:: not implemented yet, returns n always.'''
        return n
    
    def GetDeliveryTime(self, p, v):
        ''' Returns the time of delivery of v units of data to processor p
        
        .. warning:: not implemented yet, returns v always.'''
        return v