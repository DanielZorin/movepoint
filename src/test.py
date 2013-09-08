from Schedules.System import *
from Schedules.SimpleInterpreter import *
from SchedulerGUI.Project import Project
from plugins.Random import *
from Schedules.Metrics import HMetric
import time, threading

if __name__ == '__main__':
    gen = RandomProgramGenerator()
    # Compare temperatures with each other
    p = Project("program.xml", "temperature test")
    gen.Generate(p.method.system)
    p.method.parallelThreads = 3
    p.method.Reset()
    p.method.Start()
