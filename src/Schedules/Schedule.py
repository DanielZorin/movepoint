'''
Created on 03.11.2010

@author: juan
'''
from Schedules.Program import Program
from Schedules.Operation import *
from Core.Processor import Processor
from Core.NVP import NVP
from Core.Reserve import Reserve
from Schedules.ScheduleVertex import ScheduleVertex
from Schedules.Exceptions import SchedulerTypeException

class Schedule(object):
    '''Represents a schedule for a certain program. A schedule is a set of quadruples
    (task, version, processor, number). Info about reserve processor is stored here too.
    
    :param program: :class:`~Schedules.Program.Program` object
    :param processors: List of available processors'''
    
    vertices = {}
    '''Dictionary of :class:`~Core.Processor.Processor` numbers to 
    :class:`~Schedules.ScheduleVertex.ScheduleVertex` objects'''
    
    processors = []
    '''List of :class:`~Core.Processor.Processor` '''
    
    program = None
    ''':class:`~Schedules.Program.Program` scheduled'''
    
    availableProcessors = []
    ''' List of :class:`~Core.Processor.Processor` objects representing the types of processors
    that can be used. In future it'll contain more info on them'''
    
    currentVersions = {}
    
    # TODO: rename: delays -> idletimes, waiting -> delays
    delays = []
    waiting = []
    endtimes = []
    
    # These arrays are filled during the interpretation.
    # This data is used for fast drawing of the schedule in GUI.
    executionTimes = {}
    deliveryTimes = []
    
    _depCache = {}
    _transCache = {}
    _succCache = {}
    
    def __init__(self, program, processors=[]):
        self.program = program
        self.availableProcessors = processors
        self.emptyprocessors = []
        self.vertices = {}
        for v in self.program.vertices:
            p = self._getProcessor()
            s = ScheduleVertex(v, v.versions[0], p)
            self.vertices[p.number] = [s]
            self.currentVersions[v.number] = [s]
        
    def __str__(self):
        res = "Schedule: \n"
        for k in self.vertices.keys():
            proc = "Processor " + str(k) + ": "
            for v in self.vertices[k]:
                proc += str(v.v.number) + " -- "
            proc += "\n"
            res += proc
        return res
    
    def SetToDefault(self):    
        ''' Places each vertex on a new processor'''
        self.vertices = {}
        self.processors = []
        self.emptyprocessors = []
        i = 1
        for v in self.program.vertices:
            p = self._getProcessor()
            s = ScheduleVertex(v, v.versions[0], p)
            self.vertices[p.number] = [s]
            self.currentVersions[v.number] = [s]
            i += 1
            
    def SetToDefault2(self):
        ''' Places all vertices on one processor '''
        self.vertices = {}
        self.processors = []
        self.emptyprocessors = []
        p = self._getProcessor()
        i = 1
        self.vertices[p.number] = []
        for v in self.program.vertices:
            s = ScheduleVertex(v, v.versions[0], p)
            self.vertices[p.number].append(s)
            self.currentVersions[v.number] = [s]
            i += 1  
        
    '''Auxiliary functions to handle the set of working processors'''   
        
    # Returns a processor where it's possible to assign a new task
    # Here it just creates a new processor from the list of available processors
    # Reimplement this if you need to make the number of processors limited
    def _getProcessor(self, proc=None):
        if not proc is None:
            # TODO: check errors
            ind = self.emptyprocessors.index(proc)
            m = self.emptyprocessors[ind]
            del self.emptyprocessors[ind]
            self.processors.append(m)
            return m

        if len(self.emptyprocessors) > 0:
            p = self.emptyprocessors[0]
            self.emptyprocessors = self.emptyprocessors[1:]
        else:
            p = Processor(self.GetProcessorsWithoutDoubles() + 1, \
                          self.availableProcessors[0].reliability, \
                          self.availableProcessors[0].speed)
        self.processors.append(p)
        return p
    
    def _delEmptyProc(self, p):
        if self.vertices[p.number]:
            return
        del self.vertices[p.number]
        tmp = []
        for v in self.processors:
            if v != p:
                tmp.append(v)
                
        if not p in self.emptyprocessors:
            p.reserves = 1
            self.emptyprocessors.append(p)
        self.processors = tmp
     
    '''Auxiliary functions: check dependencies between vertices'''
    
    def _dep(self, s):
        dep = []
        #self.program._buildData()
        for v in self.program._dep[s.v.number]:
            dep += self.currentVersions[v.number]
        return dep
    
    def _trans(self, s):
        trans = []
        #self.program._buildData()
        for v in self.program._trans[s.v.number]:
            trans += self.currentVersions[v.number]
        return trans
        
    def _succ(self, s):
        # TODO: WHAT THE FLYING FUCK IS GOING ON WITH SUCC CACHE!?
        try:
            return self._succCache[s]
        except:
            pass
        cur = self._trans(s)
        new = []
        while True:
            for v in cur:
                new.append(v)
                tr = self._trans(v)
                new += tr
                new += self.vertices[v.m.number][self.vertices[v.m.number].index(v):]
                new = list(set(new))
            if len(new) == len(cur):
                self._succCache[s] = new
                return new
            else:
                cur = new
                new = []

    '''Search specific elements in the schedule'''
    
    def FindVertex(self, v = None, k = None):
        ''' Returns the first vertex satisfying the given (v, k, m, n) mask.
        "None" stands for any value'''
        for m in self.vertices.keys():
            for t in self.vertices[m]:
                if (v is None) or (t.v == v):
                    if (k is None) or (t.k == k):
                        return t
        return None
     
    def FindAllVertices(self, v = None, k = None):
        ''' Returns a list of vertices satisfying the given mask.
        "None" stands for any value'''
        res = []
        for m in self.vertices.keys():
            for t in self.vertices[m]:
                if (v is None) or (t.v == v):
                    if (k is None) or (t.k == k):
                        res.append(t)
        return res
    
    def FindProcessor(self, v):
        for m in self.vertices.keys():
            if v in self.vertices[m]:
                return self.GetProcessor(m)
        raise "None"
    
    def GetProcessor(self, n):
        for p in self.processors:
            if p.number == n:
                return p
        raise "None"
    
    '''Main features of a schedule: time, reliability, size'''

    def GetTime(self):
        ''' Returns the time of schedule execution assuming that data delivery begins as soon as the task ends'''
        def FindReadyTask(l, parsed):
            for s in l:
                b = True
                for v in self._dep(s):
                    if not (v in parsed):
                        b = False
                if s.n > 1:
                    if not (self.vertices[s.m.number][s.n-2] in parsed):
                        b = False
                if b:
                    return s
            raise "FindReadyTask: Error"
        
        parsed = []
        notparsed = []
        for v in self.vertices.values():
            notparsed += v
        timestamps = {}
        while notparsed != []:
            s = FindReadyTask(notparsed, parsed)
            parsed.append(s)
            del notparsed[notparsed.index(s)]
            curtime = s.Processor().GetTime(s.Task().time)
            # First task starts at 0, others start when the previous one ends
            if s.n == 1:
                max = 0
            else:
                max = timestamps[self.vertices[s.m.number][s.n-2]]
            for prev in self._dep(s):
                e = self.program.FindEdge(prev.v, s.v)
                tmp = timestamps[prev] + prev.Processor().GetDeliveryTime(s.Processor(), e.volume)
                if tmp > max:
                    max = tmp
            timestamps[s] = max + curtime
        max = 0
        for v in timestamps.values():
            if v > max:
                max = v       
        return max
    
    def Interpret(self):
        ''' Returns the time of schedule execution assuming that each processor supports
        only one sending/receiving operation at a time. If one of the processors is busy, the delivery
        is added to the queue and is initiated only when both processors become available.'''
        # Uses local variables donetasks and edges
        def CheckReady(v):
            for v0 in self._dep(v):
                if not (v0 in donetasks):
                    # Waiting for some task
                    return False
            for e in edges:
                if (e[1] == v) and (e[3] == False):
                    # Waiting for a delivery to finish
                    return False
            return True

        # Ordered queue of tasks for each processor
        sortedTasks = {}
        # Current step
        time = 0
        # List of finished tasks
        donetasks = []
        # Status of each processor and remaining time
        working = {}
        # List of current deliveries
        deliveries = []
        # List of pending deliveries
        deliveryQueue = []
        # Status of the port of each processor (busy=True/ready=False)
        portStatus = {}
        # List of all pairs that cause delivery data between processors
        edges = []
        # Waiting time of each vertex
        delays = {}
        self.delays = []
        # point of time when a certain task is over. Used to calculate waiting time
        endTimes = {}
        self.waiting = []
        self.executionTimes = {}
        self.deliveryTimes = []
        for e in self.program.edges:
            for i in self.FindAllVertices(v=e.source):
                for j in self.FindAllVertices(v=e.destination):
                    if i.m != j.m:
                        # Add only deliveries between different processors
                        # The boolean field indicates whether the delivery is finished or not
                        edges.append([i, j, e.volume, False])
        
        for proc in self.processors:
            m = proc.number
            sortedTasks[m] = [v for v in self.vertices[m]]
            working[m] = None
            portStatus[m] = False
            if len(sortedTasks[m]) > 0:
                first = sortedTasks[m][0]
                if len(self._dep(first)) == 0:
                    working[m] = ["working", first.m.GetTime(first.Task().time)]
                    self.executionTimes[first] = (time, time + first.m.GetTime(first.Task().time))
                else:
                    working[m] = ["waiting"]
                    delays[first] = 0
            else:
                # TODO: this is a bug. Empty processors shouldn't exist
                working[m] = ["ready"]
        while True:
            # Print debug information
            '''
            print("Time = ", time)
            for m in self.processors:
                print("Processor ", m.number, " ", working[m][0])
                if working[m][0] == "working":
                    print(sortedTasks[m][0].v.number)
                    print(" ", working[m][1], " seconds left")
                print("port is ", portStatus[m])
            print("Deliveries: ")
            for d in deliveries:
                print("From: ", d[0].m, " To: ", d[1].m,  d[2], " seconds left") 
            for d in deliveryQueue:
                print(d) 
            for e in edges:
                print("Edge ", e[0].v.number, " ", e[1].v.number, " ", e[3])   
            print("------------------------------------")   
            '''
                
            time += 1
            
            # Advance all deliveries
            deliv2 = []
            for d in deliveries:
                if d[2] > 0:
                    d[2] -= 1
                    deliv2.append(d)
                else:
                    for e in edges:
                        if (e[0] == d[0]) and (e[1] == d[1]):
                            # The delivery is over. We add the info about it to deliveryTimes
                            e[3] = True
                            self.deliveryTimes.append((e[0].m, e[1].m, time - e[2], time))
                    portStatus[d[0].m] = False
                    portStatus[d[1].m] = False
                        
            deliveries = deliv2
            
            # Advance all tasks by 1 quantum
            for proc in self.processors:
                m = proc.number
                if working[m][0] == "working":
                    if working[m][1] > 1:
                        # One more quantum of work
                        working[m][1] -= 1
                    else:
                        # Task is over
                        # Add all deliveries to the queue
                        tmp = []
                        for e in edges:
                            if e[0] == sortedTasks[m][0]:
                                tmp.append([e[1], e[2]])
                        if len(tmp) > 0:
                            deliveryQueue.append([sortedTasks[m][0], tmp])
                        # Delete the complete task and start a new one
                        donetasks.append(sortedTasks[m][0])
                        endTimes[sortedTasks[m][0]] = time
                        sortedTasks[m] = sortedTasks[m][1:]
                        if len(sortedTasks[m]) == 0:
                            working[m] = ["ready"]
                        else:
                            if CheckReady(sortedTasks[m][0]):
                                working[m] = ["working", proc.GetTime(sortedTasks[m][0].Task().time)]
                                # The task is put to execution, it will end after a fixed period of time
                                self.executionTimes[sortedTasks[m][0]] = (time, time + proc.GetTime(sortedTasks[m][0].Task().time))
                            else:
                                working[m] = ["waiting"]
                                delays[sortedTasks[m][0]] = 0
                elif working[m][0] == "waiting":
                    if CheckReady(sortedTasks[m][0]):
                        working[m] = ["working", proc.GetTime(sortedTasks[m][0].Task().time)]
                        self.executionTimes[sortedTasks[m][0]] = (time, time + proc.GetTime(sortedTasks[m][0].Task().time))
                        self.delays.append([sortedTasks[m][0],delays[sortedTasks[m][0]]])
                    else:
                        working[m] = ["waiting"]
                        delays[sortedTasks[m][0]] += 1
                
            # Start deliveries
            deliv2 = []
            for e in deliveryQueue:
                b = True
                if portStatus[e[0].m.number] == True:
                    b = False
                for d in e[1]:
                    if portStatus[d[0].m.number] == True:
                        b = False
                if b:
                    # Append: source, destination, length
                    portStatus[e[0].m.number] = True
                    for d in e[1]:
                        deliveries.append([e[0], d[0], e[0].m.GetDeliveryTime(d[0].m, d[1])-1])
                        portStatus[d[0].m.number] = True
                else:
                    deliv2.append(e)
            deliveryQueue = deliv2              
            
            # If all processors are "ready", stop interpretation
            b = True
            for m in self.processors:
                if working[m][0] != "ready":
                    b = False        
            if b:
                break
            
            # TODO: this is an old workaround used for debugging. Beware.
            if time > 1000:
                print(self)
                raise "Can't calculate time. Possibly an infinite loop occurred"
        
        self.delays = sorted(self.delays, key=lambda x: x[1])
        # Calculate waiting time for each task
        for m in self.processors:
            for v in self.vertices[m.number]:
                start = endTimes[v] - v.m.GetTime(v.v.time)
                dep = self._dep(v)
                tmp = 0
                for v0 in dep:
                    if start - endTimes[v0] > tmp:
                        tmp = start - endTimes[v0]
                self.waiting.append([v, tmp])
        self.waiting = sorted(self.waiting, key=lambda x: x[1])
        self.endtimes = endTimes
        return time
    
    def GetReliability(self):
        ''' Calculates reliability of the system as a product of the reliability 
        of all processors (including reserves) and the reliability of all tasks
        (including the task that are run with NVP)'''
        hard = 1.0
        soft = 1.0      
        for p in set(self.processors):
            proc = [p for i in range(p.reserves)]
            r = Reserve(proc)
            hard *= r.GetReliability() 
           
        for ver in self.program.vertices:
            vers = self.currentVersions[ver.number]
            # TODO: read pall, pd, prv from config file
            nvp = NVP([v.Version() for v in vers], [], 1.0, 1.0, 1.0)
            soft *= nvp.GetReliability()

        return hard * soft
    
    def GetProcessors(self):
        ''' :return: the total number of processors used in the schedule'''
        return sum([p.reserves for p in self.processors])
    
    def GetProcessorsWithoutDoubles(self):
        ''' :return: the number of main processors (not counting the reserves) '''
        return len(set(self.processors))
    
    '''Operations with schedules'''
    
    def ApplyOperation(self, op):
        if isinstance(op, AddProcessor):
            return self.AddProcessor(op.processor)
        elif isinstance(op, DeleteProcessor):
            return self.DeleteProcessor(op.processor)
        elif isinstance(op, AddVersion):
            return self.AddVersion(op.task, op.pos1[0], op.pos1[1], op.pos2[0], op.pos2[1])
        elif isinstance(op, DeleteVersion):
            return self.AddVersion(op.task)
        elif isinstance(op, MoveVertex):
            return self.MoveVertex(op.task, op.pos1[1], op.pos2[0], op.pos2[1])
        elif isinstance(op, MultiOperation):
            for o in op.ops:
                self.ApplyOperation(o)
    
    def AddProcessor(self, m):
        ''' Adds a reserve to processor m
        
        :return: True is the operation is successful (m exists and it's possible to add a reserve)'''
        for p in self.processors:
            if p == m:
                p.reserves += 1
                return True
        return False
        
    def DeleteProcessor(self, m):
        ''' Deletes a reserve to processor m
        
        :return: True is the operation is successful (m exists and has at least one reserve'''
        if m.reserves > 1:
            m.reserves -= 1
            return True
        else:
            return False
        
    def AddVersion(self, v, p1=None, n1=None, p2=None, n2=None):
        ''' Adds a pair of versions to task v
        
        :return: True is the operation is successful (v exists and it's possible to add two versions)'''
        curver = self.FindAllVertices(v=v)
        totalver = v.versions
        #Not enough versions
        if len(totalver) <= len(curver) + 1:
            return False
        if not p1:
            p = self._getProcessor()
            s1 = ScheduleVertex(v, totalver[len(curver)], p)
            s2 = ScheduleVertex(v, totalver[len(curver)+1], p)
            self.vertices[p.number] = [s1, s2]
        else:
            p = p1
            s1 = ScheduleVertex(v, totalver[len(curver)], p1)
            s2 = ScheduleVertex(v, totalver[len(curver)+1], p1)
            self.vertices[p1.number].insert(n1-1, s1)
            self.vertices[p2.number].insert(n2-1, s2)
        self.currentVersions[v.number] += [s1, s2]
        self._succCache = {}
        return p.number
    
    def DeleteVersion(self, v):
        ''' Deletes a pair of versions of task v
        
        :return: True if the operation is successful (v exists and has at least three versions used)'''
        curver = self.currentVersions[v.number]
        # Only one version remains
        if len(curver) == 1:
            return False

        # TODO: this is assuming versions are ordered
        s1 = curver[len(curver) - 1]
        s2 = curver[len(curver) - 2]
        p1 = s1.m
        p2 = s2.m
        proc1 = self.vertices[p1.number]
        proc2 = self.vertices[p2.number]
        self.currentVersions[v.number] = self.currentVersions[v.number][:-2]
        n1 = proc1.index(s1)
        n2 = proc2.index(s2)
        del proc1[proc1.index(s1)]
        self._delEmptyProc(p1)
        del proc2[proc2.index(s2)]
        #TODO: is this really correct when p1=p2?
        self._delEmptyProc(p2)
        self._succCache = {}
        return (p1, p2, n1, n2)
        
    def MoveVertex(self, s, n1, m2, n2):
        ''' Moves a :class:`~Schedules.ScheduleVertex.ScheduleVertex` s1 to position n on processor m 
        
        :return: True if the operation is successful (all objects exist and the operation doesn't cause the appearance of cycles in the schedule)'''
        self._succCache = {}
        # m = None -> move to a new processor
        if m2 == None or not m2 in self.processors:
            p = self._getProcessor(m2)
            self.vertices[p.number] = [s]
            del self.vertices[s.m.number][n1]
            self._delEmptyProc(s.m)
            s.m = p
            return True
        if s.m == m2:
        # Same processor
            del self.vertices[s.m.number][n1]
            if n2 > n1:
                n2 -= 1
            self.vertices[s.m.number].insert(n2, s)
            return True
        else:
        #Different processors
            del self.vertices[s.m.number][n1]
            self.vertices[m2.number].insert(n2, s)
            self._delEmptyProc(s.m)
            s.m = m2
            return True
 
    # TODO: deprecate this method       
    def TryMoveVertex(self, s, n1, m2, n2):
        '''.. deprecated:: 0.1
        
        Use MoveVertex'''
        if s.m == m2:
        # Same processor
            if n2 > n1:
            #Move forward
                if len(self.vertices[s.m.number]) < n2:
                    return False
                if len(self.vertices[s.m.number]) == n2:
                    n2 -= 1
                s2 = self.vertices[s.m.number][n2]
                # TODO: bug with nonexistent position. Fix it in the algorithm
                if s2 in self._succ(s) or s2 is None:
                    return False
                else:
                    return True
            else:
            #Move backward
                after_s2 = self.vertices[s.m.number][n2:n1]
                for v in after_s2:
                    if s in self._succ(v):
                        return False
                return True
        else:
        #Different processors
            # m = None -> move to a new processor
            if m2 == None:
                return True
            succ_s = self._succ(s)
            other_proc = self.vertices[m2.number]
            if n2 > len(other_proc) + 1:
                return False
            for v in other_proc[:n2]:
                if v in succ_s:
                    return False
            for v in other_proc[n2:]:
                if s in self._succ(v):
                    return False
            return True
        
    def CanDeleteProcessor(self):
        ''':return: True if there is at least one processor with at least one reserve'''
        for m in self.processors:
            if m.reserves > 1:
                return True
        return False
    
    def CanDeleteVersions(self):
        ''':return: True if there is at least one task with more than one version '''
        for v0 in self.vertices.values():
            for v in v0:
                if v.k.number > 1:
                    return True
        return False
    
    def CanAddVersions(self):
        ''':return: True if there is at least one task with two available unused versions
        
        .. warning:: Not implemented yet'''
        for v in self.program.vertices:
            cur = self.currentVersions[v.number]
            if len(v.versions) >= len(cur) + 2:
                return True
        return False
