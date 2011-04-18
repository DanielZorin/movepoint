from Systems.PointSystem import PointSystem
from Systems.SystemGenerator import *
from Core.Common import *
from Methods.ParetoOptimization.FullIteration import *
from Methods.ParetoOptimization.Settings import *

# Generates Pareto front by random selection of solutions.
def RandomSelection(system):
    iteration = 0
    paretofront = []
    paretosolutions = []
    while iteration < MaximumIterations:
        new = system.GenerateRandomSolution()
        system.Decode(new)
        rel = system.GetReliability()
        cost = system.GetCost()
        a = b = False
        tmppareto = []
        tmppareto2 = []
        index = 0
        for cur in paretofront:
            if Dominates(cur, {"rel":rel, "cost":cost}):
                a = True
            if DominatesStrictly({"rel":rel, "cost":cost}, cur):
                b = True
            if b == False:
                tmppareto.append(cur)
                tmppareto2.append(paretosolutions[index])
            index += 1
            b = False
        if a == False:
            tmppareto.append({"rel":rel, "cost":cost})
            tmppareto2.append(new)
        paretofront = tmppareto
        paretosolutions = tmppareto2  
        iteration += 1
        if iteration % 500 == 0:
            print(iteration)
    return paretofront, paretosolutions