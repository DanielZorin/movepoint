'''
Created on 03.11.2010

@author: juan
'''

class ProgramEdge(object):
    
    source = None
    destination = None
    volume = None

    def __init__(self, src, dst, v):
        self.source = src
        self.destination = dst
        self.volume = v
        
    def __str__(self):
        return "Edge (" + str(self.source.number) +"," + str(self.destination.number) + "): volume = " + str(self.volume) + "\n"