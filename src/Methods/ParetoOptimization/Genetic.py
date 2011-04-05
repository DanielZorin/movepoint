from Systems.PointSystem import PointSystem
from Core.Common import *
from Methods.ParetoOptimization.Settings import *
import copy, pickle
import random

class Chromosome(object):
    seperator = ''

    def __init__(self, chromosome=None, length=0):
        self.chromosome = chromosome or self._makechromosome()
        self.length = length
        self.score = None  # set during evaluation
    
    def _makechromosome(self):
        "makes a chromosome from randomly selected alleles."
        return zeros(self.length)

    def evaluate(self, optimum=None):
        "this method MUST be overridden to evaluate individual fitness score."
        pass
    
    def crossover(self, other):
        "override this method to use your preferred crossover method."
        return self._twopoint(other)
    
    def mutate(self, gene):
        "override this method to use your preferred mutation method."
        self._pick(gene) 

    def __repr__(self):
        "returns string representation of self"
        return '<%s chromosome="%s" score=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str,self.chromosome)), self.score)

    def __cmp__(self, other):
        res = self.chromosome != other.chromosome
        return res
    
    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin


class GeneticAlgorithm(object):
    def __init__(self, system):
        self.system = system
        self.generation = 0
        self.population = self._makepopulation()
        self.next_population = []
        self.best = []
        self.iteration = 0
        self.report()
        
    #Create initial population (random)
    def _makepopulation(self):
        lst = []
        i = 0
        while i < ParetoFrontSize:
            tmp = self.system.GenerateRandomSolution()
            if not (tmp in lst):
                lst.append(tmp)
                i += 1
        res = []
        for s in lst:
            res.append(Chromosome(s))
        return res
    
    def _goal(self):
        return self.generation > MaximumIterations
    
    def step(self):
        self._select()
        self._crossover()
        self._mutation()
        self.generation += 1
        self.report()
    
    def _crossover(self):
        self.next_population = []
        i = 0
        while len(self.next_population) < ParetoFrontSize:
            mate1 = copy.deepcopy(self.best[random.randint(0,len(self.best)-1)])
            mate2 = copy.deepcopy(self.best[random.randint(0,len(self.best)-1)])
            if mate1 == mate2:
                pass
            number = random.randint(0, len(mate1.chromosome)-1)
            tmp = copy.deepcopy(mate1.chromosome[number])
            mate1.chromosome[number] = copy.deepcopy(mate2.chromosome[number])
            mate2.chromosome[number] = tmp
            if not (mate1 in self.next_population):
                self.next_population.append(mate1)
                i = 0
            if not (mate2 in self.next_population):
                self.next_population.append(mate2)  
                i = 0
            i += 1
            if i > 500:
                self.next_population.append(mate1)
                self.next_population.append(mate2)
        self.next_population = self.next_population[:ParetoFrontSize]
        self.population = copy.deepcopy(self.next_population) #[:Settings.ParetoFrontSize]

    def _select(self):
        "override this to use your preferred selection method"
        print("select parent")
    
    def _mutation(self):
        for i in range(len(self.population)):
            s = random.random()
            if s < MutationProbability:
                index = random.randint(0, len(self.population[i].chromosome)-1)
                flag = False
                while flag == False:
                    a, b = self.system.Encode()
                    new = copy.deepcopy(self.population[i])
                    if b[index]["hardware"]-1 >= 1:
                        new.chromosome[index]["hardware"] = random.randint(1, b[index]["hardware"]-1)
                    if b[index]["software"]-1 >= 1:
                        new.chromosome[index]["software"] = random.randint(1, b[index]["software"]-1)
                    if self.system.TestSolution(new.chromosome) == True:
                        flag = True
                        self.population[i] = new
        for s in self.population:
            if self.system.Decode(s.chromosome) == False:
                raise "error"
        self.system._default()

    def report(self):
        print("generation: ", self.generation)
        
    def Start(self):
        while not self._goal():
            self.step()