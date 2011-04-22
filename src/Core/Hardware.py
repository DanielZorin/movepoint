'''
Created on 13.12.2010

@author: juan
'''

class Hardware(object):
    ''' Represents abstract hardware, usually some kind of CPU used to run certain programs'''
    
    reliability = None
    ''' Reliability, a float in [0,1]'''
    
    variance = None
    ''' Reliability variance. If reliability is considered a random variable, the scalar reliability value
    is the mean, and this is the variance. '''
    
    cost = None
    ''' Abstract cost of the unit'''
    
    name = None
    ''' Name of the unit. Can be used to differentiate between the units. '''
    
    def __init__(self, rel=0.0, var=0.0, cost=0, name=""):
        self.reliability = rel
        self.variance = var
        self.cost = cost
        self.name = name
    def __str__(self):
        return str(self.name) + " " + str(self.reliability) + " " + str(self.variance) + " " + str(self.cost)