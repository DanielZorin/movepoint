from Systems.PointSystem import PointSystem
from Systems.SystemGenerator import SystemGenerator
from Methods.ParetoOptimization.FullIteration import GenerateParetoFront
from Core.Common import Cmeasure
#from Optimize.mpmath import erfinv
from Tests.Settings import *
import math,pickle

class QualityTest:
    def __init__(self, methods, log=None):
        self.methods = methods
        self.idealresult = []
        if log != None:
            self.log = log
        else:
            f = file("default_log.txt","w")
            self.log = f
    
    def Start(self):
        
        def Check(accuracy, i):
            m = 0
            for cur in self.result[i]:
                if math.sqrt(Cmeasure(cur, self.idealresult[i])**2 + Cmeasure(self.idealresult[i], cur)**2) >= accuracy:
                    m += 1
                    self.log.write("Experiment " + str(self.result[i].index(cur)) + " with method " + str(self.methods[i]) + " was successful\n")
                else:
                    self.log.write("Experiment " + str(self.result[i].index(cur)) + " with method " + str(self.methods[i]) +  " failed\n")
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
        
        self.result = []
        self.idealresult = []
        for i in range(len(self.methods)):
            self.result.append([])
        for i in range(NumberOfIterations):
            c = SystemGenerator(4,4,4)
            p = c.Generate()
            p._default()
            for j in range(len(self.methods)):
                front, solutions = self.methods[j](p)                
                self.result[j].append(front)
            a, b = GenerateParetoFront(p)
            self.idealresult.append(a)
            print(i, "iteration")
        for i in range(len(self.result)):
            accuracy = 0.4
            roundValue = 0.1
            previous = None
            while True:
                self.log.write("=============================\n")
                self.log.write("accuracy " + str(accuracy) + "\n")
                print(accuracy)
                if accuracy >= 1.0 or accuracy <= 0.0:
                    break
                r = Check(accuracy, i)
                if r == True:
                    accuracy += roundValue
                else:
                    accuracy -= roundValue
                if previous == None:
                    previous = r
                else:
                    if previous != r:
                        previous = None
                        roundValue /= 10.0
                        if roundValue == 0.0001:
                            break
                    else:
                        previous = r