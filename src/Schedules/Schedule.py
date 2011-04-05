'''
Created on 03.11.2010

@author: juan
'''
from Schedules.Program import Program
from Core.Processor import Processor
from Core.NVP import NVP
from Core.Reserve import Reserve
from Schedules.ScheduleVertex import ScheduleVertex
from Schedules.Exceptions import SchedulerTypeException

class Schedule(object):
    
    vertices = []
    processors = []
    program = None
    availableProcessors = []
    
    # TODO: rename: delays -> idletimes, waiting -> delays
    delays = []
    waiting = []
    endtimes = []
    
    # These arrays are filled during the interpretation.
    # This data is used for fast drawing of the schedule in GUI.
    executionTimes = {}
    deliveryTimes = []
    
    '''Constructors and auxiliary functions'''
    
    def __init__(self, program, processors=[]):
        self.program = program
        self.availableProcessors = processors
        self.emptyprocessors = []
        #TODO: reconsider this. 
        self.SetToDefault()
        
    def __str__(self):
        res = "Schedule: \n"
        for v in self.vertices:
            res+= str(v)
        return res
    
    def SetToDefault(self):    
        # Each vertex is placed on a new processor
        self.vertices = []
        self.processors = []
        self.emptyprocessors = []
        i = 1
        for v in self.program.vertices:
            p = self._getProcessor()
            s = ScheduleVertex(v, v.versions[0], p, 1)
            self.vertices.append(s)
            i += 1
            
    def SetToDefault2(self):
        # All vertices are placed on one processor
        self.vertices = []
        self.processors = []
        self.emptyprocessors = []
        p = self._getProcessor()
        i = 1
        for v in self.program.vertices:
            s = ScheduleVertex(v, v.versions[0], p, i)
            self.vertices.append(s)
            i += 1  
        
    '''Auxiliary functions to handle the set of working processors'''   
        
    # Returns a processor where it's possible to assign a new task
    # Here it just creates a new processor from the list of available processors
    # Reimplement this if you need to make the number of processors limited
    def _getProcessor(self):
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
        for v in self.vertices:
            if v.m == p:
                return
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
        res = []
        for e in self.program.edges:
            if e.destination == s.v:
                res.append(self.FindVertex(v=e.source))
        return res
    
    def _trans(self, s):
        cur = [s]
        new = []
        while True:
            for v1 in cur:
                if not(v1 in new):
                    new.append(v1)
                for v2 in self.vertices:
                    if self.program.FindEdge(v1.v, v2.v):
                        if not(v2 in new):
                            new.append(v2)
            if new == cur:
                # Delete s and all its versions
                final = []
                for v in new:
                    if v.v != s.v:
                        final.append(v)
                return final
            else:
                cur = []
                for v in new:
                    cur.append(v)
                new = []        
    
    def _succ(self, s):
        cur = self._trans(s)
        new = []
        while True:
            for v1 in cur:
                if not(v1 in new):
                    new.append(v1)
                tr = self._trans(v1)
                for v in tr:
                    if not(v in new):
                        new.append(v)
                for v2 in self.vertices:
                    if v1.m == v2.m and v1.n < v2.n:
                        if not(v2 in new):
                            new.append(v2)
            if new == cur:
                return new
            else:
                cur = []
                for s in new:
                    cur.append(s)
                new = []                  

    '''Search specific elements in the schedule'''
    
    #Returns the first vertex satisfying the given mask.
    #"None" stands for any value
    def FindVertex(self, v = None, k = None, m = None, n = None):
        for ver in self.vertices:
            if (v is None) or (ver.v == v):
                if (k is None) or (ver.k == k):
                    if (m is None) or (ver.m == m):
                        if (n is None) or (ver.n == n):
                            return ver
        return None
    
    # Returns a list of vertices satisfying the given mask
    def FindAllVertices(self, v = None, k = None, m = None, n = None):
        res = []
        for ver in self.vertices:
            if (v is None) or (ver.v == v):
                if (k is None) or (ver.k == k):
                    if (m is None) or (ver.m == m):
                        if (n is None) or (ver.n == n):
                            res.append(ver)
        return res
    
    '''Main features of a schedule: time, reliability, size'''

    def GetTime(self):
        def FindReadyTask(l, parsed):
            for s in l:
                b = True
                for v in self._dep(s):
                    if not (v in parsed):
                        b = False
                if s.n > 1:
                    if not (self.FindVertex(m=s.m, n=s.n-1) in parsed):
                        b = False
                if b:
                    return s
            return None
        
        parsed = []
        notparsed = list(self.vertices)
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
                max = timestamps[self.FindVertex(m=s.m, n=s.n-1)]
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
        # Uses local variables donetasks and edges
        def CheckReady(v):
            for v0 in self._dep(v):
                if not (v0 in donetasks):
                    # Waiting for some task
                    return False
            for e in edges:
                if (e[1] == v) and (e[3] == False):
                    # Waiting for delivery to finish
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
        
        for m in self.processors:
            tmp = sorted(self.FindAllVertices(m=m), key=lambda x: x.n)
            #print(tmp)
            sortedTasks[m] = tmp
            #print(sortedTasks[m])
            working[m] = None
            portStatus[m] = False
            #print(tmp)
            if len(sortedTasks[m]) > 0:
                first = sortedTasks[m][0]
                if len(self._dep(first)) == 0:
                    working[first.m] = ["working", first.m.GetTime(first.Task().time)]
                    self.executionTimes[first] = (time, time + first.m.GetTime(first.Task().time))
                else:
                    working[first.m] = ["waiting"]
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
            for m in self.processors:
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
                                working[m] = ["working", m.GetTime(sortedTasks[m][0].Task().time)]
                                # The task is put to execution, it will end after a fixed period of time
                                self.executionTimes[sortedTasks[m][0]] = (time, time + m.GetTime(sortedTasks[m][0].Task().time))
                            else:
                                working[m] = ["waiting"]
                                delays[sortedTasks[m][0]] = 0
                elif working[m][0] == "waiting":
                    if CheckReady(sortedTasks[m][0]):
                        working[m] = ["working", m.GetTime(sortedTasks[m][0].Task().time)]
                        self.executionTimes[sortedTasks[m][0]] = (time, time + m.GetTime(sortedTasks[m][0].Task().time))
                        self.delays.append([sortedTasks[m][0],delays[sortedTasks[m][0]]])
                    else:
                        working[m] = ["waiting"]
                        delays[sortedTasks[m][0]] += 1
                
            # Start deliveries
            deliv2 = []
            for e in deliveryQueue:
                b = True
                if portStatus[e[0].m] == True:
                    b = False
                for d in e[1]:
                    if portStatus[d[0].m] == True:
                        b = False
                if b:
                    # Append: source, destination, length
                    portStatus[e[0].m] = True
                    for d in e[1]:
                        deliveries.append([e[0], d[0], e[0].m.GetDeliveryTime(d[0].m, d[1])-1])
                        portStatus[d[0].m] = True
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
            # TODO: this is an old workaround used for testing. Beware.
            if time > 1000000:
                break
        
        self.delays = sorted(self.delays, key=lambda x: x[1])
        # Calculate waiting time for each task
        for v in self.vertices:
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
        hard = 1.0
        soft = 1.0      
        for p in set(self.processors):
            proc = [p for i in range(p.reserves)]
            r = Reserve(proc)
            hard *= r.GetReliability() 
           
        for ver in self.program.vertices:
            vers = self.FindAllVertices(v=ver)
            # TODO: read pall, pd, prv from config file
            nvp = NVP([v.Version() for v in vers], [], 1.0, 1.0, 1.0)
            soft *= nvp.GetReliability()

        return hard * soft
    
    def GetProcessors(self):
        return sum([p.reserves for p in self.processors])
    
    def GetProcessorsWithoutDoubles(self):
        return len(set(self.processors))
    
    '''Operations with schedules'''
    
    def AddProcessor(self, m):
        for p in self.processors:
            if p == m:
                p.reserves += 1
                return True
        return False
        
    def DeleteProcessor(self, m):
        if m.reserves > 1:
            m.reserves -= 1
            return True
        else:
            return False
        
    def AddVersion(self, v):
        curver = self.FindAllVertices(v=v)
        totalver = v.versions
        #Not enough versions
        if len(totalver) <= len(curver) + 1:
            return False
        p = self._getProcessor()
        s1 = ScheduleVertex(v, totalver[len(curver)], p, 1)
        s2 = ScheduleVertex(v, totalver[len(curver)+1], p, 2)
        self.vertices.append(s1)
        self.vertices.append(s2)
        return True
    
    def DeleteVersion(self, v):
        curver = self.FindAllVertices(v=v)
        # Only one version remains
        if len(curver) == 1:
            return False

        # TODO: this is assuming versions are ordered
        s1 = curver[len(curver) - 1]
        s2 = curver[len(curver) - 2]
        p1 = s1.m
        p2 = s2.m
        proc1 = self.FindAllVertices(m=p1)
        proc2 = self.FindAllVertices(m=p2)
        for v in proc1:
            if v.n > s1.n:
                v.n -= 1
        for v in proc2:
            if v.n > s2.n:
                v.n -= 1
        del self.vertices[self.vertices.index(s1)]
        del self.vertices[self.vertices.index(s2)]
        self._delEmptyProc(p1)
        #TODO: is this really correct when p1=p2?
        self._delEmptyProc(p2)
        
    def MoveVertex(self, s1, m, n):
        if s1.m == m:
        # Same processor
            if n > s1.n:
            #Move forward
                s2 = self.FindVertex(m=s1.m, n=n)
                # TODO: fix this. Why is s2 == None when there's only one processor?
                if s2 in self._succ(s1) or s2 == None:
                    return False
                else:
                    after_s2 = self.FindAllVertices(m = s1.m)
                    for v in after_s2:
                        if (v.n <= s2.n) and (v.n > s1.n):
                            v.n -= 1
                    s1.n = n
                    self._delEmptyProc(s1.m)
                    return True
            elif n < s1.n:
            #Move backward
                after_s2 = self.FindAllVertices(m = s1.m)
                for v in after_s2:
                    if v.n >= n and v.n < s1.n:
                        if s1 in self._succ(v):
                            return False
                for v in after_s2:
                    if v.n >= n and v.n < s1.n:
                        v.n += 1
                s1.n = n
                self._delEmptyProc(s1.m)
                return True
            else:
                # "Move" to the same position
                return True
        else:
        #Different processors
            # m = None -> move to a new processor
            if m == None:
                p = self._getProcessor()
                s1_proc = self.FindAllVertices(m = s1.m)
                for v in s1_proc:
                    if v.n > s1.n:
                        v.n -= 1  
                old = s1.m
                s1.m = p
                s1.n = 1
                self._delEmptyProc(old)
                return True
            succ_s1 = self._succ(s1)
            s1_proc = self.FindAllVertices(m = s1.m)
            other_proc = self.FindAllVertices(m = m)
            if n > len(other_proc) + 1:
                return False
            for v in other_proc:
                if v.n < n:
                    if v in succ_s1:
                        return False
                if v.n >= n:
                    if s1 in self._succ(v):
                        return False
            for v in other_proc:
                if v.n >= n:
                    v.n += 1
            for v in s1_proc:
                if v.n > s1.n:
                    v.n -= 1        
            s1.n = n
            p = s1.m
            s1.m = m
            self._delEmptyProc(p)
            return True  
 
    # TODO: deprecate this method       
    def TryMoveVertex(self, s1, m, n):
        if s1.m == m:
        # Same processor
            if n > s1.n:
            #Move forward
                s2 = self.FindVertex(m=s1.m, n=n)
                if s2 in self._succ(s1):
                    return False
                else:
                    return True
            else:
            #Move backward
                after_s2 = self.FindAllVertices(m = s1.m)
                for v in after_s2:
                    if v.n >= n and v.n < s1.n:
                        if s1 in self._succ(v):
                            return False
                return True
        else:
        #Different processors
            # m = None -> move to a new processor
            if m == None:
                return True
            succ_s1 = self._succ(s1)
            s1_proc = self.FindAllVertices(m = s1.m)
            other_proc = self.FindAllVertices(m = m)
            if n > len(other_proc) + 1:
                return False
            for v in other_proc:
                if v.n < n:
                    if v in succ_s1:
                        return False
                if v.n >= n:
                    if s1 in self._succ(v):
                        return False
            return True
        
    def CanDeleteProcessor(self):
        for v in self.vertices:
            if v.m.reserves > 1:
                return True
        return False
    
    def CanDeleteVersions(self):
        for v in self.vertices:
            if v.k.number > 1:
                return True
        return False
    
    def CanAddVersions(self):
        return True