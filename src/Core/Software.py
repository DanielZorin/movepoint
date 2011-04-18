'''
Created on 13.12.2010

@author: juan
'''

class Software(object):
    
    reliability = None
    variance = None
    cost = None
    name = None 
    
    def __init__(self, rel=0.0, var=0.0, cost=0, name=""):
        self.reliability = rel
        self.variance = var
        self.cost = cost
        self.name = name
        
    def __str__(self):
        return str(self.name) + " " + str(self.reliability) + " " + str(self.variance) + " " + str(self.cost)