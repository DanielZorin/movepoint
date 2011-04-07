'''
Created on 07.04.2011

@author: juan
'''
class Error(object):
    '''
    classdocs
    '''

    def __init__(self, time, programmer, severity, item):
        self.time = time
        self.programmer = programmer
        self.severity = severity
        self.item = item