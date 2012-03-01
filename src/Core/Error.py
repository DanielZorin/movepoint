'''
Created on 07.04.2011

@author: juan
'''

class Error(object):
    '''
    Represents an error detected in software
    '''

    time = None
    ''' Time when the error occurred/was detected.'''
    
    programmer = None
    ''' ID of the programmer who wrote the code'''
    
    severity = None
    ''' Abstract level of severity '''
    
    item = None
    ''' Component/subprogram/whatever part of the program where the error occurred '''

    def __init__(self, time, programmer, severity, item):
        self.time = time
        self.programmer = programmer
        self.severity = severity
        self.item = item