from Schedules.System import *
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import *
from Core.Processor import *

class AntennaGenerator:
    a = 2.5
    B = 100
    K = 2
    L = 2
    n = 10
    steps = 2
    Mtheta = 2
    FFT = 10
    BCM = 10
    perf = 100
    bandwidth = 1
    rel = 0.9

    def __init__(self):
        pass

    def GetName():
        return "Antenna"

    def GetType():
        return "generator"

    def Generate(self, s):
        s.program.vertices = []
        s.program.edges = []
        # Create processors

        # Create FFT
        self.vCount = 1

        #TODO: turn to generator function
        def newVertex(time):
            newv = ProgramVertex(self.vCount, time)
            ver = Version(newv, 1, 1.0)
            newv.versions.append(ver)
            self.vCount += 1
            s.program.vertices.append(newv)
            return newv

        fft = []
        for i in range(self.K):
            v = newVertex(self.FFT)
            v.name = "FFT_" + str(i + 1)
            fft.append(v)

        # Create BCM
        last = []
        for i in range(self.L):
            v = newVertex(self.BCM)
            v.name = "BCM_" + str(i + 1) + "_stage_1"
            for v0 in fft:
                e = ProgramEdge(v0, v, 1)
                s.program.edges.append(e)
            for j in range(self.steps - 1):
                v1 = newVertex(self.BCM)
                v1.name = "BCM_" + str(i + 1) + "_stage_" + str(j + 2)
                e = ProgramEdge(v, v1, 1)
                s.program.edges.append(e)
                v = v1
            prev = v
            lastpar = []
            for k in range(self.Mtheta):
                v1 = newVertex(self.BCM)
                v1.name = "BCM_" + str(i + 1) + "_pstage_1_" + str(k)
                e = ProgramEdge(prev, v1, 1)
                s.program.edges.append(e)
                v = v1
                for j in range(self.steps - 2):
                    v1 = newVertex(self.BCM)
                    v1.name = "BCM_" + str(i + 1) + "_pstage_" + str(j + 2) + "_" + str(k)
                    e = ProgramEdge(v, v1, 1)
                    s.program.edges.append(e)
                    v = v1
                lastpar.append(v)
            v = newVertex(self.BCM)
            v.name = "BCM_" + str(i + 1) + "_pstage_" + str(self.steps) + "_" + str(k)
            for v0 in lastpar:
                e = ProgramEdge(v0, v, 1)
                s.program.edges.append(e)
            last.append(v)
        v = newVertex(self.BCM)
        v.name = "BCM_final"
        for v0 in last:
            e = ProgramEdge(v0, v, 1)
            s.program.edges.append(e)
        last.append(v)           

        # Calculate tdir
        s.tdir = self.a * self.B * self.n
        s.program._buildData()

    def GetSettings(self):
        # importing here to allow using the class without Qt
        from PyQt4.QtCore import QObject
        class Translator(QObject):
            def __init__(self, parent):
                QObject.__init__(self)
                self.parent = parent
            def getTranslatedSettings(self):
                return [
                [self.tr("Frequency (B)"), self.parent.B],
                [self.tr("Kotelnikov coefficient (a)"), self.parent.a],
                [self.tr("Array size (K) "), self.parent.K],
                [self.tr("L"), self.parent.L],
                [self.tr("M-theta"), self.parent.Mtheta],
                [self.tr("BCM steps"), self.parent.steps],
                [self.tr("Sample size (n)"), self.parent.n],
                [self.tr("Performance"), self.parent.perf],
                [self.tr("Bandwidth"), self.parent.bandwidth],
                [self.tr("Reliability"), self.parent.rel],
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        self.B = dict[0][1]
        self.a = dict[1][1]
        self.K = dict[2][1]
        self.L = dict[3][1]
        self.Mtheta = dict[4][1]
        self.steps = dict[5][1]
        self.n = dict[6][1]
        self.perf = dict[7][1]
        self.bandwidth = dict[8][1]
        self.rel = dict[9][1]

def pluginMain():
    return AntennaGenerator