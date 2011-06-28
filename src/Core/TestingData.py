'''
Created on 07.04.2011

@author: juan
'''

import xml.dom.minidom, copy
from Core.Error import Error

class TestingData(object):
    '''
    Represents a set of testing data, i.e. the list of errors detected during testing and additional info
    '''
    
    errors = []
    ''' A list of :class:`~Core.Error.Error` objects'''
    
    errortimes = []
    ''' A list of times of all currently selected errors. Provided for convenience'''
    
    programmer = []
    ''' A set of programmer IDs. 
    Only errors with programmers from this list are selected and appear in :attr:`~Core.TestingData.TestingData.errortimes`
    If the list is empty, all errors are selected. '''
    
    severity = []
    ''' A set of severity levels. 
    Only errors with severity level from this list are selected and appear in :attr:`~Core.TestingData.TestingData.errortimes`
    If the list is empty, all errors are selected. '''
    
    item = []
    ''' A set of items/program module IDs. 
    Only errors with items from this list are selected and appear in :attr:`~Core.TestingData.TestingData.errortimes`
    If the list is empty, all errors are selected. '''
    
    startTime = None
    ''' Only errors that occurred after startTime are selected. By default it's zero'''
    
    endTime = None
    ''' Only errors that occurred before endTime are selected. By default it's the time of the last error'''

    def __init__(self, file=""):
        if file == "":
            self.errors = []
            self.errortimes = []
        else:
            self.LoadXml(file)
    
    def LoadXml(self, filename):
        ''' Load a list of errors from XML
        
        .. warning:: Describe XML format here'''
        q = open(filename, "r")
        dom = xml.dom.minidom.parse(q)
        dom.normalize()
        self.errors = []
        for node in dom.childNodes:
            if node.tagName == "errors":
                for error in node.childNodes:
                    # TODO: default values
                    currentError = {"time":0, "programmer":0, "severity":0, "item":0}
                    for attr in error.childNodes:
                        if attr.nodeName == "time":
                            for k in attr.childNodes:
                                currentError["time"] = int(k.nodeValue)
                        elif attr.nodeName == "programmer":
                            for k in attr.childNodes:
                                currentError["programmer"] = k.nodeValue
                        elif attr.nodeName == "severity":
                            for k in attr.childNodes:
                                currentError["severity"] = k.nodeValue
                        elif attr.nodeName == "item":
                            for k in attr.childNodes:
                                currentError["item"] = k.nodeValue   
                    if currentError != {}:
                        e = Error(time=currentError["time"], programmer=currentError["programmer"],
                                  severity=currentError["severity"], item=currentError["item"])
                        self.errors.append(e)                         
        q.close()
        self.CalculateErrorTimes()
        
    def AddDataXml(self, file):
        ''' Load a new XML and add the data from it to the current data'''
        errorsBack = copy.deepcopy(self.errors)
        self.LoadXml(file)
        self.errors += errorsBack
        self.CalculateErrorTimes()
        
    def DumpXml(self, filename):
        ''' Save current data to XML '''
        dom = xml.dom.minidom.Document()
        root = dom.createElement("errors")
        dom.appendChild(root)
        for s in self.errors:
            node = dom.createElement("error")
            time = dom.createElement("time")
            time.appendChild(dom.createTextNode(str(s["time"])))
            programmer = dom.createElement("programmer")
            programmer.appendChild(dom.createTextNode(str(s["programmer"])))
            severity = dom.createElement("severity")
            severity.appendChild(dom.createTextNode(str(s["severity"])))
            item = dom.createElement("item")
            item.appendChild(dom.createTextNode(str(s["item"])))
            node.appendChild(time)
            node.appendChild(programmer)
            node.appendChild(severity)
            node.appendChild(item)
            root.appendChild(node)
        f = open(filename, "w")
        dom.writexml(f)
        f.close()
        
    def AddError(self, t, p, s, i):
        ''' Add a single new error.
        
        :param t: Time
        :param p: Programmer
        :param s: Severity
        :param i: Item'''
        e = Error(t, p, s, i)
        self.errors.append(e)
        self.CalculateErrorTimes()
        
    def CalculateErrorTimes(self):
        ''' Auxiliary function used to calculate the list of errortimes for selected errors'''
        self.errortimes = []
        for e in self.errors:
            if self.programmer != [] and not e.programmer in self.programmer:
                pass
            elif self.severity != [] and not e.severity in self.severity:
                pass
            elif self.item != [] and not e.item in self.item:
                pass
            else:
                # TODO: think how to get rid of None here. Beware: lazy logical expression
                if self.startTime == None or self.endTime == None or (e.time < self.endTime and e.time > self.startTime): 
                    self.errortimes.append(e.time)
        self.errortimes.sort()
        
    def GetErrorTimes(self):
        ''':return: :attr:`~Core.TestingData.TestingData.errortimes`'''
        self.CalculateErrorTimes()
        return self.errortimes
    
    def ErrorsNumber(self):
        ''':return: total number of selected errors'''
        return len(self.errortimes)
    
    def StartTime(self):
        ''' :return: time of the first error'''
        # TODO: error if it's empty
        if self.errortimes != []:
            return self.errortimes[0]
        else:
            return 0
    
    def EndTime(self):
        ''' :return: time of the last error'''
        if self.errortimes != []:
            return self.errortimes[len(self.errortimes) - 1]
        else:
            return 0
    
    def TotalTime(self):
        ''' :return: total time between the first and the last error '''
        if self.errortimes != []:
            return self.errortimes[len(self.errortimes) - 1] - self.errortimes[0]
        else:
            return 0
    
    def SetProgrammerRestriction(self, p):
        ''' Sets the :attr:`~Core.TestingData.TestingData.programmer` list and computes errortimes again'''
        self.programmer = p
        self.CalculateErrorTimes()
        
    def SetSeverityRestriction(self, s):
        ''' Sets the :attr:`~Core.TestingData.TestingData.severity` list and computes errortimes again'''
        self.severity = s
        self.CalculateErrorTimes()
        
    def SetItemRestriction(self, i):
        ''' Sets the :attr:`~Core.TestingData.TestingData.item` list and computes errortimes again'''
        self.item = i
        self.CalculateErrorTimes()
        
    def SetTimeRestriction(self, st, end): 
        ''' Sets the start and end times and computes errortimes again'''       
        self.startTime = st
        self.endTime = end
        self.CalculateErrorTimes()