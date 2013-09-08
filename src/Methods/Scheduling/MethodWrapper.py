'''
Created on 10.11.2010

@author: juan
'''

from Schedules.Operation import *
from Schedules.Schedule import *
from Schedules.SimpleInterpreter import SimpleInterpreter
from Methods.Scheduling.SimulatedAnnealing import *
import logging, multiprocessing, os, threading

class MethodWrapper(object):
    ''' Simulated Annealing method adapted for scheduling.
    
    .. warning:: Write details here'''
    
    system = None
    ''' System, program and schedule to optimize'''
    
    iteration = 1
    ''' Current iteration (see Simulated Annealing) '''
    
    numberOfIterations = 0
    ''' Number of iteration is 10 * number of vertices '''
    
    lastOperation = VoidOperation()
    ''' Here we keep the info about the last operation. It's used in GUI '''

    parallelThreads = 1
    ''' Number of parallel threads. By default, there is no parallelism'''

    limits = []
    
    trace = [Trace()]

    algs = []

    algorithm = None
    '''The actual algorithm instance'''

    # TODO: find a better solution
    interpreter = SimpleInterpreter()

    def __init__(self, system):
        self.iteration = 1
        self.system = system
        self.numberOfIterations = len(self.system.program.vertices) * 1 + 1
        self._prepare()
    
    def ChangeSystem(self, s):
        ''' Replace the system'''
        self.numberOfIterations = len(self.system.program.vertices) * 1
        self.system = s
        self._prepare()
    
    def Reset(self):
        ''' Resets the method to the zero iteration'''
        self.system.schedule.SetToDefault()
        self.numberOfIterations = 10 * len(self.system.program.vertices)
        self._prepare()
        self.algorithm.Prepare()
   
    def _prepare(self):
        self.limits = []
        if self.parallelThreads > 1:
            pass

        self.trace = []
        for i in range(self.parallelThreads):
            self.trace.append(Trace())
        for t in self.trace:
            t.clear()
            self.lastOperation = VoidOperation()
            data = {"time":self.interpreter.Interpret(self.system.schedule),
                    "reliability":self.system.schedule.GetReliability(),
                    "processors":self.system.schedule.GetProcessors()
                    }
            t.addStep(self.lastOperation, data)
            t.setBest(0)
        
    def Start(self):
        ''' Runs the algorithm with the given number of iterations'''
        self.iteration = 1
        if self.parallelThreads == 1:
            while self.algorithm.iteration <= self.numberOfIterations:           
                self.Step()
                self.algorithm.iteration += 1
                if (self.trace[0].getLast()[1]["processors"] == 1) and \
                    (self.trace[0].getLast()[1]["time"]  <= self.system.tdir) and \
                    (self.trace[0].getLast()[1]["reliability"]  >= self.system.rdir):
                    return 
        else:
            threads = []
            algs = [0 for i in range(self.parallelThreads)]
            for id in range(self.parallelThreads):
                limits = []
                print ("thread ", id)
                s = Schedule(self.system.program, self.system.schedule.availableProcessors)
                s.SetToDefault()
                algs[id] = SimulatedAnnealing(s, (self.algorithm.tdir, self.algorithm.rdir), self.trace[id], SimpleInterpreter())
                thread = threading.Thread(target=self.StartThread, args=(algs[id], limits, id))
                threads.append(thread)
                thread.start()
            #for t in threads:
            #    t.join()
        return
    
    def StartThread(self, alg, limits, id):
        self.trace[id].deleteTail(self.system.tdir, self.system.rdir)
        self.lastOperation = VoidOperation()
        while alg.iteration <= self.numberOfIterations:
            print ("thread " + str(id) +  " " + str(alg.iteration))
            alg.Step(limits, id)
            alg.iteration += 1
            if (self.trace[id].getLast()[1]["processors"] == 1) and \
                (self.trace[id].getLast()[1]["time"]  <= self.system.tdir) and \
                (self.trace[id].getLast()[1]["reliability"]  >= self.system.rdir):
                return      

            
    def Step(self):
        ''' Makes a single iteration of the algorithm'''
        self.trace[0].deleteTail(self.system.tdir, self.system.rdir)
        self.lastOperation = VoidOperation()
        self.algorithm.Step()

    def ScrollTrace(self, diff):
        ''' Scrolls diff operations along the trace'''
        if diff == 0:
            return
        if diff > 0:
            if self.trace[0].current + diff >= self.trace[0].length():
                diff = self.trace[0].length() - self.trace[0].current - 1
            for i in range(diff):
                self.trace[0].current += 1
                op = self.trace[0].getCurrent()
                self.system.schedule.ApplyOperation(op[0])
        if diff < 0:
            if self.trace[0].current + diff < 0:
                diff = -self.trace.current
            for i in range(-diff):
                op = self.trace[0].getCurrent()
                self.system.schedule.ApplyOperation(op[0].Reverse())
                self.trace[0].current -= 1

    def ManualStep(self, op, **params):
        ''' Callback for applying operations from the outside of this class, i.e. when the operation is defined by GUI'''
        if op == "MoveVertex":
            v = params["v"]
            n1 = params["n1"]
            n2 = params["n2"]
            m2 = params["m2"]
            res = self.system.schedule.TryMoveVertex(v, n1, m2, n2)
            if res != True:
                return res
            else:
                self.lastOperation = MoveVertex(v, v.m, n1, m2, n2)
                self.system.schedule.ApplyOperation(self.lastOperation)
        elif op == "AddProcessor":
            m = params["m"]
            self.lastOperation = AddProcessor(m)
            self.system.schedule.ApplyOperation(self.lastOperation)
        elif op == "DeleteProcessor":
            m = params["m"]
            self.lastOperation = DeleteProcessor(m)
            self.system.schedule.ApplyOperation(self.lastOperation)
        elif op == "AddVersion":
            v = params["v"]
            newproc = self.system.schedule.AddVersion(v)
            self.lastOperation = AddVersion(v, newproc, 1, newproc, 2)
        elif op == "DeleteVersion":
            v = params["v"]
            (m1, m2, n1, n2) = self.system.schedule.DeleteVersion(v) 
            self.lastOperation = DeleteVersion(v, m1, n1, m2, n2)
        
        cur = self.trace.getLast()[1]
        curTime = cur["time"]
        curRel = cur["reliability"]
        curProc = cur["processors"]
        self.lastOperation.result = True
        new_time = self.interpreter.Interpret(self.system.schedule)
        new_rel = self.system.schedule.GetReliability()
        new_proc = self.system.schedule.GetProcessors()
        self.trace[0].deleteTail(self.system.tdir, self.system.rdir)
        self.trace[0].addStep(self.lastOperation, {"time":new_time, "reliability":new_rel, "processors":new_proc})
        return True
