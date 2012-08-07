# TODO: make it working
class SimpleInterpreter:
    idletimes = []
    delays = []
    endtimes = []
    
    # These arrays are filled during the interpretation.
    # This data is used for fast drawing of the schedule in GUI.
    executionTimes = {}
    deliveryTimes = []

    def __init__(self):
        pass

    def GetName(self):
        return "Default"

    def Interpret(self, schedule):
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
        
        return 0
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
    