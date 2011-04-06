'''
Created on 06.04.2011

@author: juan
'''

from SRGM.SRGM import SRGM
from math import exp, sqrt, log

class JelinskiMoranda(SRGM):
    '''
    Represents the Jelinski-Moranda model
    '''

    def __init__(self, name):
        SRGM.__init__(self, name)    
        
    def JMfunc(self, x):
        sum = 0
        for i in range(1, self.total+1 ):     
            sum += 1 / (x - i + 1)
        tmpsum = 0.0
        for i in range(1, self.total+1 ):  
            tmpsum += (i-1)*(self.data[i]-self.data[i-1])
        sum -= self.total / ( x - tmpsum/self.totaltime)
        return sum        
    
    def Compute(self):
        n = self.Solve(self.JMfunc, self.total+1.0, self.total*2.0)
        tmpsum = 0.0
        for i in range(1, self.total+1 ):  
            tmpsum += (i-1)*(self.data[i]-self.data[i-1])
        phi = self.total / (self.totaltime*n - tmpsum)
        mttf = 1 / (phi*(n - self.total))
        return n, phi, mttf