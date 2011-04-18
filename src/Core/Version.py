'''
Created on 03.11.2010

@author: juan
'''

from Core.Software import Software

class Version(Software):

    number = None
    reliability = None
    task = None

    def __init__(self, task, number, reliability = 1.0):
        Software.__init__(self, reliability)
        self.number = number
        self.task = task
        
    def __str__(self):
        return "Version: " + str(self.number) + "\n"