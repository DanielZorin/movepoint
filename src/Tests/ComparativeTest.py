from Systems.PointSystem import PointSystem
from Systems.SystemGenerator import SystemGenerator
from Core.Common import Cmeasure
#from Optimize.mpmath import erfinv
from Tests.Settings import *
import math,pickle

class ComparativeTest:
    '''.. deprecated:: 0.1
    
    To be reimplemented as Z-test'''
    
    def __init__(self, methods, log=None):
        self.methods = methods
        self.systemGenerator = SystemGenerator(20,6,6)
        if log != None:
            self.log = log
        else:
            f = file("default_log.txt","w")
            self.log = f
    
    def CompareAllPairs(self):
        matrix = [[0 for i in range(len(self.methods))] for j in range(len(self.methods))]
        for i in range(len(self.methods)):
            for j in range(len(self.methods)):
                first = 0.0
                second = 0.0
                for n in range(100):
                    if self.matrices[n][i][j] > self.matrices[n][j][i]:
                        first += 1.0
                    else:
                        second += 1.0
                first /= 100.0
                second /= 100.0
                print(first, second)
                p = first
                criterium = (p - Stability) / (math.sqrt(Stability*(1-Stability)/NumberOfIterations))
                criticalValue = math.sqrt(2) * erfinv(2 * Significance - 1)
                if criterium > criticalValue:
                    print(self.methods[i], " is better than ", self.methods[j])
                    matrix[i][j] = 1
                p = second
                criterium = (p - Stability) / (math.sqrt(Stability*(1-Stability)/NumberOfIterations))
                criticalValue = math.sqrt(2) * erfinv(2 * Significance - 1)
                if criterium > criticalValue:
                    print(self.methods[j], " is better than ", self.methods[i])
                    matrix[j][i] = 1
        s = ""
        for i in range(len(self.methods)):
            for j in range(len(self.methods)):
                s += (str(matrix[i][j])+";")
            s += "\n"
        print(s) 
    
    def PrintMatrix(self):
        matrix = [[-1 for i in range(len(self.methods))] for j in range(len(self.methods))]
        for i in range(len(self.methods)):
            for j in range(len(self.methods)):
                tmp = 0.0
                for n in range(100):
                    tmp += self.matrices[n][i][j]
                matrix[i][j] = tmp/100.0 
        s = ""
        for i in range(len(self.methods)):
            for j in range(len(self.methods)):
                s += (str(matrix[i][j])+";")
            s += "\n"
        print(s)    
        print(matrix)
    
    def Start(self):
        self.result = []
        self.idealresult = []
        for i in range(len(self.methods)):
            self.result.append([])
        for i in range(NumberOfIterations):
            p = self.systemGenerator.Generate()
            p._default()
            for j in range(len(self.methods)):
                front, solutions = self.methods[j](p)                
                self.result[j].append(front)
            print(i, "iteration")
        self.matrices = []
        for n in range(NumberOfIterations):
            current = [[-1 for i in range(len(self.methods))] for j in range(len(self.methods))]
            for i in range(len(self.methods)):
                for j in range(len(self.methods)):
                    current[i][j] = Cmeasure(self.result[i][n], self.result[j][n])
            self.matrices.append(current)
        print(matrices)

class ComparativeStabilityTest:
    def __init__(self, methods, log=None):
        self.methods = methods
        sg = SystemGenerator(20,6,6)
        self.system = sg.Generate()
        if log != None:
            self.log = log
        else:
            f = file("default_log.txt","w")
            self.log = f
    
    def Start(self):
        self.result = []
        for i in range(len(self.methods)):
            self.result.append([])
        for i in range(NumberOfIterations):
            self.system._default()
            p = self.system
            for j in range(len(self.methods)):
                front, solutions = self.methods[j](p)                
                self.result[j].append(front)
            print(i, "iteration")
        self.matrices = []
        for n in range(NumberOfIterations):
            current = [[-1 for i in range(len(self.methods))] for j in range(len(self.methods))]
            for i in range(len(self.methods)):
                for j in range(len(self.methods)):
                    current[i][j] = Cmeasure(self.result[i][n], self.result[j][n])
            self.matrices.append(current)