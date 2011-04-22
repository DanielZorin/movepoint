'''
Created on 06.04.2011

@author: juan
'''

from SRGM.SRGMBase import SRGMBase
from Core.Common import findroot
from math import log

class Logarithmic(SRGMBase):
    '''
    Represents the logarithmic model
    '''

    def __init__(self):
        SRGMBase.__init__(self)
    

    def LogarithmicFunc(self, x):
        sum = 0
        for i in range(1, self.total+1 ):     
            sum += 1/(1 + x*self.data[i])
        sum /= x
        sum -= self.totaltime*self.total / ( (1 + x*self.totaltime) * (log(1 + x*self.totaltime)) )
        return sum
    
    def Compute(self):
        b1 = findroot(self.LogarithmicFunc, 0.001, 2)
        b0 = self.total / log(1+b1*self.totaltime)
        tmp = b0*b1/(b1*self.totaltime + 1)
        mttf = 1/tmp
        return {"n":"Undefined", 
                "b":b1, 
                "mttf":mttf, 
                "conf1":"Not implemented", 
                "conf2":"Not implemented",
                "fmean":lambda x: b0*log(x*b1 + 1),
                "fint":lambda x: b0*b1 / (b1*x + 1)}  