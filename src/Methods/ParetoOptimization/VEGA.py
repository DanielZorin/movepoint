from Systems.PointSystem import PointSystem
from Methods.ParetoOptimization.Genetic import *
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import copy, pickle
import random

class VEGA(GeneticAlgorithm):
    '''.. warning:: Describe the algorithm here'''
    
    def __init__(self, system):
        GeneticAlgorithm.__init__(self, system)
        
    def _select(self):
        def CompareRel(x, y):
            self.system.Decode(x.chromosome)
            rel = self.system.GetReliability()
            self.system.Decode(y.chromosome)
            rel2 = self.system.GetReliability()
            if rel > rel2:
                return 1
            else:
                return -1
        
        def CompareCost(x, y):
            self.system.Decode(x.chromosome)           
            c = self.system.GetCost()
            self.system.Decode(y.chromosome)            
            c2 = self.system.GetCost()
            if c > c2:
                return 1
            else:
                return -1
        
        i = random.random()
        self.best = []
        # Select by reliability
        if i < 0.5:
            # TODO: this is a super hack to include multiple instructions in lambda
            self.population.sort(key = lambda x: (self.system.Decode(x.chromosome), self.system.GetReliability())[1])#cmp = CompareRel)
            self.best = self.population[:int(len(self.population)*0.85)]
        # Select by cost
        else:
            self.population.sort(key = lambda x: (self.system.Decode(x.chromosome), self.system.GetCost())[1])#cmp = CompareCost)
            self.best = self.population[:int(len(self.population)*0.85)]

def VEGA_wrapper(system):
    n = VEGA(system)
    n.Start()
    sol = []
    for r in n.population:
        system.Decode(r.chromosome)
        sol.append({"rel":system.GetReliability(), "cost":system.GetCost()})
    return sol, n.population