from Core.Common import * 
from Core.Hardware import Hardware
from Core.Software import Software
#TODO: rename Method everywhere
from Core.RedundancyTechnique import RedundancyTechnique as Method
from Core.ReliabilityFunctions import reliabilityFunctions    

class Point:
    def __init__(self, name):
        #Point name
        self.name = name
        #List of hardware. Elements are instances of Hardware class.
        self.hardware = []
        #List of software. Elements are instances of Software class.
        self.software = []
        #List of methods. Elements are instances of Method class.
        self.methods = []
        #List of indexes of the elements of self.hardware currently used.
        self.currentHardware = None
        #List of indexes of the elements of self.software currently used.
        self.currentSoftware = None
        #Index of currently used method in self.methods
        self.currentMethod = None
        #Maximum number of variants for each method.
        self._methodMask = []

        self.pall = 1.0
        self.pd = 1.0
        self.prv = 1.0
        
    def AddHardware(self, rel, var, cost, name):
        self.hardware.append(Hardware(rel, var, cost, name))
        self.FixData()
    def AddSoftware(self, rel, var, cost, name):
        self.software.append(Software(rel, var, cost, name))
        self.FixData()
    def AddMethod(self, name, hard, soft):
        self.methods.append(Method(name, hard, soft))
        self.FixData()
        
    def FixData(self):
        for m in self.methods:
            h = len(self.hardware)
            s = len(self.software)
            val = 0
            res = {}
            if m.hardware >= h:
                val = 1
            else:
                val = factorial(h) / (factorial(m.hardware) * factorial(h-m.hardware))
            res["hardware"] = int(val)
            if m.software >= s:
                val = 1
            else:
                val = factorial(s) / (factorial(m.software) * factorial(s-m.software))
            res["software"] = int(val)
            self._methodMask.append(res)
        
    def CheckIfSet(self):
        if (self.currentMethod == None) or (self.currentHardware == None) or (self.currentSoftware == None):
            return False
        else: 
            return True
    
    def CheckConsistency(self):
        if self.CheckIfSet() == False:
            return False
        if len(self.currentHardware) != self.methods[self.currentMethod].hardware:
            return False
        if len(self.currentSoftware) != self.methods[self.currentMethod].software:
            return False
        return True
        
    def GetReliability(self):
        self.reliabilityCalculator = reliabilityFunctions(self.pall, self.pd, self.prv)       
        currentHardwareList = []
        currentSoftwareList = []
        for i in self.currentHardware:
            currentHardwareList.append(self.hardware[i])
        for i in self.currentSoftware:
            currentSoftwareList.append(self.software[i])
        return self.reliabilityCalculator.Calculate(
                                                    self.methods[self.currentMethod],
                                                    currentHardwareList, 
                                                    currentSoftwareList)
    def GetCost(self):
        res = 0
        for i in self.currentHardware:
            res += self.hardware[i].cost
        for i in self.currentSoftware:
            res += self.software[i].cost
        return res        
        
    def Encode(self):
        res = {"software": 0, "hardware": 0}
        if (self.currentMethod == None) or (self.currentHardware == None) or (self.currentSoftware == None):
            return res
        #If everything is set, calculate the numbers for current hard and soft
        for i in range(self.currentMethod):
            res["software"] += self._methodMask[i]["software"]
            res["hardware"] += self._methodMask[i]["hardware"]
        s = list(range(len(self.software)))
        h = list(range(len(self.hardware)))
        for i in range(len(self.software)):
            s[i] = 0
        for i in range(len(self.hardware)):
            h[i] = 0
        for i in self.currentHardware:
            h[i] = 1
        for i in self.currentSoftware:
            s[i] = 1
        res["software"] += combinationNumber(s, self.methods[self.currentMethod].software)
        res["hardware"] += combinationNumber(h, self.methods[self.currentMethod].hardware)
        return res
        
    def GetMaximumValues(self):
        h = 0
        s = 0
        for k in self._methodMask:
            h += k["hardware"]
            s += k["software"]
        return {"software": s, "hardware": h}
    
    def Decode(self, v):
        #Decodes a point. Returns false if the values are invalid.
        value = {}
        value["hardware"] = v["hardware"]
        value["software"] = v["software"]
        tmp = {"software": 0, "hardware": 0}
        for i in range(len(self._methodMask)):
            if value["software"] <= self._methodMask[i]["software"]:
                self.currentMethod = i
                break
            value["software"] -= self._methodMask[i]["software"]
            value["hardware"] -= self._methodMask[i]["hardware"]
        if (value["hardware"] <= 0) or (value["hardware"] > self._methodMask[self.currentMethod]["hardware"]):
            return False
        try:
            self.currentSoftware = getCombinationByNumber(len(self.software), 
                                         self.methods[self.currentMethod].software, 
                                         value["software"])
            self.currentHardware = getCombinationByNumber(len(self.hardware), 
                                         self.methods[self.currentMethod].hardware, 
                                         value["hardware"])
        except:
            raise "LOGIC ERROR"
        return True
    
    def TestSolution(self, v):
        value = {}
        value["hardware"] = v["hardware"]
        value["software"] = v["software"]
        tmp = {"software": 0, "hardware": 0}
        for i in range(len(self._methodMask)):
            if value["software"] <= self._methodMask[i]["software"]:
                break
            value["software"] -= self._methodMask[i]["software"]
            value["hardware"] -= self._methodMask[i]["hardware"]
        if (value["hardware"] <= 0) or (value["hardware"] > self._methodMask[i]["hardware"]):
            return False
        else:
            return True
    
    def __str__(self):
        hardlist = []
        softlist = []
        methodlist = []
        for s in self.hardware:
            hardlist.append(str(s))
        for s in self.software:
            softlist.append(str(s))
        for s in self.methods:
            methodlist.append(str(s))
        s = "Name: " + self.name + "\n"
        s += "Hardware: " + str(hardlist) + "\n"
        s += "Software: " + str(softlist) + "\n"
        s += "Methods: " + str(methodlist) + "\n"
        s += "Current method: " + str(self.currentMethod) + "\n"
        s += "Current Hardware: " + str(self.currentHardware) + "\n"
        s += "Current Software: " + str(self.currentSoftware) + "\n"
        return s