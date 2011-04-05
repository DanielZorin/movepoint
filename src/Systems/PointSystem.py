import random
import xml.dom.minidom
from Systems.Point import *

class PointSystem:
    """
    self.points - list of all points of the system.
    self.connections - list of pairs of points, representing the structure
        of the system graph.
    """
    def __init__(self):
        self.points = []
        self.connections = []
        
    def LoadFromXml(self, filename):
        #Clear the system before loading
        self.points = []
        self.connections = []
        #Parse the XML file
        f = file(filename)
        dom = xml.dom.minidom.parse(f)
        for node in dom.childNodes:
            if node.tagName == "system":
                for singlepoint in node.childNodes:
                    currentPoint = {"methods":[], 
                                    "hardware":[],
                                    "software":[]}
                    if singlepoint.nodeName == "point":
                        name = singlepoint.getAttribute("name")
                        type = singlepoint.getAttribute("type")
                        pall = singlepoint.getAttribute("pall")
                        pd = singlepoint.getAttribute("pd")
                        prv = singlepoint.getAttribute("prv")
                    for attr in singlepoint.childNodes:
                        if attr.nodeName == "method":
                            name = attr.getAttribute("name")
                            hard = int(attr.getAttribute("hardware"))
                            soft = int(attr.getAttribute("software"))
                            currentPoint["methods"].append({"name":name,
                                                            "hard":hard,
                                                            "soft":soft})
                        elif attr.nodeName == "hardware":
                            name = attr.getAttribute("name")
                            rel = float(attr.getAttribute("reliability"))
                            try:
                                var = float(attr.getAttribute("variance"))
                            except:
                                var = None
                            cost = int(attr.getAttribute("cost"))
                            currentPoint["hardware"].append({"name":name,
                                                             "reliability":rel,
                                                             "cost":cost,
                                                             "variance":var})
                        elif attr.nodeName == "software":
                            name = attr.getAttribute("name")
                            rel = float(attr.getAttribute("reliability"))
                            try:
                                var = float(attr.getAttribute("variance"))
                            except:
                                var = None
                            cost = int(attr.getAttribute("cost"))
                            currentPoint["software"].append({"name":name,
                                                             "reliability":rel,
                                                             "cost":cost,
                                                             "variance":var})
                    if currentPoint != {"methods":[], "hardware":[], "software":[]}:
                        p = Point(name)
                        for elem in currentPoint["software"]:
                            p.AddSoftware(elem["reliability"], 
                                          elem["variance"], 
                                          elem["cost"],
                                          elem["name"])
                        for elem in currentPoint["hardware"]:
                            p.AddHardware(elem["reliability"], 
                                          elem["variance"], 
                                          elem["cost"],
                                          elem["name"])
                        for elem in currentPoint["methods"]:
                            p.AddMethod(elem["name"], 
                                          elem["hard"], 
                                          elem["soft"])  
                        #FIXME: encapsulate this in Point instances
                        p.FixData()
                        p.pall = float(pall) 
                        p.pd = float(pd) 
                        p.prv = float(prv)                          
                        self.points.append(p)
        f.close()
        self._default()
        
    def SaveStateToXml(self, filename):
        if self.CheckConsistency() == False:
            #FIXME: exception here
            return
        dom = xml.dom.minidom.Document()
        resultsystem = dom.createElement("resultsystem")
        dom.appendChild(resultsystem)
        for p in self.points:
            point = dom.createElement("point")
            point.setAttribute("name", p.name)
            method = dom.createElement("method")
            method.setAttribute("name", p.methods[p.currentMethod].name)
            method.setAttribute("hardware", str(p.methods[p.currentMethod].hardware))
            method.setAttribute("software", str(p.methods[p.currentMethod].software))
            for i in p.currentHardware:
                hard = dom.createElement("hardware")
                hard.setAttribute("name", p.hardware[i].name)
                method.appendChild(hard)
            for i in p.currentSoftware:
                soft = dom.createElement("software")
                soft.setAttribute("name", p.software[i].name)
                method.appendChild(soft)
            point.appendChild(method)
            resultsystem.appendChild(point)
        f = file(filename, "w")
        f.write(dom.toprettyxml())
    
    def SaveToXml(self, filename):
        pass
        #TODO: implement
        
    def Encode(self):
        #Encodes system into a string, returns it and a string of maximum values. 
        encodedList = []
        maximumList = []
        for p in self.points:
            encodedList.append(p.Encode())
            maximumList.append(p.GetMaximumValues())
        return encodedList, maximumList
    
    def Decode(self, encodedList):
        #Load the system from a string
        for i in range(len(encodedList)):
            if self.points[i].Decode(encodedList[i]) == False:
                return False
        return True
    
    def TestSolution(self, solution):
        #Test if the given solution is encoded correctly.
        for i in range(len(solution)):
            if self.points[i].TestSolution(solution[i]) == False:
                return False
        return True
    
    # Function for debug purposes. Sets all points to some values 
    def _default(self):
        for i in range(len(self.points)):
            n = random.randrange(0, len(self.points[i].methods))
            h = self.points[i].methods[n].hardware
            s = self.points[i].methods[n].software
            self.points[i].currentMethod = n
            self.points[i].currentSoftware = list(range(s))
            self.points[i].currentHardware = list(range(h))
            
    #Generates a random valid solution for the given system
    def GenerateRandomSolution(self):
        v, max = self.Encode()
        i = 0
        while i < len(v):
            v[i]["software"] = random.randint(1,max[i]["software"])
            v[i]["hardware"] = random.randint(1,max[i]["hardware"])
            if self.points[i].TestSolution(v[i]):
                i += 1
        return v
    
    def CheckConsistency(self):
        for p in self.points:
            if p.CheckConsistency() == False:
                return False
    
    def GetReliability(self):
        if self.CheckConsistency() == False:
            raise "System not set. Try to decode it first."
        r = 1.0
        for p in self.points:
            r = r * p.GetReliability()
        return r
    
    def GetCost(self):
        if self.CheckConsistency() == False:
            raise "System not set. Try to decode it first."
        r = 0
        for p in self.points:
            r = r + p.GetCost()
        return r
        
    def __str__(self):
        s = "Points:\n"
        for p in self.points:
            s += str(p) + "\n"
        return s

