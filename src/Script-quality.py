from Tests.QualityTest import *
from Systems.PointSystem import PointSystem
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

f = open("log-RandomSelection.txt", "w")
c = QualityTest([Methods.ParetoOptimization.RandomSelection.RandomSelection],f)
c.Start()

f = open("log-SPEA.txt", "w")
c = QualityTest([Methods.ParetoOptimization.SPEA.SPEA_wrapper], f)
c.Start()

f = open("log-PAES.txt", "w")
c = QualityTest([Methods.ParetoOptimization.PAES.PAES], f)
c.Start()

f = open("log-PESA.txt", "w")
c = QualityTest([Methods.ParetoOptimization.PESA.PESA], f)
c.Start()

f = open("log-SPEA2.txt", "w")
c = QualityTest([Methods.ParetoOptimization.SPEA2.SPEA2_wrapper], f)
c.Start()

f = open("log-VEGA.txt", "w")
c = QualityTest([Methods.ParetoOptimization.VEGA.VEGA_wrapper], f)
c.Start()

f = open("log-NPGA.txt", "w")
c = QualityTest([Methods.ParetoOptimization.NPGA.NPGA_wrapper], f)
c.Start()

f = open("log-NSGA.txt", "w")
c = QualityTest([Methods.ParetoOptimization.NSGA.NSGA_wrapper], f)
c.Start()