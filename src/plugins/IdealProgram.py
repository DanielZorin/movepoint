from Schedules.System import *
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import *
from Core.Processor import *
import random

class IdealProgramGenerator:
    vertices = 20
    processors = 4

    def __init__(self):
        pass

    def GetName():
        return "Ideal Program"

    def GetType():
        return "generator"

    def Generate(self, s):
        s.program.vertices = []
        s.program.edges = []

        tdir = int(self.vertices * 5 / self.processors)
        avg = int(self.vertices / self.processors)
        count = []
        for i in range(self.processors):
            count.append(max(0, random.randint(avg - 2, avg + 2)))
        count[-1] = count[-1] + (self.vertices - sum(count))
        if count[-1] < 0:
            while count[-1] < avg:
                r = random.randint(0, len(count) - 2)
                if count[r] > 1:
                    count[r] -= 1
                    count[-1] += 1
        total = 1
        verts = []
        for i in range(self.processors):
            lst = []
            for j in range(count[i]):
                lst.append(random.randint(1, 10))
            lst.append(tdir - sum(lst) - random.randint(0, 3))
            if lst[-1] < 0:
                while lst[-1] < 2:
                    r = random.randint(0, len(lst) - 2)
                    if lst[r] > 1:
                        lst[r] -= 1
                        lst[-1] += 1
            print (i, lst)
            summ = 0
            for j in lst:
                v = ProgramVertex(total, j)
                s.program.vertices.append(v)
                total += 1
                verts.append((v, i, summ, summ + v.time))
                summ += v.time

        for v in s.program.vertices:
            ver = Version(v, 1, 1.0)
            v.versions.append(ver)
        edges = self.vertices
        total = 0
        while total < edges:
            i = random.randint(0, len(verts) - 1)
            j = random.randint(0, self.processors - 1)
            if j == verts[i][1]:
                j = 0
            for v in verts:
                if j == v[1]:
                    if v[2] > verts[i][3]:
                        vol = random.randint(1, v[2] - verts[i][3])
                        src = verts[i][0]
                        dest = v[0]
                        e = ProgramEdge(src, dest, vol)
                        if s.program.FindEdge(src, dest) == None:
                            s.program.edges.append(e)
                            total += 1
        s.program._buildData()
        s.tdir = tdir
        s.rdir = 0.0
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
                [self.tr("Vertices"), self.parent.vertices],
                [self.tr("Processors"), self.parent.processors]
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        # importing here to allow using the class without Qt
        self.vertices = dict[0][1]
        self.processors = dict[1][1]

def pluginMain():
    return IdealProgramGenerator