'''
Created on 03.11.2010

@author: juan
'''

class ProgramVertex(object):
    ''' Represents a vertex of the program data flow graph.'''

    number = None
    ''' Ordinal number of the task'''
    
    time = None
    '''Time required to complete the task'''
    
    versions = None
    '''List of versions of the task. See :class:`~Core.Version.Version` for reference'''

    name = ""
    '''Name displayed in the editor '''
    
    def __init__(self, n, c):
        self.number = n
        self.time = c
        self.versions = []
    
    def __str__(self):
        return "Vertex " + str(self.number) + "\n"
    