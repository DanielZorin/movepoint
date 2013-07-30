from Schedules.System import *
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge
from Core.Version import *
from Core.Processor import *
import math

class AntennaGenerator:
    a = 2.5
    B = 80
    K = 5
    L = 3
    n = 100
    steps = 1
    Mtheta = 2
    perf = 50
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

        # Calculate tdir
        s.tdir = int(self.a * self.B * self.n / self.perf)

        # Create processorsw

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
        x = self.L
        y = self.K
        if x < y:
            x, y = y, x
        while y != 0:
            x, y = y, x % y
        gcd = x
        fft = []
        for i in range(self.K):
            v = newVertex(int(self.a * self.L / gcd))
            v.name = "Norm_" + str(i + 1)
            v2 = newVertex(int(self.a * self.L / gcd * math.log(self.a * self.L, 2)))
            v2.name = "FFT_" + str(i + 1)
            v3 = newVertex(int(self.K * self.K / gcd))
            v3.name = "Mult_" + str(i + 1)
            e = ProgramEdge(v, v2, int(self.a * self.L))
            s.program.edges.append(e)
            e = ProgramEdge(v2, v3, 1)
            s.program.edges.append(e)
            fft.append(v3)

        # Create BCM
        last = []
        for i in range(self.L):
            v = newVertex(int(self.K ** 3 / gcd))
            v.name = "Eigenvalues_" + str(i + 1)
            for v0 in fft:
                e = ProgramEdge(v0, v, self.K ** 2)
                s.program.edges.append(e)
            for j in range(self.steps):
                v1 = newVertex(int(self.K / gcd))
                v1.name = "CME_" + str(i + 1) + "_stage_" + str(j + 2)
                e = ProgramEdge(v, v1, self.K ** 2)
                s.program.edges.append(e)
                v = v1
            prev = v
            lastpar = []
            for k in range(self.Mtheta):
                v1 = newVertex(int(self.K / gcd))
                v1.name = "CME_" + str(i + 1) + "_pstage_" + str(k)
                e = ProgramEdge(prev, v1, self.K)
                s.program.edges.append(e)
                v = v1
                for j in range(self.steps - 1):
                    v1 = newVertex(int(self.K / gcd))
                    v1.name = "CME_" + str(i + 1) + "_pstage_" + str(k) + "_" + str(j + 2)
                    e = ProgramEdge(v, v1, self.K)
                    s.program.edges.append(e)
                    v = v1
                lastpar.append(v)
            v = newVertex(int(self.K / gcd))
            v.name = "Comparison_" + str(i + 1)
            for v0 in lastpar:
                e = ProgramEdge(v0, v, 1)
                s.program.edges.append(e)
            last.append(v)
        v = newVertex(int(self.K * self.L / gcd))
        v.name = "CME_final"
        for v0 in last:
            e = ProgramEdge(v0, v, self.K)
            s.program.edges.append(e)
        last.append(v)           
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
                [self.tr("Frequency (Hz)"), self.parent.B],
                [self.tr("Kotelnikov coefficient"), self.parent.a],
                [self.tr("Array size"), self.parent.K],
                [self.tr("Number of frequency components"), self.parent.L],
                [self.tr("Number of support vectors"), self.parent.Mtheta],
                [self.tr("Sample size"), self.parent.n],
                [self.tr("Processor performance (GFLOPS)"), self.parent.perf],
                [self.tr("Processor reliability"), self.parent.rel],
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        self.B = dict[0][1]
        self.a = dict[1][1]
        self.K = dict[2][1]
        self.L = dict[3][1]
        self.Mtheta = dict[4][1]
        self.n = dict[5][1]
        self.perf = dict[6][1]
        self.rel = dict[7][1]

def pluginMain():
    return AntennaGenerator