'''
Created on 06.04.2011

@author: juan
'''

class SRGM(object):
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

    def __init__(self, name):
        f = open(name, "r")
        self.data = f.read()
        self.data = self.data.split(',')
        f.close()
        self.total = 0
        for i in range(0,len(self.data)):
            self.data[i] = int(self.data[i])
        for i in range(1, len(self.data)):
            self.data[i] = self.data[i] - self.data[0] + 1
        self.data[0] = 1
        self.data.insert(0,0)
        self.total = len(self.data)-1
        self.totaltime = self.data[self.total]
    
    #TODO: Move to Common    
    def Solve(self, f, a, b):
        k = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fk = f(k)
        if b - a < 0.001:
            return b
        if(fk*fa < 0):
            return self.Solve(f, a, k)
        else:
            return self.Solve(f, k, b)