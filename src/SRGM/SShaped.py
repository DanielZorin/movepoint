'''
Created on 06.04.2011

@author: juan
'''
from .SRGM import SRGM
from Core.Common import findroot
from math import exp, sqrt, log

class SShaped(SRGM):
    '''
    Represents the S-Shaped model
    '''

    def __init__(self):
        SRGM.__init__(self) 
        
    def SShapedFunc(self, x):
        i = 1
        sum = self.total*(self.totaltime**2)*exp(-x*self.totaltime)/(1-(1+x*self.totaltime)*exp(-x*self.totaltime))
        while i < self.total+1: 
            if i < self.total:
                if self.data[i] != self.data[i+1]:     
                    tmp = (self.data[i]**2)*exp(-x*self.data[i]) - (self.data[i-1]**2)*exp(-x*self.data[i-1])
                    tmp /= ((1+x*self.data[i-1])*exp(-x*self.data[i-1]) - (1+x*self.data[i])*exp(-x*self.data[i]))
                    sum -= tmp                    
                    i += 1
                else:
                    k = 1
                    tmp = self.data[i-1]
                    while self.data[i] == self.data[i+1]:
                        k += 1
                        i += 1
                        if i >= self.total - 1:
                            break
                    
                    tmp2 = k * (self.data[i]**2)*exp(-x*self.data[i]) - (tmp**2)*exp(-x*tmp)
                    tmp2 /= ((1+x*tmp)*exp(-x*tmp) - (1+x*self.data[i])*exp(-x*self.data[i]))
                    sum -= tmp2
            
                    i += 1
            else:
                if self.data[i] == self.data[i-1]:
                    break
                tmp = (self.data[i]**2)*exp(-x*self.data[i]) - (self.data[i-1]**2)*exp(-x*self.data[i-1])
                tmp /= ((1+x*self.data[i-1])*exp(-x*self.data[i-1]) - (1+x*self.data[i])*exp(-x*self.data[i]))
                sum -= tmp 
                i += 1
        return sum
    
    def Compute(self):
        b = findroot(self.SShapedFunc, 0.000001, 0.01)     
        n = self.total / (1-(1+b*self.totaltime)*exp(-b*self.totaltime))
        f = lambda x: n*(1-(1+b*x)*exp(-b*x))-self.total-1
        mttf = -1
        if n - self.total > 1.0:
            try:
                mttf = self.Solve(f, self.totaltime+0.01, self.totaltime*4.0) - self.totaltime
            except:
                mttf = -1
        return {"n":n, 
                "b":b, 
                "mttf":mttf, 
                "conf1":"Not implemented", 
                "conf2":"Not implemented",
                "fmean":lambda x: n*(1-(1+b)*exp(-b*x)),
                "fint": lambda x: n*b*b*x*exp(-b*x)}     