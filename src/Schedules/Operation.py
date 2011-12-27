class VoidOperation:
    pass

class AddProcessor:
    def __init__(self, proc):
        self.processor = proc
        
    def Reverse(self):
        return DeleteProcessor(self.processor)

class DeleteProcessor:
    def __init__(self, proc):
        self.processor = proc

    def Reverse(self):
        return AddProcessor(self.processor)

class AddVersion:
    def __init__(self, task, proc1, pos1, proc2, pos2):
        self.task = task
        self.pos1 = (proc1, pos1)
        self.pos2 = (proc2, pos2)
        
    def Reverse(self):
        return DeleteVersion(self.task, self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])

class DeleteVersion:
    def __init__(self, task, proc1, pos1, proc2, pos2):
        self.task = task
        self.pos1 = (proc1, pos1)
        self.pos2 = (proc2, pos2)

    def Reverse(self):
        return AddVersion(self.task, self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])

class MoveVertex:
    # TODO: flag indicating processor deletion
    def __init__(self, task, proc1, pos1, proc2, pos2):
        self.task = task
        self.pos1 = (proc1, pos1)
        self.pos2 = (proc2, pos2)
        
    def Reverse(self):
        return MoveVertex(self.task, self.pos2[0], self.pos2[1], self.pos1[0], self.pos1[1])
    
    def __str__(self):
        return str(self.task) + str(self.pos1[0]) + str(self.pos1[1]) + str(self.pos2[0]) + str(self.pos2[1])
    
class MultiOperation:
    def __init__(self):
        self.ops = []
    def Add(self, op):
        self.ops.append(op)
    def Reverse(self):
        res = []
        for op in self.ops:
            res = [op.Reverse()] + res
        return res

class Trace:
    def __init__(self):
        self.ops = []
        self.best = -1
        self.current = -1

    def addStep(self, op, params):
        self.ops.append((op, params))
        self.current = self.length() - 1
        
    def setBest(self, i):
        # TODO: check boundaries
        self.best = i

    def getBest(self):
        if self.best != -1:
            return self.ops[self.best]

    def getLast(self):
        return self.ops[len(self.ops) - 1]

    def getCurrent(self):
        return self.ops[self.current]

    def length(self):
        return len(self.ops)

    def clear(self):
        self.ops = []
