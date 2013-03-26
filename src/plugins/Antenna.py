from Schedules.System import *
from Schedules.ProgramVertex import ProgramVertex
from Schedules.ProgramEdge import ProgramEdge

class AntennaGenerator:
    K = 6
    L = 4
    n = 3
    Mtheta = 2
    FFT = 10
    BCM = 10

    def __init__(self):
        pass

    def GetName():
        return "Antenna"

    def GetType():
        return "generator"

    def Generate(self):
        s = System()
        # Create processors

        # Create FFT
        vCount = 1
        fft = []
        for i in range(self.K):
            v = ProgramVertex(vCount, self.FFT)
            v.name = "FFT_" + str(i + 1)
            vCount += 1
            s.program.vertices.append(v)
            fft.append(v)

        # Create BCM
        last = []
        for i in range(self.L):
            v = ProgramVertex(vCount, self.BCM)
            v.name = "BCM_" + str(i + 1) + "_stage_1"
            vCount += 1
            s.program.vertices.append(v)
            for v0 in fft:
                e = ProgramEdge(v0, v, 1)
                s.program.edges.append(e)
            for j in range(self.n - 1):
                v1 = ProgramVertex(vCount, self.BCM)
                v1.name = "BCM_" + str(i + 1) + "_stage_" + str(j + 2)
                vCount += 1
                s.program.vertices.append(v1)
                e = ProgramEdge(v, v1, 1)
                s.program.edges.append(e)
                v = v1
            prev = v
            lastpar = []
            for k in range(self.Mtheta):
                v1 = ProgramVertex(vCount, self.BCM)
                v1.name = "BCM_" + str(i + 1) + "_pstage_1_" + str(k)
                vCount += 1
                s.program.vertices.append(v1)
                e = ProgramEdge(prev, v1, 1)
                s.program.edges.append(e)
                v = v1
                for j in range(self.n - 2):
                    v1 = ProgramVertex(vCount, self.BCM)
                    v1.name = "BCM_" + str(i + 1) + "_pstage_" + str(j + 2) + "_" + str(k)
                    vCount += 1
                    s.program.vertices.append(v1)
                    e = ProgramEdge(v, v1, 1)
                    s.program.edges.append(e)
                    v = v1
                lastpar.append(v)
            v = ProgramVertex(vCount, self.BCM)
            v.name = "BCM_" + str(i + 1) + "_pstage_" + str(self.n) + "_" + str(k)
            vCount += 1
            s.program.vertices.append(v)
            for v0 in lastpar:
                e = ProgramEdge(v0, v, 1)
                s.program.edges.append(e)
            last.append(v)
        v = ProgramVertex(vCount, self.BCM)
        v.name = "BCM_final"
        vCount += 1
        s.program.vertices.append(v)
        for v0 in last:
            e = ProgramEdge(v0, v, 1)
            s.program.edges.append(e)
        last.append(v)           

        # Calculate tdir

        s.program._buildData()
        return s

    def GetSettings(self):
        # importing here to allow using the class without Qt
        from PyQt4.QtCore import QObject
        class Translator(QObject):
            def __init__(self, parent):
                QObject.__init__(self)
                self.parent = parent
            def getTranslatedSettings(self):
                return [
                [self.tr("Net size (K) "), self.parent.K],
                [self.tr("L"), self.parent.L],
                [self.tr("M-theta"), self.parent.Mtheta],
                [self.tr("FFT time"), self.parent.FFT],
                [self.tr("BCM time"), self.parent.BCM],
                [self.tr("BCM steps"), self.parent.n],
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        # importing here to allow using the class without Qt
        self.K = dict[0][1]
        self.L = dict[1][1]
        self.Mtheta = dict[2][1]
        self.FFT = dict[3][1]
        self.BCM = dict[4][1]
        self.n = dict[5][1]

def pluginMain():
    return AntennaGenerator