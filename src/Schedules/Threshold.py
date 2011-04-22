'''
Created on 19.11.2010

@author: juan
'''

# TODO: move this class to Common package
class Threshold(object):
    ''' Threshold function: a function of one scalar parameter x.
    
    Represents the probability to choose a new approximation on a certain iteration.
    
    The function is supposed to be decreasing with the growth of x.
    
    :param type: One of the predefined types: linear or square
    :param cachedparams: The dictionary of parameters. Used to serialize the Threshold object.
    :param params: A list of other params, specifically coefficients of the polynom
    ''' 
    
    def __init__(self, type, cachedparams=None, **params):

        self.type = type
        if cachedparams != None:
            self.params = cachedparams
        else:
            self.params = params
        if type == "linear":
            self.f = lambda x: self.params["a"] * x + self.params["b"]
        elif type == "square":
            self.f = lambda x: self.params["a"] * x**2 + self.params["b"] * x + self.params["c"]