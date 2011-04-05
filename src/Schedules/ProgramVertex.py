'''
Created on 03.11.2010

@author: juan
'''

class ProgramVertex(object):

    number = None
    time = None
    versions = None
    
    def __init__(self, n, c):
        self.number = n
        self.time = c
        self.versions = []
    
    def __str__(self):
        return "Vertex " + str(self.number) + "\n"
    