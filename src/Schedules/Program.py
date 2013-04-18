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
    _next = {}

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
        # TODO: simplify
        self._buildData()

    def AddEdge(self, e):
        self.edges.append(e)
        #TODO: simplify
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
        self._dep = {}
        self._trans= {}
        for v in self.vertices:
            res = []
            for e in self.FindAllEdges(v2=v):
                res.append(e.source)
            self._dep[v.number] = res 

            self._next[v.number] = self.FindAllEdges(v1=v)
        
        levels = {}
        leftverts = list(self.vertices)
        verts = []
        limit = len(self.vertices)
        lev = 1
        while len(leftverts) != 0:
            curlev = []
            newlv = []
            for v in leftverts:
                dep = self._dep[v.number]
                cur = True
                for v0 in dep:
                    if (v0 in leftverts):
                        cur = False
                if cur:
                    curlev.append(v)
                    verts.append(v)
                else:
                    newlv.append(v)
            leftverts = newlv
            levels[lev] = curlev
            lev += 1
        lev -= 1            
        while lev > 0:
            for v in levels[lev]:
                edges = self.FindAllEdges(v1=v)
                trans = []
                for e in edges:
                    trans += self._trans[e.destination.number]
                    trans.append(e.destination)
                self._trans[v.number] = sorted(list(set(trans)), key=lambda x: x.number)
            lev -= 1
          
    def OrderedVertices(self):
        res = []
        for v in self.vertices:
            if len(self._dep[v.number]) == 0:
                res.append(v)
        while len(res) != len(self.vertices):
            for v in self.vertices:
                if not v in res:
                    edges = self.FindAllEdges(v2=v)
                    add = True
                    for e in edges:
                        if not e.source in res:
                            add = False
                    if add:
                        res.append(v)
        return res
    
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
    
    def __str__(self):
        res = ""
        for v in self.vertices:
            res += str(v)
        for e in self.edges:
            res += str(e)
        return res  
