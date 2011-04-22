from Systems.PointSystem import PointSystem
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import random, copy

def PAES(system):
    '''.. warning:: Describe the algorithm here'''
    
    iteration = 0
    paretofront = []
    paretosolutions = []
    X = system.GenerateRandomSolution()
    while iteration < MaximumIterations:
        X1 = copy.deepcopy(X)
        for n in range(3):
            i = random.randint(0,len(X)-1)           
            while True:
                not_used, max = system.Encode()
                X1[i]["hardware"] = random.randint(1, max[i]["hardware"])
                X1[i]["software"] = random.randint(1, max[i]["software"])
                if system.Decode(X1) == True:
                    break
        X1data = {"rel":system.GetReliability(), "cost":system.GetCost()}
        system.Decode(X)
        Xdata = {"rel":system.GetReliability(), "cost":system.GetCost()}
        if Dominates(Xdata, X1data):
            best = Xdata
        elif Dominates(X1data, Xdata):
            best = X1data
            X = copy.deepcopy(X1)
        else:
            Xc = 0
            X1c = 0
            for p in paretofront:
                if Dominates(Xdata, p):
                    Xc += 1
                if Dominates(X1data, p):
                    X1c += 1
            if Xc > X1c:
                best = X1data
            else:
                best = Xdata
                X = copy.deepcopy(X1)
        a = b = False
        tmppareto = []
        tmppareto2 = []
        index = 0
        for cur in paretofront:
            if DominatesStrictly(cur, best):
                a = True
            if Dominates(best, cur):
                b = True
            if b == False:
                tmppareto.append(cur)
                tmppareto2.append(paretosolutions[index])
            index += 1
            b = False
        if a == False:
            tmppareto.append(best)
            tmppareto2.append(X)
        paretofront = tmppareto
        paretosolutions = tmppareto2  
        iteration += 1
    return paretofront, paretosolutions