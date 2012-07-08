from Systems.PointSystem import PointSystem
from Systems.Point import Point, Software, Method
from Core.Hardware import Hardware
import random


class SystemGenerator:
    ''' Generator a random :class:`~Systems.PointSystem.PointSystem` object
    
    :param size: Number of points
    :param soft: Average number of software components in a point
    :param hard: Average number of hardware components in a point'''
    
    def __init__(self, size = 5, soft = 4, hard = 4):
        self.size = size
        if soft >= 3:
            self.soft = soft
        else:
            self.soft = 3
        if hard >= 2:
            self.hard = hard
        else:
            self.hard = 2
        self.methods = []
        self.methods.append(Method("none", 1, 1))
        self.methods.append(Method("nvp/0/1", 1, 3))
        self.methods.append(Method("nvp/1/1", 1, 3))
        self.methods.append(Method("rb/1/1", 2, 2))
        
    def Generate(self):
        ''' Generates the system
        
        .. warning:: the implementation of random variables is weird'''
        res = PointSystem()
        for i in range(self.size):
            p = Point("generated point")
            n = random.randint(1,4)
            for j in range(n):
                k = random.randint(0,3)
                if not (self.methods[k] in p.methods):
                    p.methods.append(self.methods[k])
            res.points.append(p)
            for j in range(2):
                new = Hardware(random.random(), random.random(), random.randint(5,100), "generated")
                p.hardware.append(new)
            for j in range(3):
                new = Software(random.random(), random.random(), random.randint(5,100), "generated")
                p.software.append(new)
            for j in range(self.soft - 3):
                coin = random.random()
                if coin > 0.5:
                    new = Software(random.random(), random.random(), random.randint(5,100), "generated")
                    p.software.append(new)
            for j in range(self.hard - 2):
                coin = random.random()
                if coin > 0.5:
                    new = Hardware(random.random(), random.random(), random.randint(5,100), "generated")
                    p.hardware.append(new)
            p.FixData()
        res._default()
        return res