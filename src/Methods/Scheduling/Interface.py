'''
Created on 01.03.2011

@author: juan
'''
from Methods.Scheduling.SimulatedAnnealing import SimulatedAnnealing
from Methods.Scheduling.RandomSimulatedAnnealing import RandomSimulatedAnnealing
import copy

def RunMixed(sys):
    ''' Runs Simulated annealing with mixed strategy on a given system'''
    m = SimulatedAnnealing(sys)
    m.LoadConfig("config.xml")
    res = m.Start() 
    sys.schedule = res
    return sys

def RunIdle(sys):
    m = SimulatedAnnealing(sys)
    m.LoadConfig("config-idle.xml")
    res = m.Start()
    sys.schedule = res
    return sys

def RunDelay(sys):
    m = SimulatedAnnealing(sys)
    m.LoadConfig("config-delay.xml")
    res = m.Start() 
    sys.schedule = res
    return sys

def RunRandom(sys):
    m = RandomSimulatedAnnealing(sys)
    m.LoadConfig("config.xml")
    res = m.Start() 
    sys.schedule = res
    return sys

def RunRandomAndNormal(sys):
    sys2 = copy.deepcopy(sys)
    m = SimulatedAnnealing(sys)
    m.LoadConfig("config-three.xml")
    res = m.Start() 
    sys.schedule = res
    mr = RandomSimulatedAnnealing(sys2)
    mr.LoadConfig("config.xml")
    res2 = mr.Start() 
    sys2.schedule = res2
    return (sys, sys2)