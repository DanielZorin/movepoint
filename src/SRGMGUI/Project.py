'''
Created on 15.12.2010

@author: juan
'''
import pickle, xml.dom.minidom
from SRGM.SRGMList import SRGMList
from Core.TestingData import TestingData

class Project(object):
    
    name = None
    testingData = None
    
    def __init__(self, name="", data=""):
        self.name = name
        self.testingData = TestingData(data)
        
    def Serialize(self, filename):
        fn = open(filename, "wb")
        dict = {"name":self.name, "data":self.testingData}
        pickle.dump(dict, fn)
        fn.close()
    
    def Deserialize(self, filename):
        fn = open(filename, "rb")
        dict = pickle.load(fn)
        fn.close()
        self.name = dict["name"]
        self.testingData = dict["data"]
        
    def ReplaceData(self, file):
        self.testingData = TestingData(file)
        
    def AddData(self, file):
        self.testingData.AddDataXml(file)
        
    def ComputeModel(self, model):
        computer = SRGMList[model]()
        computer.SetData(self.testingData.GetErrorTimes())
        print(len(self.testingData.GetErrorTimes()))
        return computer.Compute()
    
    def GetTotalTime(self):
        return self.testingData.TotalTime()
    
    def GetErrorsNumber(self):
        return self.testingData.ErrorsNumber()