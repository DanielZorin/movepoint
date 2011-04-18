from Systems.PointSystem import PointSystem
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import random, copy

def PESA(system):
    
    def initial(system):
        lst = []
        i = 0
        data = []
        while i < ParetoFrontSize:
            tmp = system.GenerateRandomSolution()
            if not (tmp in lst):
                lst.append(tmp)
                i += 1
                data.append({"rel":system.GetReliability(), "cost":system.GetCost()})
        return lst, data
    
    iteration = 0
    S = []
    Sdata = []
    P, Pdata = initial(system)
    for iteration in range(MaximumIterations):
        for i in range(len(Pdata)):
            if not ExistsDominatingStrictly(Pdata[i], Pdata):
                a = False
                b = False
                tmpS = []
                tmpSdata = []
                for j in range(len(S)):
                    if DominatesStrictly(Sdata[j], Pdata[i]):
                        a = True
                    if Dominates(Pdata[i], Sdata[j]):
                        b = True
                    if b == False:
                        tmpS.append(S[j])
                        tmpSdata.append(Sdata[j])
                    b = False
                if a == False:
                    tmpS.append(P[i])
                    tmpSdata.append(Pdata[i])
                S = tmpS
                Sdata = tmpSdata
        P = []
        Pdata = []
        while len(P) <= ParetoFrontSize:
            r = random.random()
            if r < MutationProbability:
                index = random.randint(0, len(S)-1)
                flag = False
                new = copy.deepcopy(S[index])
                for n in range(3):
                    i = random.randint(0,len(S[index])-1)           
                    while True:
                        not_used, max = system.Encode()
                        new[i]["hardware"] = random.randint(1, max[i]["hardware"])
                        new[i]["software"] = random.randint(1, max[i]["software"])
                        if system.Decode(new) == True:
                            break
                P.append(new)
                Pdata.append({"rel":system.GetReliability(), "cost":system.GetCost()})
            else:
                mate1 = copy.deepcopy(S[random.randint(0,len(S)-1)])
                mate2 = copy.deepcopy(S[random.randint(0,len(S)-1)])
                number = random.randint(0, len(mate1)-1)
                tmp = copy.deepcopy(mate1[number])
                mate1[number] = copy.deepcopy(mate2[number])
                mate2[number] = tmp
                if not (mate1 in P):
                    P.append(mate1)
                    system.Decode(mate1)
                    Pdata.append({"rel":system.GetReliability(), "cost":system.GetCost()})
                if not (mate2 in P):
                    P.append(mate2) 
                    system.Decode(mate2)
                    Pdata.append({"rel":system.GetReliability(), "cost":system.GetCost()}) 
    return Sdata, S