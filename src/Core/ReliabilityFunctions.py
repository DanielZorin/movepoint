#TODO: this class is obsolete. All the techniques are now implemented in their own classes

class reliabilityFunctions:
    def __init__(self, pall, pd, prv):
        self.pall = pall
        self.pd = pd
        self.prv = prv
    
    def Calculate(self, method, hardware, software):
        if method.name == "none":
            return self.none(hardware, software)
        elif method.name == "nvp/0/1":
            return self.nvp01(hardware, software)
        elif method.name == "nvp/1/1":
            return self.nvp11(hardware, software)
        elif method.name == "rb/1/1":
            return self.rb11(hardware, software)
        else:
            raise "unknown reliability method"
    
    def nvp01(self, hardware, software):
        res = 0.0
        res += (1 - self.prv)
        res += self.prv * (1 - self.prv)
        res += self.prv * self.prv * (1 - self.prv)
        res += self.prv ** 3 * (1 - self.pd)
        res += self.prv ** 3 * self.pd * (1 - self.pall)
        res += self.prv ** 3 * self.pd * self.pall * (1 - hardware[0].reliability)
        tmp = self.prv ** 3 * self.pd * self.pall * hardware[0].reliability
        q1 = software[0].reliability
        q2 = software[1].reliability
        q3 = software[2].reliability
        res += tmp * (1 - q1) * (1 - q2)
        res += tmp * q1 * (1 - q2) * (1 - q3)
        res += tmp * q2 * (1 - q1) * (1 - q3)
        return 1 - res
    
    def nvp11(self, hardware, software):
        res = 0.0
        res += 1 - self.prv
        res += (1 - self.prv) * self.prv
        res += (1 - self.prv) * self.prv ** 2
        res += (1 - self.pd) * self.prv ** 3
        res += self.pd * self.prv ** 3 * (1 - self.pall)
        q1 = software[0].reliability
        q2 = software[1].reliability
        q3 = software[2].reliability
        h = hardware[0].reliability
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
        return 1 - res
    
    def rb11(self,hardware, software):
        res = 0.0
        res += (1 - self.prv)
        res += self.prv * (1 - self.pd)
        res += self.prv * self.pd * (1 - self.pall)
        tmp = self.prv * self.pd * self.pall
        h1 = hardware[0].reliability
        h2 = hardware[1].reliability
        s1 = software[0].reliability
        s2 = software[1].reliability
        res += tmp * (1 - h1) * (1 - h2)
        res += tmp * (1 - (1 - h1) * (1 - h2)) * (1 - s1) * (1 - s2)
        return 1 - res
    
    def none(self, hardware, software):
        return hardware[0].reliability * software[0].reliability