'''
Created on 06.04.2011

@author: juan
'''

from SRGM.SRGM import SRGM
from math import exp, sqrt, log

class Logarithmic(SRGM):
    '''
    Represents the logarithmic model
    '''

    def __init__(self, name):
        SRGM.__init__(self, name) 
    

    def LogarithmicFunc(self, x):
        sum = 0
        for i in range(1, self.total+1 ):     
            sum += 1/(1 + x*self.data[i])
        sum /= x
        sum -= self.totaltime*self.total / ( (1 + x*self.totaltime) * (log(1 + x*self.totaltime)) )
        return sum
    
    def Compute(self):
        b1 = self.Solve(self.LogarithmicFunc, 0.001, 2)
        b0 = self.total / log(1+b1*self.totaltime)
        tmp = b0*b1/(b1*self.totaltime + 1)
        mttf = 1/tmp
        return b0, b1, mttf