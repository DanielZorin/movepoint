'''
Created on 06.04.2011

@author: juan
'''

from SRGM.SRGMBase import SRGMBase
from Core.Common import findroot
from math import exp, sqrt, log

class GoelOkumoto(SRGMBase):
    '''
    Represents the Goel-Okumoto model (also known as exponential)
    '''

    def __init__(self):
        SRGMBase.__init__(self)
               
    def GOfunc(self, x):
        sum = 0
        i = 1
        while i < self.total+1: 
            if i < self.total:
                if self.data[i] != self.data[i+1]:     
                    sum += (self.data[i]*exp(-x*self.data[i]) - self.data[i-1]*exp(-x*self.data[i-1])) / (exp(-x*self.data[i-1]) - exp(-x*self.data[i]))
                    i += 1
                else:
                    k = 1
                    tmp = self.data[i-1]
                    while self.data[i] == self.data[i+1]:
                        k += 1
                        i += 1
                        if i >= self.total - 1:
                            break
                    sum += k * (self.data[i]*exp(-x*self.data[i]) - tmp*exp(-x*tmp)) / (exp(-x*tmp) - exp(-x*self.data[i]))
                    i += 1
            else:
                if self.data[i] == self.data[i-1]:
                    break
                sum += (self.data[i]*exp(-x*self.data[i]) - self.data[i-1]*exp(-x*self.data[i-1])) / (exp(-x*self.data[i-1]) - exp(-x*self.data[i]))
                i += 1     
        sum -= self.totaltime*self.total* exp(-x*self.totaltime) / (1 - exp(-x*self.totaltime))
        return sum
    
    def GOConfidence(self, b):
        sum = 0
        i = 1
        while i < self.total+1: 
            if i < self.total:
                if self.data[i] != self.data[i+1]:     
                    sum += (self.data[i] - self.data[i-1])**2 * exp(-b*(self.data[i] + self.data[i-1])) / ((exp(-b*self.data[i-1]) - exp(-b*self.data[i]))**2)
                    i += 1
                else:
                    k = 1
                    tmp = self.data[i-1]
                    while self.data[i] == self.data[i+1]:
                        k += 1
                        i += 1
                        if i >= self.total - 1:
                            break
                    sum += k * (self.data[i] - tmp)**2 * exp(-b*(self.data[i] + tmp)) / ((exp(-b*tmp) - exp(-b*self.data[i]))**2)
                    i += 1
            else:
                if self.data[i] == self.data[i-1]:
                    break
                sum += (self.data[i] - self.data[i-1])**2 * exp(-b*(self.data[i] + self.data[i-1])) / ((exp(-b*self.data[i-1]) - exp(-b*self.data[i]))**2)
                i += 1     
        sum -= self.total*self.totaltime*self.totaltime*exp(b*self.totaltime)/((exp(b*self.totaltime)-1)**2)
        bconf = 1.645/sqrt(1)#tmp)
        if b - bconf > 0:
            conf1 = self.total/(1-exp(-(b+bconf)*self.totaltime))
            conf2 = self.total/(1-exp(-(b-bconf)*self.totaltime))
        else:
            conf1 = self.total/(1-exp(-(b+bconf)*self.totaltime))
            conf2 = self.total/(1-exp(-(b)*self.totaltime))
        return conf1, conf2
       
    def Compute(self):
        b = findroot(self.GOfunc, 0.00001, 0.1)
        n = self.total / (1-exp(-b*self.totaltime))
        tmp = exp(-b*self.totaltime)-(1/n)
        if tmp > 0:
            mttf = -1/b * log(tmp) - self.totaltime
        else:
            mttf = 0
        conf1, conf2 = self.GOConfidence(b)
        #if b == 0.1:
        #    return -2, -2, -2, -2, -2
        return {"n":n, 
                "b":b, 
                "mttf":mttf, 
                "conf1":conf1, 
                "conf2":conf2,
                "fmean":lambda x: n*(1-exp(-b*x)),
                "fint": lambda x: n*b*exp(-b*x)}