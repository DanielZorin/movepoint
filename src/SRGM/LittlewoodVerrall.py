'''
Created on 06.04.2011

@author: juan
'''

from .SRGM import SRGM
from math import exp, sqrt, log

class LittlewoodVerrall(SRGM):
    '''
    Represents the LV model
    '''

    def __init__(self):
        SRGM.__init__(self)
        
    def Compute(self):
        def f1(a,b,c):
            res = 1
            for i in range(1, self.total+1):
                res *= (b + c*i)/(self.data[i] - self.data[i-1] + b + c*i)
            res = log(res)
            res += self.total / a
            return res
        def f2(a,b,c):
            res = 0.0
            for i in range(1, self.total+1):
                res += a / (b + c*i) - (a + 1) / (self.data[i] - self.data[i-1] + b + c*i)
            return res
        def f3(a,b,c):
            res = 0
            for i in range(1, self.total+1):
                res += a * i / (b + c*i) - (a + 1) * i / (self.data[i] - self.data[i-1] + b + c*i)            
            return res
        def line(a,b):
            res = sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
            return res
        
        x0 = [0.1,0.1,0.1]
        x1 = [1000.0,1000.0,1000.0]
        square = 10.0
        try:
            while square > 0.01:
                x0[0] = x1[0]
                x0[1] = x1[1]
                x0[2] = x1[2]
                x1[0] = f1(x0[0], x0[1], x0[2])
                x1[1] = f2(x0[0], x0[1], x0[2])
                x1[2] = f3(x0[0], x0[1], x0[2])
                square = x1[0]**2+x1[1]**2+x1[2]**2
                x1[0] += x0[0]
                x1[1] += x0[1]
                x1[2] += x0[2]
        except: #ValueError:
            print("ZERO")
        p = x1
        # TODO: it doesn't work at all
        return {"n":"Undefined", 
                "b":"Undefined", 
                "mttf":(x1[1]+x1[2]*(self.total+1))/(x1[0]-1), 
                "conf1":"Not implemented", 
                "conf2":"Not implemented",
                "fmean":lambda x: (p[0]-1)/(4*p[2]*(p[0]-1)) * sqrt(2*p[2]*(p[0]-1)*x + p[1]**2),
                "fint":lambda x: (p[0]-1)/sqrt(p[1]**2+2*p[2]*x*(p[0]-1))}
    