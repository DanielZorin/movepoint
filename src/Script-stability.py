from Tests.SimpleTest import *
from Systems.PointSystem import PointSystem
from Systems.SystemGenerator import SystemGenerator
import Methods.ParetoOptimization.RandomSelection
import Methods.ParetoOptimization.FullIteration
import Methods.ParetoOptimization.NSGA
import Methods.ParetoOptimization.NPGA
import Methods.ParetoOptimization.SPEA
import Methods.ParetoOptimization.SPEA2
import Methods.ParetoOptimization.PAES
import Methods.ParetoOptimization.VEGA
import Methods.ParetoOptimization.PESA
import pickle

ss = SystemGenerator(2,3,3)
p = ss.Generate()
a,b = Methods.ParetoOptimization.FullIteration.GenerateParetoFrontOptimized(p)

f = open("log-RandomSelection.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.RandomSelection.RandomSelection, p, f, a)
c.Start()

f = open("log-SPEA.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.SPEA.SPEA_wrapper, p, f, a)
c.Start()

f = open("log-PAES.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.PAES.PAES, p, f, a)
c.Start()

f = open("log-PESA.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.PESA.PESA, p, f, a)
c.Start()

f = open("log-SPEA2.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.SPEA2.SPEA2_wrapper, p, f, a)
c.Start()

f = open("log-VEGA.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.VEGA.VEGA_wrapper, p, f, a)
c.Start()

f = open("log-NPGA.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.NPGA.NPGA_wrapper, p, f, a)
c.Start()

f = open("log-NSGA.txt", "w")
c = SimpleTest(Methods.ParetoOptimization.NSGA.NSGA_wrapper, p, f, a)
c.Start()