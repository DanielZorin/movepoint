'''
Created on 19.11.2010

@author: juan
'''

# TODO: move this class to Common package
class Threshold(object):
  
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