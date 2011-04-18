from Core.Common import Cmeasure
# TODO: find an alternative for mpmath
#from Optimize.mpmath import erfinv
from Tests.Settings import *
import math, pickle

class SimpleTest:
    def __init__(self, method, system, log=None, ideal=None):
        self.method = method
        self.idealresult = ideal
        self.system = system
        if log != None:
            self.log = log
        else:
            f = file("default_log.txt","w")
            self.log = f
    
    def Start(self):
        result = []
        p = self.system 
        for i in range(NumberOfIterations):
            front, solutions = self.method(p)
            print(i, "iteration")
            result.append(front)
        if self.idealresult == None:
            self.idealresult, not_used = Optimize.Methods.FullIteration.GenerateParetoFront(p)
        m = 0
        num = 1
        for cur in result:
            if math.sqrt(Cmeasure(cur, self.idealresult)**2 + Cmeasure(self.idealresult, cur)**2) >= DefaultAccuracy:
                m += 1
                self.log.write("Experiment " + str(num) + " was successful\n")
            else:
                self.log.write("Experiment " + str(num) + " failed\n")
            num += 1
        p = float(m) / float(NumberOfIterations)
        criterium = (p - Stability) / (math.sqrt(Stability*(1-Stability)/NumberOfIterations))
        criticalValue = math.sqrt(2) * 1#erfinv(2 * Significance - 1)
        self.log.write("Success rate: "+ str(p) + "\n")
        self.log.write("Criterium: "+ str(criterium) + "\n")
        self.log.write("Critical value: "+ str(criticalValue) + "\n")
        if criterium > criticalValue:
            return True
        else:
            return False