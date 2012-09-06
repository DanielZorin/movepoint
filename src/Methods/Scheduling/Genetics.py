'''
Created on 10.11.2010

@author: juan
'''

from Schedules.Operation import *
import random, math
import logging

class Genetics(object):
    ''' Genetics method adapted for scheduling.
    
    .. warning:: Write details here'''

    writeLog = False

    population = []
    populationSize = 20
    mutationProbability = 0.1

    def __init__(self, data):
        self.data = data
        logging.basicConfig(level=logging.DEBUG)
    
    def write(self, *text):
        ''' Print debug information'''
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            logger = logging.getLogger('Genetics')
            logger.debug(" ".join(res))
           
    def Prepare(self):
        self.createPopulation()
             
    def Step(self):
        ''' Makes a single iteration of the algorithm'''
        print ("step")
        self.rank()
        self.crossover()
        self.selection()
        self.mutation()

    def createPopulation(self):
        self.population = []
        backup = self.data.system.schedule.Serialize()
        for i in range(self.populationSize):
            self.data.system.schedule.Randomize()
            time = self.data.interpreter.Interpret(self.data.system.schedule)
            rel = self.data.system.schedule.GetReliability()
            proc = self.data.system.schedule.GetProcessors()
            self.population.append([self.data.system.schedule.Serialize(),
                                    {"time":time, "reliability":rel, "processors":proc}])
        self.data.trace.addStep(Replacement(backup, self.population[0][0]), self.population[0][1])

    def rank(self):
        def rankfunc(x):
            rank = 0
            # TODO: add reliability here too
            if x[1]["time"] > self.data.system.tdir:
                # TODO: a bit dirty
                rank = self.data.system.tdir * len(self.data.system.program.vertices) * 10
            else:
                # Ranking by the number of processors. Solutions with equal number are ranked by time
                rank = x[1]["processors"] * self.data.system.tdir + x[1]["time"]
            return rank
        self.population = sorted(self.population, key=rankfunc, reverse=True)

    def crossover(self):
        for i in range(int(self.populationSize / 2)):
            pass

    def selection(self):
        self.rank()
        self.population = self.population[:self.populationSize]
        best = self.data.trace.getLast()[1]
        cur = self.population[0][1]
        new_time = cur["time"]
        new_rel = cur["reliability"]
        new_proc = cur["processors"]
        if new_time <= self.data.system.tdir and new_rel >= self.data.system.rdir:
            if new_proc < best["processors"]  or (new_proc == best["processors"] and new_time < best["time"]):
                self.data.trace.addStep(Replacement(self.data.trace.getLast()[0].new, self.population[0][0]), self.population[0][1])

    def mutation(self):
        pass