class SimpleInterpreter:
    idletimes = []
    delays = []
    
    # These arrays are filled during the interpretation.
    # This data is used for fast drawing of the schedule in GUI.
    executionTimes = {}
    deliveryTimes = []

    bandwidth = 1
    delay = 0

    def __init__(self):
        pass

    def GetName(self):
        return "Default"

    def Interpret(self, schedule):
        sc = schedule
        self.idletimes = []
        self.delays = []
        self.executionTimes = {}
        self.deliveryTimes = []
        allverts = []
        verts = {}
        for m in sc.vertices.keys():
            allverts.extend(sc.vertices[m])
            verts[m] = list(sc.vertices[m])
        limit = len(allverts)
        levels = {}
        lev = 0
        parsed = 0
        donetasks = []
        while parsed < limit:
            curlev = []
            for m in [v for v in verts.keys()]:
                ok = True
                for v0 in schedule._dep(verts[m][0]):
                    if not (v0 in donetasks):
                        ok = False
                        break
                if ok:
                    curlev.append(verts[m][0])
                    parsed += 1
                    verts[m] = verts[m][1:]
                    if verts[m] == []:
                        del verts[m]
            donetasks.extend(curlev)
            levels[lev] = curlev
            lev += 1

        proctime = {}
        verts = {}
        incoming = {}
        for m in sc.vertices.keys():
            proctime[m] = 0
            verts[m] = list(sc.vertices[m])
            incoming[m] = []

        for i in range(lev):
            tasks = levels[i]
            for t in tasks:
                inc = [v for v in incoming[t.m] if v[0].destination == t.v]
                begin = proctime[t.m]
                for e in inc:
                    if e[1][3] > begin:
                        begin = e[1][3]
                end = begin + t.m.GetTime(t.Task().time)
                proctime[t.m] = end
                self.executionTimes[t] = (begin, end)
            newdels = []
            for t in tasks:
                nxt = sc._next(t)
                for e in nxt.keys():
                    for other in nxt[e]:
                        if other.m != t.m:
                            begin = self.executionTimes[t][1]
                            end = begin + t.m.GetDeliveryTime(other.m, e.volume) * self.bandwidth + self.delay
                            newd = (t.m, other.m, begin, end)
                            newdels.append(newd)
                            incoming[other.m].append((e, newd))
            self.deliveryTimes.extend(newdels)
        
        time = 0
        for m in proctime.keys():
            if proctime[m] > time:
                time = proctime[m]

        for m in sc.processors:
            pos = 0
            for v in sc.vertices[m.number]:
                start = self.executionTimes[v][0]
                dep = sc._dep(v)
                tmp = 0
                for v0 in dep:
                    end = self.executionTimes[v0][1]
                    if start - end > tmp:
                        tmp = start - end
                self.delays.append([v, tmp])

                if pos == 0:
                    idle = start
                else:
                    idle = start - self.executionTimes[sc.vertices[m.number][pos-1]][1]
                if idle > 0:
                    self.idletimes.append([[m, pos], idle])
                pos += 1
            idle = time - self.executionTimes[sc.vertices[m][-1]][1]
            if idle > 0:
                self.idletimes.append([[m, pos], idle])
        self.idletimes = sorted(self.idletimes, key=lambda x: -x[1])
        self.delays = sorted(self.delays, key=lambda x: -x[1])
        return time

    # This implementation is much slower
    def Interpret2(self, schedule):
        ''' Returns the time of schedule execution assuming that each processor supports
        only one sending/receiving operation at a time. If one of the processors is busy, the delivery
        is added to the queue and is initiated only when both processors become available.'''
        # Uses local variables donetasks and edges
        def CheckReady(v):
            for v0 in schedule._dep(v):
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
        # List of all pairs that cause delivery data between processors
        edges = []
        # Waiting time of each vertex
        delays = {}
        self.idletimes = []
        # point of time when a certain task is over. Used to calculate waiting time
        endTimes = {}
        self.delays = []
        self.executionTimes = {}
        self.deliveryTimes = []
        self.program = schedule.program
        for e in self.program.edges:
            for i in schedule.FindAllVertices(v=e.source):
                for j in schedule.FindAllVertices(v=e.destination):
                    if i.m != j.m:
                        # Add only deliveries between different processors
                        # The boolean field indicates whether the delivery is finished or not
                        edges.append([i, j, e.volume, False])
        
        for proc in schedule.processors:
            m = proc.number
            sortedTasks[m] = [v for v in schedule.vertices[m]]
            working[m] = None
            if len(sortedTasks[m]) > 0:
                first = sortedTasks[m][0]
                if len(schedule._dep(first)) == 0:
                    working[m] = ["working", first.m.GetTime(first.Task().time)]
                    self.executionTimes[first] = (time, time + first.m.GetTime(first.Task().time))
                else:
                    working[m] = ["waiting"]
                    delays[first] = 0
            else:
                # TODO: this is a bug. Empty processors shouldn't exist
                working[m] = ["ready"]
        while True:
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
                            self.deliveryTimes.append((e[0].m, e[1].m, time - e[2] * self.bandwidth - self.delay, time))
                        
            deliveries = deliv2
            
            # Advance all tasks by 1 quantum
            for proc in schedule.processors:
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
                            target_proc = schedule.GetProcessor(m)
                            target_pos = len(schedule.vertices[m])
                            self.idletimes.append([[target_proc, target_pos], time])
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
                        target_proc = schedule.GetProcessor(m)
                        target_pos = schedule.vertices[m].index(sortedTasks[m][0])
                        self.idletimes.append([[target_proc, target_pos], delays[sortedTasks[m][0]] + 1])
                    else:
                        working[m] = ["waiting"]
                        delays[sortedTasks[m][0]] += 1
                
            # Start deliveries
            for e in deliveryQueue:
                # Append: source, destination, length
                for d in e[1]:
                    deliveries.append([e[0], d[0], e[0].m.GetDeliveryTime(d[0].m, d[1]) * self.bandwidth + self.delay -1])          
            deliveryQueue = [] 
            
            # If all processors are "ready", stop interpretation
            b = True
            for m in schedule.processors:
                if working[m][0] != "ready":
                    b = False        
            if b:
                break
            
            # TODO: this is an old workaround used for debugging. Beware.
            if time > 10000:
                print(schedule)
                for v in schedule.program.vertices:
                    print (v.number, " trans ", [v0.number for v0 in schedule.program._trans[v.number]])
                print(schedule.program)
                for m in self.executionTimes.keys():
                    print(m.v.number, self.executionTimes[m])
                print (working)
                print( "Can't calculate time. Possibly an infinite loop occurred")
                import sys
                sys.exit(-1)
        
        for v in self.idletimes:
            if len(schedule.vertices[v[0][0].number]) == v[0][1]:
                v[1] = time - v[1] + 1
        self.idletimes = sorted(self.idletimes, key=lambda x: -x[1])
        # Calculate waiting time for each task
        for m in schedule.processors:
            for v in schedule.vertices[m.number]:
                start = endTimes[v] - v.m.GetTime(v.v.time)
                dep = schedule._dep(v)
                tmp = 0
                for v0 in dep:
                    if start - endTimes[v0] > tmp:
                        tmp = start - endTimes[v0]
                self.delays.append([v, tmp])
        self.delays = sorted(self.delays, key=lambda x: -x[1])
        self.endtimes = endTimes
        return time   
    
    def GetSettings(self):
        # importing here to allow using the class without Qt
        from PyQt4.QtCore import QObject
        class Translator(QObject):
            def __init__(self, parent):
                QObject.__init__(self)
                self.parent = parent
            def getTranslatedSettings(self):
                return [
                [self.tr("Channel bandwidth"), self.parent.bandwidth],
                [self.tr("Delay"), self.parent.delay]
                        ]
        t = Translator(self)
        return t.getTranslatedSettings()

    def UpdateSettings(self, dict):
        # importing here to allow using the class without Qt
        self.bandwidth = dict[0][1]
        self.delay = dict[1][1] 