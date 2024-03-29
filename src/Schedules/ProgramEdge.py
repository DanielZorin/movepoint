'''
Created on 03.11.2010

@author: juan
'''

class ProgramEdge(object):
    '''Represents an edge of the program data flow graph'''
    
    source = None
    ''' First :class:`vertex <Schedules.ProgramVertex.ProgramVertex>` '''
    
    destination = None
    ''' Second :class:`vertex <Schedules.ProgramVertex.ProgramVertex>`'''
    
    volume = None
    '''Volume of data sent over this edge'''

    name = ""

    def __init__(self, src, dst, v):
        self.source = src
        self.destination = dst
        self.volume = v
        
    def __str__(self):
        return "Edge (" + str(self.source.number) +"," + str(self.destination.number) + "): volume = " + str(self.volume) + "\n"