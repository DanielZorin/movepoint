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
    mutationProbability = 0.4

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
        self.rank()
        self.crossover()
        self.selection()
        self.mutation()
        self.data.system.schedule.Deserialize(self.data.trace.getLast()[0].new)

    def createPopulation(self):
        self.population = []
        self.data.trace.deleteTail(self.data.system.tdir, self.data.system.rdir)
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
        self.population = sorted(self.population, key=rankfunc, reverse=False)

    def crossover(self):
        def mate(mate1, mate2):
            keys = [k for k in mate1[0][0].keys()]
            proc = random.randint(0, len(keys) - 1)
            #print ("selected proc ", keys[proc])
            proc = mate1[0][0][keys[proc]]
            s.Deserialize(mate2[0])
            #print("base schedule is ")
            #print(s)
            #print ("new proc is ")
            for v in proc:
                print (v)
            s.ReplaceProcessor(proc)
            time = self.data.interpreter.Interpret(s)
            rel = s.GetReliability()
            proc = s.GetProcessors()
            self.population.append([s.Serialize(),
                                    {"time":time, "reliability":rel, "processors":proc}])

        #print ("=================================================")
        
        s = self.data.system.schedule
        for i in range(int(self.populationSize / 2)):
            m1 = self.population[i]
            m2 = self.population[i + 1]
            #print ("mating 1")
            #print ("begin...")
            mate(m1, m2)
            
            #print ("mating 2")
            #print ("begin...")
            mate(m2, m1)

    def selection(self):
        self.rank()
        self.population = self.population[:self.populationSize]
        last = self.data.trace.getLast()[1]
        best = self.data.trace.getBest()[1]
        cur = self.population[0][1]
        new_time = cur["time"]
        new_rel = cur["reliability"]
        new_proc = cur["processors"]
        if new_time <= self.data.system.tdir and new_rel >= self.data.system.rdir:
            if new_proc < last["processors"] or new_time < last["time"]:
                self.data.trace.addStep(Replacement(self.data.trace.getLast()[0].new, self.population[0][0]), self.population[0][1])
            if new_proc < best["processors"] or (new_proc == best["processors"] and new_time < best["time"]):
                self.data.trace.setBest(self.data.trace.length() - 1)

    def mutation(self):
        newpopulation = []
        for c in self.population:
            if random.random() < self.mutationProbability:
                self.data.system.schedule.Deserialize(c[0])
                s = self.data.system.schedule
                keys = [m for m in s.vertices.keys()]
                while True:
                    m1 = keys[random.randint(0, len(keys) - 1)]
                    m2 = keys[random.randint(0, len(keys) - 1)]
                    n1 = random.randint(0, len(s.vertices[m1]) - 1)
                    n2 = random.randint(0, len(s.vertices[m2]))
                    s1 = s.vertices[m1][n1]
                    if (m1 != m2) or (n1 != n2):
                        if s.TryMoveVertex(s1, n1, s.vertices[m2][0].m, n2) == True:
                            s.MoveVertex(s1, n1, s.vertices[m2][0].m, n2)
                            break
                time = self.data.interpreter.Interpret(s)
                rel = s.GetReliability()
                proc = s.GetProcessors()
                newpopulation.append([s.Serialize(),
                                        {"time":time, "reliability":rel, "processors":proc}])
            else:
                newpopulation.append(c)
        self.population = newpopulation