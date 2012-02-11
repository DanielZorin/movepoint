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
    ''' Represents a program that consists of several tasks depending on each other
        Basically, it's a direct acyclic graph.
        
    :param filename: name of the XML file with the specification
    '''
    
    vertices = []
    ''' List of tasks, i.e. :class:`vertices  <Schedules.ProgramVertex.ProgramVertex>` of the graph '''
    
    edges = []
    ''' List of dependencies, i.e. :class:`edges  <Schedules.ProgramEdge.ProgramEdge>` of the graph'''
    
    _dep = {}
    _trans = {}

    def __init__(self, filename=""):
        self.vertices = []
        self.edges = []
        if filename != "":
            self.LoadFromXML(filename)
            
    def LoadFromXML(self, filename):
        ''' Load edges and vertices from XML
        
        .. warning:: Describe XML format here'''
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
            self._buildData()
            
        except IOError:
            raise SchedulerFileException(filename)
        except(ValueError):
            f.close()
            raise SchedulerXmlException(filename)

    def Export(self, dom, root):
        ''' Exports program to XML by appending children to the root XML element of dom Document'''

        for v in self.vertices:
            vertex = dom.createElement("vertex")
            vertex.setAttribute("name", v.name)
            vertex.setAttribute("number", str(v.number))
            vertex.setAttribute("complexity", str(v.time))
            for ver in v.versions:
                vers = dom.createElement("version")
                vers.setAttribute("reliability", str(ver.reliability))
                vertex.appendChild(vers)
            root.appendChild(vertex)
        for e in self.edges:
            edge = dom.createElement("edge")
            edge.setAttribute("name", e.name)
            edge.setAttribute("source", str(e.source.number))
            edge.setAttribute("destination", str(e.destination.number))
            edge.setAttribute("volume", str(e.volume))
            root.appendChild(edge)
    
    def CheckCycles(self):
        ''' Finds all cycles in the graph '''
        cycles = []
        for v in self.vertices:
            if v in self._trans[v.number]:
                cycles.append(v)
        return cycles
    
    def GetNumber(self):
        nums = [i for i in range(1, len(self.vertices) + 2)]
        for v in self.vertices:
            nums.remove(v.number)
        return nums[0]

    def AddVertex(self, v):
        self.vertices.append(v)
        self._buildData()

    def AddEdge(self, e):
        self.edges.append(e)
        self._buildData()

    def DeleteVertex(self, v):
        ind = self.vertices.index(v)
        new_edges = []
        for e in self.edges:
            if e.source != v and e.destination != v:
                new_edges.append(e)
            else:
                del e
        self.edges = new_edges
        del self.vertices[ind]
        self._buildData()

    def DeleteEdge(self, ed):
        new_edges = []
        for e in self.edges:
            if e != ed:
                new_edges.append(e)
            else:
                del e
        self.edges = new_edges
        self._buildData()

    def _buildData(self):
        for v in self.vertices:
            res = []
            for e in self.FindAllEdges(v2=v):
                res.append(e.source)
            self._dep[v.number] = res 
            
        for v in self.vertices:
            cur = []
            for v2 in self.vertices:
                if self.FindEdge(v, v2):
                    if not(v2 in cur):
                        cur.append(v2)
            new = []
            while True:
                for v1 in cur:
                    if not(v1 in new):
                        new.append(v1)
                    for v2 in self.vertices:
                        if self.FindEdge(v1, v2):
                            if not(v2 in new):
                                new.append(v2)
                if new == cur:
                    self._trans[v.number] = cur
                    break
                else:
                    cur = []
                    for v0 in new:
                        cur.append(v0)
                    new = []      
    
    def FindEdge(self, v1, v2):
        '''Search for a specific edge from v1 to v2. Returns None if the edge doesn't exist'''
        for ver in self.edges:
            if (ver.source == v1):
                if (ver.destination == v2):
                    return ver
        return None
    
    def FindAllEdges(self, v1 = None, v2 = None):
        '''Search for all edges where source is v1 and destination is v2. 
        If v1 or v2 is None, it doesn't set any restrictions.
        I.e. FindAllEdges(None, None) returns a list of all edges of the graph'''
        res = []
        for ver in self.edges:
            if (v1 is None) or (ver.source == v1):
                if (v2 is None) or (ver.destination == v2):
                    res.append(ver)
        return res
    
    def FindMaxChain(self, countedges):
        '''Finds the longest (in terms of time) chain in the graph.
        
        Each vertex has an integer attribute "time" assigned to it. This function finds the chain
        of edges where the sum of times is maximal. It's not necessary the chain that has the most vertices
        
        If countedges is True, then the volume of the edges between the vertices is counted as well.
        It makes sense when the time of delivery between processors is constant, hence volume of data
        is proportional to the time'''
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
        '''Finds the maximal realiability achievable for this program (when all versions
        of all tasks are used)'''
        strict = 1.0
        normal = 1.0
        for v in self.vertices:
            normal *= v.versions[0].reliability
            nvp = NVP(v.versions, [], 1.0, 1.0, 1.0)
            p = nvp.GetReliability()
            strict *= p
            
        return strict, normal
    
    def GenerateRandom(self, params):
        '''Generates a random graph with n vertices.
        Each task has from 1 to 5 versions.
        Times are random integers from t1 to t2.
        Volumes are random integers from v1 to v2.
        All parameters are passed in a dictionary.'''
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
            for j in [0]:#range(random.randint(0, 1)):
                src = self.vertices[i]
                dest = self.vertices[random.randint(i+1, params["n"]-1)]
                volume = random.randint(params["v1"], params["v2"])
                e = ProgramEdge(src, dest, volume)
                if self.FindEdge(src, dest) == None:
                    self.edges.append(e)
                    
        self._buildData()
    
    def __str__(self):
        res = ""
        for v in self.vertices:
            res += str(v)
        for e in self.edges:
            res += str(e)
        return res  
