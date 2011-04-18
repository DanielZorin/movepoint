'''
Created on 13.12.2010

@author: juan
'''

class RedundancyTechnique:
    def __init__(self, name, hard, soft):
        self.name = name
        self.hardware = hard
        self.software = soft
        #FIXME: Add standard functions here
        self.reliabilityFunction = None
        
    def __str__(self):
        return str(self.name) + " " + str(self.hardware) + " " + str(self.software)