from Systems.PointSystem import PointSystem
from Methods.ParetoOptimization.Genetic import *
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import copy, pickle
import random

class NSGA(GeneticAlgorithm):
    
    def __init__(self, system):
        GeneticAlgorithm.__init__(self, system)
        
    def _select(self):
        def CompareFit(x, y):
            if x.score > y.score:
                return 1
            else:
                return -1
        for p in self.population:
            p.score = None
        C = 100.0/len(self.population)       
        not_sorted = copy.deepcopy(self.population)
        self.population = []
        while True:    
            tmp = []
            chromosomes = []
            for s in not_sorted:
                self.system.Decode(s.chromosome)
                chromosomes.append({"rel":self.system.GetReliability(), "cost":self.system.GetCost()})      
            for s in not_sorted:
                self.system.Decode(s.chromosome)
                cur = {"rel":self.system.GetReliability(), "cost":self.system.GetCost()}  
                if not ExistsDominatingStrictly(cur, chromosomes):
                    tmp.append(s)
            for t in tmp:
                t.score = C * len(tmp)
                self.population.append(copy.deepcopy(t))
            not_sorted_2 = []
            for s in not_sorted:
                if s.score == None:
                    not_sorted_2.append(copy.deepcopy(s))
            if not_sorted_2 == []:
                break
            not_sorted = copy.deepcopy(not_sorted_2)
          
        self.population.sort(key = lambda x: x.score)#cmp = CompareFit)
        assert len(self.population) == ParetoFrontSize
        self.best = self.population[:int(len(self.population)*0.85)]

def NSGA_wrapper(system):
    n = NSGA(system)
    n.Start()
    sol = []
    for r in n.population:
        system.Decode(r.chromosome)
        sol.append({"rel":system.GetReliability(), "cost":system.GetCost()})
    return sol, n.population