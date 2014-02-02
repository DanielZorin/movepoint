from Schedules.System import *
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import *
from Core.Processor import *
import random

class RandomProgramGenerator:
    n = 10
    t1 = 2
    t2 = 5
    v1 = 2
    v2 = 5
    q = 0.7
    tdir = [["Unreal", "Very strict", "Normal", "None"], 2]
    rdir = [["Unreal", "Very strict", "Normal", "None"], 2]

    def __init__(self):
        pass

    def GetName():
        return "Random"

    def GetType():
        return "generator"

    def Generate(self, s):
        ''' Generates a random system.
        Now that the processors are fixed it merely creates a random program
        The params dictionary is passed to the :meth:`~Schedules.Program.Program.GenerateRandom` function.
        
        Time and reliability constraints are generated here. Types of constraints (params["tdir"]/params["rdir"]):
        
        * 0 = Impossible
        * 1 = Strict
        * 2 = Normal
        * 3 = Nonexisting
        
        Numbers are used because strings in GUI can be translated'''
        s.program.vertices = []
        s.program.edges = []
        
        for i in range(self.n):
            v = ProgramVertex(i + 1, random.randint(self.t1, self.t2))
            s.program.vertices.append(v)
            for j in range(random.randint(1,5)):
                ver = Version(v, j + 1, (50.0 + random.random()) / 51.0)
                v.versions.append(ver)
            v.versions.sort(key=lambda x: x.reliability)
            for j in range(len(v.versions)):
                v.versions[j].number = j + 1
        for i in range(int((self.n-1) * self.q)):
            num = int(i / self.q)
            src = s.program.vertices[num]
            dest = s.program.vertices[random.randint(num+1, self.n-1)]
            volume = random.randint(self.v1, self.v2)
            e = ProgramEdge(src, dest, volume)
            if s.program.FindEdge(src, dest) == None:
                s.program.edges.append(e)
                    
        s.program._buildData()

        maxchain = s.program.FindMaxChain(True) 
        ss = sum([v.time for v in s.program.vertices])     
        s.tdir = {
                     0: 0,
                     1: maxchain,
                     2: int(maxchain + (ss - maxchain) / 3),
                     # TODO: replace this workaround
                     3: int(maxchain * 1000)
                     }[self.tdir[1]]
                     
        relstrict, relnormal = s.program.GetReliabilityBoundaries()
        # TODO: this only works now that we have only one processor
        procrel = s.processors[0].reliability ** self.n
        relstrict *= procrel
        relnormal *= procrel
        s.rdir = {
                     0: 1.0,
                     1: relstrict,
                     2: relnormal,
                     3: 0.0
                     }[self.rdir[1]]
        return None

    def GetSettings(self):
        # importing here to allow using the class without Qt
        from PyQt4.QtCore import QObject
        class Translator(QObject):
            def __init__(self, parent):
                QObject.__init__(self)
                self.parent = parent
            def getTranslatedSettings(self):
                return [
                [self.tr("Number of vertices"), self.parent.n],
                [self.tr("t1"), self.parent.t1],
                [self.tr("t2"), self.parent.t2],
                [self.tr("v1"), self.parent.v1],
                [self.tr("v2"), self.parent.v2],
                [self.tr("tdir"), self.parent.tdir],
                [self.tr("rdir"), self.parent.rdir]
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        # importing here to allow using the class without Qt
        self.n = dict[0][1]
        self.t1 = dict[1][1]
        self.t2 = dict[2][1]
        self.v1 = dict[3][1]
        self.v2 = dict[4][1]
        self.tdir = dict[5][1]
        self.rdir = dict[6][1]

def pluginMain():
    return RandomProgramGenerator