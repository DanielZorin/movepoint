'''
Created on 10.11.2010

@author: juan
'''

from Schedules.Operation import *
import random, math
import logging

class Genetics(object):
    ''' Genetics method adapted for scheduling.
    
    .. warning:: Write details here'''

    writeLog = False

    def __init__(self, data):
        self.data = data
        logging.basicConfig(level=logging.DEBUG)
    
    def write(self, *text):
        ''' Print debug information'''
        if self.writeLog:
            res = []
            for s in text:
                res.append(str(s))
            logger = logging.getLogger('SimulatedAnnealing')
            logger.debug(" ".join(res))
            
    def Step(self):
        ''' Makes a single iteration of the algorithm'''
