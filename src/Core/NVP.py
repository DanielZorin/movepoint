'''
Created on 13.12.2010

@author: juan
'''
from Core.RedundancyTechnique import RedundancyTechnique
import itertools

class NVP(RedundancyTechnique):
    
    pall = None
    pd = None
    prv = None
    
    def __init__(self, soft, hard, pall, pd, prv):
        RedundancyTechnique.__init__(self, "nvp", hard, soft)
        self.pall = pall
        self.pd = pd
        self.prv = prv
    
    def GetReliability(self):
        # NVP/0/n
        if len(self.hardware) <= 1:
            res = 0.0
            res += (1 - self.prv)
            res += self.prv * (1 - self.prv)
            res += self.prv * self.prv * (1 - self.prv)
            res += self.prv ** 3 * (1 - self.pd)
            res += self.prv ** 3 * self.pd * (1 - self.pall)
            tmp = self.prv ** 3 * self.pd * self.pall 
            if len(self.software) % 2 == 0:
                self.software = self.software[:len(self.software)-1]
            for i in range(int(len(self.software) / 2) + 1, len(self.software)+1):
                faults = itertools.combinations(self.software, i)
                for combination in faults:
                    prob = 1.0
                    for v in self.software:
                        if v in combination:
                            prob *= v.reliability
                        else:
                            prob *= 1 - v.reliability
                    res += tmp * prob
            return res
        # NVP/1/1
        elif len(self.hardware) == 3:
            res = 0.0
            res += 1 - self.prv
            res += (1 - self.prv) * self.prv
            res += (1 - self.prv) * self.prv ** 2
            res += (1 - self.pd) * self.prv ** 3
            res += self.pd * self.prv ** 3 * (1 - self.pall)
            q1 = self.software[0].reliability
            q2 = self.software[1].reliability
            q3 = self.software[2].reliability
            h = self.hardware[0].reliability
            tmp = self.pd * self.prv ** 3 * self.pall
            res += (1 - q1) * (1 - q2) * tmp
            res += (1 - q3) * (1 - q2) * q1 * tmp
            res += (1 - q1) * (1 - q3) * q2 * tmp
            # The general formula is for 3 different versions of hardware. 
            # We consider them identical
            res += h * (1 - h) ** 2 * (1 - q1) * q2 * q3 * tmp
            res += h * (1 - h) ** 2 * q3 * (1 - (1 - q1) * (1 - q2)) * tmp
            res += q1 * q2 * (1 - q3) * h * (1 - h) ** 2 * tmp
            res += h * (1 - h) ** 2 * q2 * (1 - (1 - q1) * (1 - q3)) * tmp
            res += q1 * q3 * (1 - q2) * h * (1 - h) ** 2 * tmp
            res += h * (1 - h) ** 2 * q1 * (1 - (1 - q2) * (1 - q3)) * tmp
            res +=  2 * (1 - q1) * q2 * q3 * h * h * (1 - h) * tmp
            res +=  2 * (1 - q2) * q1 * q3 * h * h * (1 - h) * tmp
            res +=  2 * (1 - q3) * q2 * q1 * h * h * (1 - h) * tmp
            return res