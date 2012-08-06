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
import xml.dom.minidom

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
    
    def Consistency(self):
        # TODO: super beedlowcode
        for m in self.vertices.keys():
            for s in self.vertices[m]:
                self.currentVersions[s.v.number] = [s] 
               
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
        root = dom.createElement("schedule")
        dom.appendChild(root)
        for p in self.vertices.keys():
            proc = dom.createElement("processor")
            proc.setAttribute("reserves", str(self.GetProcessor(p).reserves))
            i = 1
            for v in self.vertices[p]:
                vert = dom.createElement("task")
                vert.setAttribute("id", str(v.v.number))
                vert.setAttribute("version", str(v.k.number))
                vert.setAttribute("position", str(i))
                proc.appendChild(vert)
                i += 1
            root.appendChild(proc)
        return dom.toprettyxml()
    
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
    def Interpret(self):
        return 100
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
        '''Moves a :class:`~Schedules.ScheduleVertex.ScheduleVertex` s1 to position n on processor m 
        
         :return: True if the operation is possible. String with the description of error otherwise'''

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