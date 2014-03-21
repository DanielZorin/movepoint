from Schedules.System import *
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Schedules.Schedule import *
from Core.Version import *
from Core.Processor import *
import random

class IdealProgramGenerator:
    vertices = 20
    processors = 2
    edges = 0.75
    k = 1.3

    def __init__(self):
        pass

    def GetName():
        return "Ideal Program"

    def GetType():
        return "generator"

    def Generate(self, s):
        s.program.vertices = []
        s.program.edges = []
        ideal = Schedule(s.program, s.processors)
        ideal.vertices = {}
        ideal.processors = []

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
            for j in range(count[i] - 1):
                lst.append(random.randint(2, 10))
            lst.append(tdir - sum(lst) - random.randint(0, 3))
            if lst[-1] < 0:
                while lst[-1] < 2:
                    r = random.randint(0, len(lst) - 2)
                    if lst[r] > 1:
                        lst[r] -= 1
                        lst[-1] += 1
            #print (i, lst)
            summ = 0
            proc = ideal._getProcessor()
            ideal.vertices[proc.number] = []
            for j in lst:
                v = ProgramVertex(total, j)
                ver = Version(v, 1, 1.0)
                v.versions.append(ver)
                s.program.vertices.append(v)
                total += 1
                verts.append((v, i, summ, summ + v.time))
                summ += v.time
                ideal.vertices[proc.number].append(ScheduleVertex(v, ver, proc))

        edges = int(self.vertices * self.edges)
        total = 0
        for i in range(1, self.processors):
            proc = ideal.vertices[i]
            if len(proc) > 1:
                for start in range(len(proc) - 1):
                    v1 = proc[start].v
                    v2 = proc[start + 1].v
                    vol = random.randint(1, 10)
                    e = ProgramEdge(v1, v2, vol)
                    if s.program.FindEdge(v1, v2) == None:
                        s.program.edges.append(e)
                        #print(v1.number, v2.number)
                        total += 1
                        if total == edges:
                            break
        iter = 0
        while total < edges:
            print (total)
            iter += 1
            if iter == 10000:
                break
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
        s.tdir = tdir * self.k
        s.rdir = 0.0
        return ideal

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
                [self.tr("Processors"), self.parent.processors],
                [self.tr("Edges/vertices rate"), self.parent.edges]
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        # importing here to allow using the class without Qt
        self.vertices = dict[0][1]
        self.processors = dict[1][1]
        self.edges = dict[2][1]

def pluginMain():
    return IdealProgramGenerator