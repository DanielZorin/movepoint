from Systems.PointSystem import PointSystem
from Core.Common import *
from Systems.SystemGenerator import SystemGenerator
import copy, pickle

def GenerateSolutions(system):
    ''' Returns a list of all possible variants of the system. '''
    
    result = []
    v, max = system.Encode()
    for i in range(len(v)):
        v[i]["software"] = 1
        v[i]["hardware"] = 1
    result.append(v)
    final = []
    for i in range(len(v)):
        tmp = []
        print(i, "/", len(v))
        j = 0
        l = len(result)
        print(l)
        for s in result:
            j+=1
            for k1 in range(1, max[i]["software"]):
                for k2 in range(1, max[i]["hardware"]):
                    new = copy.deepcopy(s)
                    new[i]["software"] = k1
                    new[i]["hardware"] = k2
                    if system.TestSolution(new):
                        tmp.append(new)
                        final.append(new)
            if j % 100 == 0:
                print(j, "/", l)
        result = tmp
    return final 

def GenerateParetoFront(system):
    ''' Returns a list of reliability/cost values of Pareto front and 
    a list of the corresponding solutions.'''
    result = []
    v, max = system.Encode()
    for i in range(len(v)):
        v[i]["software"] = 1
        v[i]["hardware"] = 1
    result.append(v)
    paretofront = []
    paretosolutions = []
    for i in range(len(v)):
        tmp = []     
        print(i, "/", len(v))
        j = 0
        l = len(result)
        for s in result:
            j += 1
            for k1 in range(1, max[i]["software"]+1):
                for k2 in range(1, max[i]["hardware"]+1):                 
                    new = copy.deepcopy(s)
                    new[i]["software"] = k1
                    new[i]["hardware"] = k2
                    if system.TestSolution(new) == False:
                        pass
                    else:
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
                        tmp.append(new)
            if j % 100 == 0:
                print(j, "/", l)
        result = tmp
        #print result
    return paretofront, paretosolutions

def GenerateParetoFrontOptimized(system):
    ''' Returns a list of reliability/cost values of Pareto front and 
    a list of the corresponding solutions.'''
    def next(v, max):
        new = copy.deepcopy(v)
        for i in range(len(v)):
            if v[i]["hardware"] != max[i]["hardware"]:
                new[i]["hardware"] += 1
                return new
            else:
                new[i]["hardware"] = 1
            if v[i]["software"] != max[i]["software"]:
                new[i]["software"] += 1
                return new
            else:
                new[i]["software"] = 1
    
    result = []
    v, max = system.Encode()
    total = 1
    i = 0
    for i in range(len(v)):
        v[i]["software"] = 1
        v[i]["hardware"] = 1
        total *= max[i]["hardware"] * max[i]["software"]
    paretofront = []
    paretosolutions = []
    while True: 
        i += 1
        if i % 1000 == 0:
            print(i, "/", total)    
        new = next(v, max)
        v = new
        if system.TestSolution(new) == False:
            pass
        else:
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
                if Dominates({"rel":rel, "cost":cost}, cur):
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
        if v == max:
            break 
    return paretofront, paretosolutions
    
