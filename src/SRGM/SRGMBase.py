'''
Created on 06.04.2011

@author: juan
'''

class SRGMBase(object):
    '''
    Represents a basic Software REliability Growth Model
    
    Args:
    
    * name - path of the file with testing data
    '''
    
    data = []
    '''List of times of errors'''
    
    total = 0
    '''Length of self.data'''
    
    totaltime = 0
    '''Time of the last detected fault'''

    def __init__(self):
        pass
        
    def SetData(self, data):
        self.data = [0]
        self.data += data
        self.total = len(self.data)-1
        self.totaltime = self.data[self.total]