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
import xml.dom.minidom, random

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

    def ExportXml(self):
        dom = xml.dom.minidom.Document()
        root = dom.createElement("system")
        root.setAttribute("rt", "0")
        dom.appendChild(root)
        for p in self.vertices.keys():
            proc = dom.createElement("processor")
            proc.setAttribute("reserves", str(self.GetProcessor(p).reserves))
            proc.setAttribute("id", "processor_" + str(p))
            i = 1
            for v in self.vertices[p]:
                vert = dom.createElement("task")
                vert.setAttribute("id", "task_" + str(v.v.number) + "_version_" + str(v.k.number))
                vert.setAttribute("time", str(v.v.time))
                vert.setAttribute("dirtime", str(v.v.time))
                vert.setAttribute("num", str(i))
                vert.setAttribute("link", "nolink")
                datavol = 0
                succ = self.program.FindAllEdges(v.v, None)
                if len(succ) > 0:
                    datavol = succ[0].volume
                vert.setAttribute("datavol", str(datavol))
                prev = self._dep(v)
                next = []
                for fol in [fol.destination for fol in self.program.FindAllEdges(v.v, None)]:
                    next += self.currentVersions[fol.number]

                for x in prev:
                    previtem = dom.createElement("prev")
                    previtem.setAttribute("id", "task_" + str(x.v.number) + "_version_" + str(x.k.number))
                    vert.appendChild(previtem)

                for x in next:
                    nextitem = dom.createElement("next")
                    nextitem.setAttribute("id", "task_" + str(x.v.number) + "_version_" + str(x.k.number))
                    vert.appendChild(nextitem)
                proc.appendChild(vert)
                i += 1
            root.appendChild(proc)
        return dom.toprettyxml()

    def ExportCode(self):
        res = ""
        for k in self.vertices.keys():
            proc = "// Processor " + str(k) + ": \n\n"
            for v in self.vertices[k]:
                proc += "// Task " + str(v.v.number) + "\n"
                for e in self.program.edges:
                    if e.source == v.v:
                        for m in self.vertices.keys():
                            if m != k:
                                for v2 in self.vertices[m]:
                                    if v2.v == e.destination:
                                        proc += "MPI_SEND(" + str(m) + ", result);\n" 
            res += proc
        return res
    
    def SetToDefault(self, limits=[]):    
        ''' Places each vertex on a new processor'''
        self.vertices = {}
        self.processors = []
        self.emptyprocessors = []
        special = []
        for l in limits:
            if l[2] == ">":
                special.append(l[0])
                special.append(l[1])

        for v in self.program.vertices:
            if not (v.number in special):
                p = self._getProcessor()
                s = ScheduleVertex(v, v.versions[0], p)
                self.vertices[p.number] = [s]
                self.currentVersions[v.number] = [s]

        if not limits:
            return

        sets = []
        for l in limits:
            if l[2] == ">":
                found = False
                for s in sets:
                    if (l[0] in s) or (l[1] in s):
                        s.add(l[0])
                        s.add(l[1])
                        found = True
                if not found:
                    s = set([l[1], l[0]])
                    sets.append(s)
        def comp(a, b):
            for l in limits:
                if l[2] == ">":
                    if (l[0] == a) and (l[1] == b):
                        return 1
                    elif (l[1] == a) and (l[0] == b):
                        return -1
            return 0

        def cmp2key(mycmp):
            class K:
                def __init__(self, obj, *args):
                    self.obj = obj
                def __lt__(self, other):
                    return mycmp(self.obj, other.obj) < 0
                def __gt__(self, other):
                    return mycmp(self.obj, other.obj) > 0
                def __eq__(self, other):
                    return mycmp(self.obj, other.obj) == 0
                def __le__(self, other):
                    return mycmp(self.obj, other.obj) <= 0
                def __ge__(self, other):
                    return mycmp(self.obj, other.obj) >= 0
                def __ne__(self, other):
                    return mycmp(self.obj, other.obj) != 0
            return K
        for s in sets:
            res = list(s)
            res.sort(key=cmp2key(lambda x, y: comp(x, y)))
            p = self._getProcessor()
            self.vertices[p.number] = []
            for r in res:
                for v in self.program.vertices:
                    if v.number == r:
                        v0 = v
                s = ScheduleVertex(v0, v0.versions[0], p)
                self.vertices[p.number].append(s)
                self.currentVersions[v0.number]= [s]
                        

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
        if not p.number in self.vertices:
            return
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

    def _next(self, s):
        dep = {}
        for e in self.program._next[s.v.number]:
            dep[e] = self.currentVersions[e.destination.number]
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
     
    def FindAllVertices(self, v = None, k = None, vid = None):
        ''' Returns a list of vertices satisfying the given mask.
        "None" stands for any value'''
        res = []
        for m in self.vertices.keys():
            for t in self.vertices[m]:
                if (v is None) or (t.v == v):
                    if (k is None) or (t.k == k):
                        if (vid is None) or (t.v.number == vid):
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
        elif isinstance(op, Replacement):
            self.Deserialize(op.new)
            self.Consistency()
    
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
        if not p1 or not p1.number in self.vertices.keys():
            p = self._getProcessor()
            s1 = ScheduleVertex(v, totalver[len(curver)], p)
            s2 = ScheduleVertex(v, totalver[len(curver)+1], p)
            self.vertices[p.number] = [s1, s2]
        else:
            p = p1
            s1 = ScheduleVertex(v, totalver[len(curver)], p1)      
            self.vertices[p1.number] = [s1]
            if not p2 or not p2.number in self.vertices.keys():
                p2 = self._getProcessor()
                s2 = ScheduleVertex(v, totalver[len(curver)+1], p2)
                self.vertices[p2.number] = [s2]
            else:
                s2 = ScheduleVertex(v, totalver[len(curver)+1], p2)
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
            self.vertices[s.m.number].insert(n2, s)
            return True
        else:
        #Different processors
            del self.vertices[s.m.number][n1]
            self.vertices[m2.number].insert(n2, s)
            self._delEmptyProc(s.m)
            s.m = m2
            return True
       
    def TryMoveVertex(self, s, n1, m2, n2, limits=[]):
        '''Moves a :class:`~Schedules.ScheduleVertex.ScheduleVertex` s1 to position n on processor m 
        
        :return: True if the operation is possible. String with the description of error otherwise'''

        for limit in limits:
            v1 = limit[0]
            v2 = limit[1]
            c = limit[2]
            if (s.v.number != v1) and (s.v.number != v2):
                continue
            if s.v.number == v1:
                other = v2
            else:
                other = v1
            verts = self.FindAllVertices(vid=other)
            for v in verts:
                if c == "=":
                    if v.m == m2:
                        return False
                if (c == ">") or (c == "<"):
                    if v.m != m2:
                        return False
                    if (c == ">") and (other == v2) and self.vertices[v.m.number].index(v) < n2:
                        return False
                    if (c == ">") and (other == v1) and self.vertices[v.m.number].index(v) > n2:
                        return False
                    if (c == "<") and (other == v2) and self.vertices[v.m.number].index(v) > n2:
                        return False
                    if (c == "<") and (other == v1) and self.vertices[v.m.number].index(v) < n2:
                        return False
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
                    return str(s2.v.number) + " depends on " + str(s.v.number)
                else:
                    return True
            else:
            #Move backward
                after_s2 = self.vertices[s.m.number][n2:n1]
                for v in after_s2:
                    if s in self._succ(v):
                        return str(s.v.number) + " depends on " + str(v.v.number)
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
                    return str(v.v.number) + " depends on " + str(s.v.number)
            for v in other_proc[n2:]:
                if s in self._succ(v):
                    return str(s.v.number) + " depends on " + str(v.v.number)
            return True
        
    def CanDeleteProcessor(self):
        ''':return: True if there is at least one processor with at least one reserve'''
        for m in self.processors:
            if m.reserves > 1:
                return True
        return False
    
    def CanDeleteAnyVersions(self):
        ''':return: True if there is at least one task with more than one version '''
        for v0 in self.vertices.values():
            for v in v0:
                if v.k.number > 1:
                    return True
        return False
    
    def CanAddAnyVersions(self):
        ''':return: True if there is at least one task with two available unused versions'''
        for v in self.program.vertices:
            cur = self.currentVersions[v.number]
            if len(v.versions) >= len(cur) + 2:
                return True
        return False

    def CanDeleteVersions(self, v):
        ''':return: True if there is at least one task with more than one version '''
        cur = self.currentVersions[v.v.number]
        if len(cur) >= 2:
            return True
        return False
    
    def CanAddVersions(self, v):
        ''':return: True if there is at least one task with two available unused versions'''
        cur = self.currentVersions[v.v.number]
        if len(v.v.versions) >= len(cur) + 2:
            return True
        return False

    ''' Auxiliary functions for genetic algorithm '''
    def Randomize(self):
        '''Make a random schedule'''
        #TODO: randomize versions and processors too
        self.vertices = {}
        self.processors = []
        self.emptyprocessors = []
        count = random.randint(1, len(self.program.vertices))
        keys = []
        procs = {}
        for i in range(count):
            p = self._getProcessor()
            self.vertices[p.number] = []
            keys.append(p.number)
            procs[p.number] = p

        # Use fictional processor number -1 to check correctness of the schedule.
        fict = Processor(-1)
        self.vertices[-1] = []
        verts = self.program.OrderedVertices()
        backup = [[v for v in self.program.vertices], [e for e in self.program.edges]]
        self.program.vertices = []
        self.program.edges = []
        for v in verts:
            self.program.vertices.append(v)
            self.program.edges = []
            for e in backup[1]:
                if e.source in self.program.vertices and e.destination in self.program.vertices:
                    self.program.edges.append(e)
            self.program._buildData()
            s = ScheduleVertex(v, v.versions[0], fict)
            self.currentVersions[v.number] = [s]
            self.vertices[-1] = [s]
            self._succCache = {}
            while True:
                m = random.randint(1, count)
                n = random.randint(0, len(self.vertices[m]))
                if self.TryMoveVertex(s, 0, procs[m], n) == True:
                    self.MoveVertex(s, 0, procs[m], n)
                    break
        for m in self.processors:
            self._delEmptyProc(m)

    def ReplaceProcessor(self, tasks):
        ''' Replaces the list of vertices on some processor with tasks, moving other vertices accordingly. 
        Used for crossover in genetic algorithm.'''
        oldverts = self.vertices
        ordered = self.program.OrderedVertices()
        self.processors = []
        self.emptyprocessors = []
        self.vertices = {}
        self.currentVersions = {}
        p = self._getProcessor()
        self.vertices[p.number] = []
        backup = [[v for v in self.program.vertices], [e for e in self.program.edges]]
        self.program._buildData()
        #self.program.vertices = []
        #self.program.edges = []
        for t in tasks:
            s = ScheduleVertex(t.v, t.v.versions[0], p)
            self.vertices[p.number].append(s)
            self.currentVersions[t.v.number] = [s]
        for v in self.program.vertices:
            if not v.number in self.currentVersions:
                self.currentVersions[v.number] = []
        #    self.program.vertices.append(t.v)
        self.Consistency()
        #for e in backup[1]:
        #    if e.source in self.program.vertices and e.destination in self.program.vertices:
        #        self.program.edges.append(e)

        fict = Processor(-1)
        spare = self._getProcessor()
        self.vertices[-1] = []
        self.vertices[spare.number] = []
        newprocs = {}
        allverts = []
        for m in oldverts.keys():
            allverts += oldverts[m]
        for vp in ordered:
            for v in [t for t in allverts if t.v == vp]:
                if [t for t in tasks if t.v == v.v] == []:
                    if v.m in newprocs:
                        p = newprocs[v.m]
                    else:
                        p = self._getProcessor()
                        self.vertices[p.number] = []
                        newprocs[v.m] = p
                    i = oldverts[v.m].index(v)
                    #self.program.vertices.append(v.v)
                    #self.program.edges = []
                    #for e in backup[1]:
                    #    if e.source in self.program.vertices and e.destination in self.program.vertices:
                    #        self.program.edges.append(e)
                    #self.program._buildData()
                    s = ScheduleVertex(v.v, v.v.versions[0], fict)
                    self.currentVersions[v.v.number] = [s]
                    self.vertices[-1] = [s]
                    self._succCache = {}
                    if self.TryMoveVertex(s, 0, p, i) == True:
                        #print ("Applying operation 1", str(s), 0, p, i)
                        self.MoveVertex(s, 0, p, i)                      
                    else:
                        if len(self.vertices[spare.number]) == 0:
                            #print ("Applying operation 2", str(s), 0, spare, 0)
                            self.MoveVertex(s, 0, spare, 0)
                        else:
                            for j in range(len(self.vertices[spare.number]) + 1):
                                if self.TryMoveVertex(s, 0, spare, j) == True:
                                    #print ("Applying operation 3", str(s), 0, spare, j)
                                    self.MoveVertex(s, 0, spare, j)
                                    break
                    self.emptyprocessors = []
                    #print(self)
                    #print("++++++++++++")
        for m in self.processors:
            self._delEmptyProc(m)
        self.Consistency()

    def Serialize(self):
        self.Consistency()
        return [self.vertices, self.processors, self.emptyprocessors, self.currentVersions]

    def Deserialize(self, d):
        self.vertices = d[0]
        self.processors = d[1]
        self.emptyprocessors = d[2]
        self.currentVersions = d[3]
        self.Consistency()

    def Consistency(self):
        # TODO: super beedlowcode
        for m in self.vertices.keys():
            for s in self.vertices[m]:
                self.currentVersions[s.v.number] = [s]
        for m in self.processors:
            self._delEmptyProc(m)
        proc = []
        for m in self.processors:
            if m.number in self.vertices:
                proc.append(m)
        self.processors = proc  
        keys = [k for k in self.vertices.keys()]
        for m in keys:
            if len(self.vertices[m]) == 0:
                del self.vertices[m]
