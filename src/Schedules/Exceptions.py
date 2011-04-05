'''
Created on 16.01.2011

@author: juan
'''
class SchedulerException(Exception):
    
    message = ""
    
    def __init__(self, m):
        self.message = m
        
class SchedulerFileException(SchedulerException):
    
    def __init__(self, m):
        self.message = "File doesn't exist or can't be opened: " + m
        
class SchedulerXmlException(SchedulerException):
    
    def __init__(self, m):
        self.message = "XML file is not well formed or has incorrect structure: " + m
        
class SchedulerTypeException(SchedulerException):
    
    def __init__(self, m1, m2):
        self.message = "Type error: expected " + m1 + " and got " + m2
