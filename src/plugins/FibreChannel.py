class FibreChannelInterpreter:
    idletimes = []
    delays = []
    endtimes = []
    
    # These arrays are filled during the interpretation.
    # This data is used for fast drawing of the schedule in GUI.
    executionTimes = {}
    deliveryTimes = []

    def __init__(self):
        pass

    def GetName():
        return "Fibre Channel"

    def Interpret(self, schedule):
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
        # Status of the port of each processor (busy=True/ready=False)
        portStatus = {}
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
            portStatus[m] = False
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
            # Print debug information
            '''
            print("Time = ", time)
            for m in schedule.processors:
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
                        self.idletimes.append([sortedTasks[m][0],delays[sortedTasks[m][0]]])
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
            for m in schedule.processors:
                if working[m][0] != "ready":
                    b = False        
            if b:
                break
            
            # TODO: this is an old workaround used for debugging. Beware.
            if time > 10000:
                print(self)
                raise "Can't calculate time. Possibly an infinite loop occurred"
        
        self.idletimes = sorted(self.idletimes, key=lambda x: x[1])
        # Calculate waiting time for each task
        for m in schedule.processors:
            for v in schedule.vertices[m.number]:
                start = endTimes[v] - v.m.GetTime(v.v.time)
                dep = self._dep(v)
                tmp = 0
                for v0 in dep:
                    if start - endTimes[v0] > tmp:
                        tmp = start - endTimes[v0]
                self.delays.append([v, tmp])
        self.delays = sorted(self.delays, key=lambda x: x[1])
        self.endtimes = endTimes
        return time

def pluginMain():
    return FibreChannelInterpreter