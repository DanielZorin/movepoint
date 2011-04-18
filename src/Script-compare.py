from Tests.SimpleTest import *
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
from Core.Common import Cmeasure
import pickle,math
#from Optimize.mpmath import erfinv

""" 
f = file("stabil.txt", "r")
pp = pickle.Unpickler(f)
a = pp.load()
#print a
spea = a[0]
spea2 = a[1]
#rs = a[2]
speabest = spea[0]

for p in spea2:
    if Cmeasure(p, speabest) > Cmeasure(speabest, p):
        speabest = p
for q in speabest:
    print q["cost"]
for q in speabest:
    print q["rel"]
    
"""

methods = [Methods.ParetoOptimization.SPEA.SPEA_wrapper,Methods.ParetoOptimization.RandomSelection.RandomSelection,Methods.ParetoOptimization.PAES.PAES,Methods.ParetoOptimization.PESA.PESA,Methods.ParetoOptimization.VEGA.VEGA_wrapper,Methods.ParetoOptimization.NPGA.NPGA_wrapper,Methods.ParetoOptimization.NSGA.NSGA_wrapper, Methods.ParetoOptimization.SPEA2.SPEA2_wrapper]
methods = [Methods.ParetoOptimization.SPEA.SPEA_wrapper,Methods.ParetoOptimization.RandomSelection.RandomSelection,Methods.ParetoOptimization.PAES.PAES,Methods.ParetoOptimization.PESA.PESA]

f = open("stabil.txt", "r")
pp = pickle.Unpickler(f)
a = pp.load()
matrices = []

for n in range(100):
    current = [[-1 for i in range(len(methods))] for j in range(len(methods))]
    for i in range(len(methods)):
        for j in range(len(methods)):
            #print i, j
            current[i][j] = Cmeasure(a[i][n], a[j][n])
    matrices.append(current)
