from Systems.PointSystem import PointSystem
from Core.Common import *
from Methods.ParetoOptimization.Genetic import *
from Methods.ParetoOptimization.Settings import *
import copy, pickle
import random, math

class NPGA(GeneticAlgorithm):
    
    def __init__(self, system):
        GeneticAlgorithm.__init__(self, system)
        
    def _select(self):        
        self.best = []
        while len(self.best) < 0.85 * len(self.population):   
            i = random.randint(0, len(self.population)-1)
            j = random.randint(0, len(self.population)-1)
            if i == j:
                continue
            test = []
            p = 0
            while len(test) < TestSetSize:
                p +=1
                k = random.randint(0, len(self.population)-1)
                if k == i:
                    continue
                if k == j:
                    continue
                self.system.Decode(self.population[k].chromosome)
                cur = {"rel":self.system.GetReliability(), "cost":self.system.GetCost()}
                if not (cur in test):
                    test.append(cur)
                if p > 500:
                    break
            self.system.Decode(self.population[i].chromosome)
            a = {"rel":self.system.GetReliability(), "cost":self.system.GetCost()}
            self.system.Decode(self.population[j].chromosome)
            b = {"rel":self.system.GetReliability(), "cost":self.system.GetCost()}
            af = False
            bf = False
            for t in test:
                if DominatesStrictly(a, t):
                    af = True
                if DominatesStrictly(b, t):
                    bf = True
            if af == True:
                if bf == False:
                    if not (self.population[i] in self.best):
                        self.best.append(copy.deepcopy(self.population[i]))
            else:
                if bf == True:
                    if not (self.population[j] in self.best):
                        self.best.append(copy.deepcopy(self.population[j]))
            if ((af == True) and (bf == True)) or (af == False) and (bf == False):
                first = second = 0
                for p in self.population:
                    self.system.Decode(p.chromosome)
                    rel = self.system.GetReliability()
                    cost = self.system.GetCost()
                    f1 = math.sqrt((a["rel"]-rel)**2 * 10**4 + (a["cost"]-cost)**2)
                    f2 = math.sqrt((b["rel"]-rel)**2 * 10**4 + (b["cost"]-cost)**2)
                    if f1 < SharingRate:
                        first += 1 - f1 / SharingRate
                    if f2 < SharingRate:
                        second += 1 - f2 / SharingRate
                if first > second:
                    if not (self.population[i] in self.best):
                        self.best.append(copy.deepcopy(self.population[i]))
                else:
                    if not (self.population[j] in self.best):
                        self.best.append(copy.deepcopy(self.population[j]))
                    
def NPGA_wrapper(system):
    n = NPGA(system)
    n.Start()
    sol = []
    for r in n.population:
        system.Decode(r.chromosome)
        sol.append({"rel":system.GetReliability(), "cost":system.GetCost()})
    return sol, n.population