from Systems.PointSystem import PointSystem
from Systems.SystemGenerator import *
from Methods.ParetoOptimization.Genetic import *
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import copy, pickle
import random

class SPEA(GeneticAlgorithm):
    '''.. warning:: Describe the algorithm here'''
    
    def __init__(self, system):
        GeneticAlgorithm.__init__(self, system)
        self.S = []
        self.Sdata = []       
    def _select(self):
        def CompareFit(x, y):
            if x.score < y.score:
                return -1
            else:
                return 1
        
        data = []
        for cur in self.population:
            self.system.Decode(cur.chromosome)
            data.append({"rel":self.system.GetReliability(), "cost":self.system.GetCost()})
        for i in range(len(data)):
            if not ExistsDominatingStrictly(data[i], data):
                a = False
                b = False
                tmpS = []
                tmpSdata = []
                for j in range(len(self.S)):
                    if Dominates(self.Sdata[j], data[i]):
                        a = True
                    if Dominates(data[i], self.Sdata[j]):
                        b = True
                    if b == False:
                        tmpS.append(self.S[j])
                        tmpSdata.append(self.Sdata[j])
                    b = False
                if a == False:
                    tmpS.append(self.population[i])
                    tmpSdata.append(data[i])
                self.S = tmpS
                self.Sdata = tmpSdata
        for i in range(len(self.S)):
            counter = 0
            for p in data:
                if DominatesStrictly(p, self.Sdata[i]):
                    counter += 1
            self.S[i].score = float(counter)/float(len(data))
        for i in range(len(self.population)):
            counter = 1.0
            for j in range(len(self.Sdata)):
                if DominatesStrictly(self.Sdata[j], data[i]):
                    counter += self.S[j].score
            self.population[i].score = counter
        
        joint = self.population + self.S   
        # TODO: check this 
        joint.sort(key = lambda x: x.score) #cmp = CompareFit)
        self.best = joint[:int(len(joint)*0.85)]

def SPEA_wrapper(system):
    n = SPEA(system)
    n.Start()
    sol = []
    for r in n.population:
        system.Decode(r.chromosome)
        sol.append({"rel":system.GetReliability(), "cost":system.GetCost()})
    return sol, n.population