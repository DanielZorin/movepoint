'''
Created on 12.02.2011

@author: juan
'''
# TODO: find an alternative for mpmath
#from Optimize.mpmath import erfinv
import math

class ZTest:
    ''' Implementation of a simple one-sample Z-test for a sample of Bernoulli distributed variables
    
    :param method: A function that takes an object from the samlple and returns some other object as a result. 
    :param sample: A list of objects
    :param func: A function that takes the result of "method" and evaluates it thus returning the actual value of the random variable to be tested
    :param log: File for debug output'''
    
    significance = 0.05
    
    def __init__(self, method, sample, func, log=None):
        self.method = method
        self.sample = sample
        self.valueFunction = func
        if log != None:
            self.log = open(log, "w")
        else:
            f = open("default_log.txt","w")
            self.log = f
    
    def _collectData(self):
        result = []
        for i in range(len(self.sample)):
            solution = self.method(self.sample[i])
            print(i, "iteration")
            result.append(solution) 
        return result   
    
    def _getNumericalSample(self, result):
        res = []
        for i in range(len(result)):
            v = self.valueFunction(result[i])
            #print(i, "iteration")
            res.append(v)
            self.log.write("Experiment " + str(i) + " returned " + str(v) + "\n")
        return res
    
    def Test(self, param):
        ''' Tests whether the valueFunction(sample) has Bernoulli distribution with parameter param.'''
        result = self._collectData()
        var = self._getNumericalSample(result)          
        p = float(sum(var)) / float(len(self.sample))
        criterium = (p - param) / (math.sqrt(param*(1-param)/len(self.sample)))
        criticalValue = math.sqrt(2) * -1.16309 # erfinv(2 * self.significance - 1)
        self.log.write("Success rate: "+ str(p) + "\n")
        self.log.write("Criterium: "+ str(criterium) + "\n")
        self.log.write("Critical value: "+ str(criticalValue) + "\n")
        return p
        # Now it's more important to get the actual percentage
        if criterium > criticalValue:
            return True
        else:
            return False