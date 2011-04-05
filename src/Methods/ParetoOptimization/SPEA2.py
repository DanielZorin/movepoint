from Systems.SystemGenerator import *
from Systems.PointSystem import PointSystem
from Methods.ParetoOptimization.Genetic import *
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import copy, pickle, math
import random

class SPEA2(GeneticAlgorithm):
    
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
        joint = self.population + self.S
        jointdata = data + self.Sdata
        strength = []
        for i in range(len(joint)):
            counter = 0
            for j in range(len(joint)):
                if DominatesStrictly(jointdata[i], jointdata[j]):
                    counter += 1
            strength.append(counter)
        
        for i in range(len(joint)):
            counter = 0
            for j in range(len(joint)):
                if DominatesStrictly(jointdata[j], jointdata[i]):
                    counter += strength[j]
            joint[i].score = counter    
        
        joint.sort(key = lambda x: x.score)#cmp = CompareFit)   
        
        def OddElement(lst):
            nearest = []
            for e in lst:
                #TODO: What the heck is this shit?!
                min = 9000000000000
                for p in lst:
                    if p != e:
                        r = math.sqrt((p["rel"]-e["rel"])**2 + (p["cost"]-e["cost"])**2)
                        if r < min:
                            min = r
                nearest.append(min)
            for e in lst:
                a = True
                for p in lst:
                    if nearest[lst.index(e)] > nearest[lst.index(p)]:
                        a = False
                if a == True:
                    return lst.index(e)
        if len(self.S) < ParetoFrontSize:
            i = 0
            while len(self.S) != ParetoFrontSize:
                if i == len(joint):
                    break
                if not (joint[i] in self.S):
                    self.S.append(joint[i])
                    self.system.Decode(joint[i].chromosome)
                    self.Sdata.append({"rel":self.system.GetReliability(), "cost":self.system.GetCost()})        
                i += 1
        elif len(self.S) > ParetoFrontSize:
            while len(self.S) != ParetoFrontSize:
                i = OddElement(self.Sdata)
                del self.S[i]
                del self.Sdata[i]

        self.best = joint[:int(len(joint)*0.85)]

def SPEA2_wrapper(system):
    n = SPEA2(system)
    n.Start()
    sol = []
    for r in n.population:
        system.Decode(r.chromosome)
        sol.append({"rel":system.GetReliability(), "cost":system.GetCost()})
    return sol, n.population