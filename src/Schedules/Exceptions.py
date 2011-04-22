'''
Created on 16.01.2011

@author: juan
'''

class SchedulerException(Exception):
    '''A base class for exceptions related to schedules'''
    
    message = ""
    '''Error message'''
    
    def __init__(self, m):
        self.message = m
        
class SchedulerFileException(SchedulerException):
    '''Thrown when the Xml file is inaccessible'''
    
    def __init__(self, m):
        self.message = "File doesn't exist or can't be opened: " + m
        
class SchedulerXmlException(SchedulerException):
    '''Thrown when the Xml is incorrect'''
    
    def __init__(self, m):
        self.message = "XML file is not well formed or has incorrect structure: " + m
        
class SchedulerTypeException(SchedulerException):
    '''Thrown in case of type mismatch'''
    
    def __init__(self, m1, m2):
        self.message = "Type error: expected " + m1 + " and got " + m2
