'''
Created on 13.12.2010

@author: juan
'''

class RedundancyTechnique:
    ''' Represents an abstract technique used to improve reliability by adding reserve components
    
    :param name: Name
    :param hard: List of :class:`~Core.Hardware.Hardware` objects used in the technique
    :param soft: List of :class:`~Core.Software.Software` objects used in the technique'''
    
    def __init__(self, name, hard, soft):
        self.name = name
        self.hardware = hard
        self.software = soft
        #FIXME: Add standard functions here
        self.reliabilityFunction = None
        
    def __str__(self):
        return str(self.name) + " " + str(self.hardware) + " " + str(self.software)