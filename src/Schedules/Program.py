'''
Created on 03.11.2010

@author: juan
'''
import xml.dom.minidom
import random
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import Version
from Core.NVP import NVP
from Schedules.Exceptions import SchedulerFileException, SchedulerXmlException

class Program(object):

    vertices = []
    edges = []
    versions = []

    def __init__(self, filename=""):
        self.vertices = []
        self.edges = []
        if filename != "":
            self.LoadFromXML(filename)
            
    def LoadFromXML(self, filename):
        # Load edges and vertices from XML
        try:
            f = open(filename, "r")
            dom = xml.dom.minidom.parse(f)
        
            for node in dom.childNodes:
                if node.tagName == "program":
                    #Parse vertices
                    for vertex in node.childNodes:
                        if vertex.nodeName == "vertex":
                            number = int(vertex.getAttribute("number"))
                            complexity = int(vertex.getAttribute("complexity"))
                            v = ProgramVertex(number, complexity)
                            self.vertices.append(v)
                            vercount = 1
                            for version in vertex.childNodes:
                                if version.nodeName == "version":
                                    rel = float(version.getAttribute("reliability"))
                                    ver = Version(v, vercount, rel)
                                    v.versions.append(ver)
                                    vercount += 1
                            v.versions.sort(key=lambda x: x.reliability)
                    self.vertices.sort(key=lambda x: x.number)
                    
                    #Parse edges
                    for edge in node.childNodes:
                        if edge.nodeName == "edge":
                            source = int(edge.getAttribute("source"))
                            destination = int(edge.getAttribute("destination"))
                            volume = int(edge.getAttribute("volume"))
                            e = ProgramEdge(self.vertices[source-1], self.vertices[destination-1], volume)
                            self.edges.append(e)
            f.close()
            
        except IOError:
            raise SchedulerFileException(filename)
        except(xml.parsers.expat.ExpatError, ValueError):
            f.close()
            raise SchedulerXmlException(filename)
    
    def CheckCycles(self):
        # Checks that there are no cycles in the graph
        pass
    
    def FindEdge(self, v1, v2):
        for ver in self.edges:
            if (ver.source == v1):
                if (ver.destination == v2):
                    return ver
        return None
    
    def FindAllEdges(self, v1 = None, v2 = None):
        res = []
        for ver in self.edges:
            if (v1 is None) or (ver.source == v1):
                if (v2 is None) or (ver.destination == v2):
                    res.append(ver)
        return res
    
    def FindMaxChain(self, countedges):
        def Walk(v, cur, countedges):
            lst = self.FindAllEdges(v1=v)
            m = cur + v.time
            for e in lst:
                if not countedges:
                    tmp = Walk(e.destination, cur + v.time, countedges)
                else:
                    tmp = Walk(e.destination, cur + e.volume + v.time, countedges)
                if tmp > m:
                    m = tmp
            return m
              
        m = 0
        for v in self.vertices:
            tmp = Walk(v, 0, countedges)
            if tmp > m:
                m = tmp
        return m
    
    def GetReliabilityBoundaries(self):
        strict = 1.0
        normal = 1.0
        for v in self.vertices:
            normal *= v.versions[0].reliability
            nvp = NVP(v.versions, [], 1.0, 1.0, 1.0)
            p = nvp.GetReliability()
            strict *= p
            
        return strict, normal
    
    # Generates a random graph with n vertices
    # Each task has from 1 to 5 versions
    # Times are random integers from t1 to t2
    # Volumes are random integers from v1 to v2
    def GenerateRandom(self, params):
        for i in range(params["n"]):
            v = ProgramVertex(i + 1, random.randint(params["t1"], params["t2"]))
            self.vertices.append(v)
            for j in range(random.randint(1,5)):
                ver = Version(v, j + 1, (50.0 + random.random()) / 51.0)
                v.versions.append(ver)
            v.versions.sort(key=lambda x: x.reliability)
            for j in range(len(v.versions)):
                v.versions[j].number = j + 1
        for i in range(params["n"]-1):
            for j in range(random.randint(0, 1)):
                src = self.vertices[i]
                dest = self.vertices[random.randint(i+1, params["n"]-1)]
                volume = random.randint(params["v1"], params["v2"])
                e = ProgramEdge(src, dest, volume)
                if self.FindEdge(src, dest) == None:
                    self.edges.append(e)
    
    def __str__(self):
        res = ""
        for v in self.vertices:
            res += str(v)
        for e in self.edges:
            res += str(e)
        return res    