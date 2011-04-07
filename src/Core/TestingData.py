'''
Created on 07.04.2011

@author: juan
'''

import xml.dom.minidom, copy
from Core.Error import Error

class TestingData(object):
    '''
    classdocs
    '''
    
    errors = []
    
    errortimes = []

    def __init__(self, file=""):
        if file == "":
            self.errors = []
            self.errortimes = []
        else:
            self.LoadXml(file)
    
    def LoadXml(self, filename):
        q = open(filename, "r")
        dom = xml.dom.minidom.parse(q)
        dom.normalize()
        self.errors = []
        for node in dom.childNodes:
            if node.tagName == "errors":
                for error in node.childNodes:
                    currentError = {}
                    for attr in error.childNodes:
                        if attr.nodeName == "time":
                            for k in attr.childNodes:
                                currentError["time"] = int(k.nodeValue)
                        elif attr.nodeName == "programmer":
                            for k in attr.childNodes:
                                currentError["programmer"] = int(k.nodeValue)
                        elif attr.nodeName == "severity":
                            for k in attr.childNodes:
                                currentError["severity"] = int(k.nodeValue)
                        elif attr.nodeName == "item":
                            for k in attr.childNodes:
                                currentError["item"] = int(k.nodeValue)   
                    if currentError != {}:
                        e = Error(time=currentError["time"], programmer=currentError["programmer"],
                                  severity=currentError["severity"], item=currentError["item"])
                        self.errors.append(e)                         
        q.close()
        self.CalculateErrorTimes()
        
    def AddDataXml(self, file):
        errorsBack = copy.deepcopy(self.errors)
        self.LoadXml(file)
        self.errors += errorsBack
        self.CalculateErrorTimes()
        
    def DumpXml(self, filename):
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
        
    def CalculateErrorTimes(self):
        self.errortimes = []
        for e in self.errors:
            self.errortimes.append(e.time)
        self.errortimes.sort()
        
    def GetErrorTimes(self):
        self.CalculateErrorTimes()
        return self.errortimes
    
    def ErrorsNumber(self):
        return len(self.errortimes)
    
    def TotalTime(self):
        return self.errortimes[len(self.errortimes)-1]