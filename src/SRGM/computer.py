from math import exp, sqrt, log

class Computer:
    def __init__(self, name):
        f = open(name, "r")
        self.data = f.read()
        self.data = self.data.split(',')
        f.close()
        self.total = 0
        for i in range(0,len(self.data)):
            self.data[i] = int(self.data[i])
        for i in range(1, len(self.data)):
            self.data[i] = self.data[i] - self.data[0] + 1
        self.data[0] = 1
        self.data.insert(0,0)
        self.total = len(self.data)-1
        self.totaltime = self.data[self.total]
        
    def Solve(self, f, a, b):
        k = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fk = f(k)
        if b - a < 0.001:
            return b
        if(fk*fa < 0):
            return self.Solve(f, a, k)
        else:
            return self.Solve(f, k, b)
    def GOfunc(self, x):
        sum = 0
        i = 1
        while i < self.total+1: 
            if i < self.total:
                if self.data[i] != self.data[i+1]:     
                    sum += (self.data[i]*exp(-x*self.data[i]) - self.data[i-1]*exp(-x*self.data[i-1])) / (exp(-x*self.data[i-1]) - exp(-x*self.data[i]))
                    i += 1
                else:
                    k = 1
                    tmp = self.data[i-1]
                    while self.data[i] == self.data[i+1]:
                        k += 1
                        i += 1
                        if i >= self.total - 1:
                            break
                    sum += k * (self.data[i]*exp(-x*self.data[i]) - tmp*exp(-x*tmp)) / (exp(-x*tmp) - exp(-x*self.data[i]))
                    i += 1
            else:
                if self.data[i] == self.data[i-1]:
                    break
                sum += (self.data[i]*exp(-x*self.data[i]) - self.data[i-1]*exp(-x*self.data[i-1])) / (exp(-x*self.data[i-1]) - exp(-x*self.data[i]))
                i += 1     
        sum -= self.totaltime*self.total* exp(-x*self.totaltime) / (1 - exp(-x*self.totaltime))
        return sum
    def GOConfidence(self, b):
        sum = 0
        i = 1
        while i < self.total+1: 
            if i < self.total:
                if self.data[i] != self.data[i+1]:     
                    sum += (self.data[i] - self.data[i-1])**2 * exp(-b*(self.data[i] + self.data[i-1])) / ((exp(-b*self.data[i-1]) - exp(-b*self.data[i]))**2)
                    i += 1
                else:
                    k = 1
                    tmp = self.data[i-1]
                    while self.data[i] == self.data[i+1]:
                        k += 1
                        i += 1
                        if i >= self.total - 1:
                            break
                    sum += k * (self.data[i] - tmp)**2 * exp(-b*(self.data[i] + tmp)) / ((exp(-b*tmp) - exp(-b*self.data[i]))**2)
                    i += 1
            else:
                if self.data[i] == self.data[i-1]:
                    break
                sum += (self.data[i] - self.data[i-1])**2 * exp(-b*(self.data[i] + self.data[i-1])) / ((exp(-b*self.data[i-1]) - exp(-b*self.data[i]))**2)
                i += 1     
        sum -= self.total*self.totaltime*self.totaltime*exp(b*self.totaltime)/((exp(b*self.totaltime)-1)**2)
        bconf = 1.645/sqrt(1)#tmp)
        if b - bconf > 0:
            conf1 = self.total/(1-exp(-(b+bconf)*self.totaltime))
            conf2 = self.total/(1-exp(-(b-bconf)*self.totaltime))
        else:
            conf1 = self.total/(1-exp(-(b+bconf)*self.totaltime))
            conf2 = self.total/(1-exp(-(b)*self.totaltime))
        return conf1, conf2
        
    def GoelOkumoto(self):
        b = self.Solve(self.GOfunc, 0.00001, 0.1)
        n = self.total / (1-exp(-b*self.totaltime))
        tmp = exp(-b*self.totaltime)-(1/n)
        if tmp > 0:
            mttf = -1/b * log(tmp) - self.totaltime
        else:
            mttf = 0
        conf1, conf2 = self.GOConfidence(b)
        #if b == 0.1:
        #    return -2, -2, -2, -2, -2
        return n, b, mttf, conf1, conf2

    def SShapedFunc(self, x):
        i = 1
        sum = self.total*(self.totaltime**2)*exp(-x*self.totaltime)/(1-(1+x*self.totaltime)*exp(-x*self.totaltime))
        while i < self.total+1: 
            if i < self.total:
                if self.data[i] != self.data[i+1]:     
                    tmp = (self.data[i]**2)*exp(-x*self.data[i]) - (self.data[i-1]**2)*exp(-x*self.data[i-1])
                    tmp /= ((1+x*self.data[i-1])*exp(-x*self.data[i-1]) - (1+x*self.data[i])*exp(-x*self.data[i]))
                    sum -= tmp                    
                    i += 1
                else:
                    k = 1
                    tmp = self.data[i-1]
                    while self.data[i] == self.data[i+1]:
                        k += 1
                        i += 1
                        if i >= self.total - 1:
                            break
                    
                    tmp2 = k * (self.data[i]**2)*exp(-x*self.data[i]) - (tmp**2)*exp(-x*tmp)
                    tmp2 /= ((1+x*tmp)*exp(-x*tmp) - (1+x*self.data[i])*exp(-x*self.data[i]))
                    sum -= tmp2
            
                    i += 1
            else:
                if self.data[i] == self.data[i-1]:
                    break
                tmp = (self.data[i]**2)*exp(-x*self.data[i]) - (self.data[i-1]**2)*exp(-x*self.data[i-1])
                tmp /= ((1+x*self.data[i-1])*exp(-x*self.data[i-1]) - (1+x*self.data[i])*exp(-x*self.data[i]))
                sum -= tmp 
                i += 1
        return sum
    
    def SShaped(self):
        b = self.Solve(self.SShapedFunc, 0.000001, 0.01)     
        n = self.total / (1-(1+b*self.totaltime)*exp(-b*self.totaltime))
        f = lambda x: n*(1-(1+b*x)*exp(-b*x))-self.total-1
        mttf = -1
        if n - self.total > 1.0:
            try:
                mttf = self.Solve(f, self.totaltime+0.01, self.totaltime*4.0) - self.totaltime
            except:
                mttf = -1
        return n, b, mttf       
    
    def JMfunc(self, x):
        sum = 0
        for i in range(1, self.total+1 ):     
            sum += 1 / (x - i + 1)
        tmpsum = 0.0
        for i in range(1, self.total+1 ):  
            tmpsum += (i-1)*(self.data[i]-self.data[i-1])
        sum -= self.total / ( x - tmpsum/self.totaltime)
        return sum        
    def JelinskiMoranda(self):
        n = self.Solve(self.JMfunc, self.total+1.0, self.total*2.0)
        tmpsum = 0.0
        for i in range(1, self.total+1 ):  
            tmpsum += (i-1)*(self.data[i]-self.data[i-1])
        phi = self.total / (self.totaltime*n - tmpsum)
        mttf = 1 / (phi*(n - self.total))
        return n, phi, mttf
    
    def LittlewoodVerrall(self):
        def f1(a,b,c):
            res = 1
            for i in range(1, self.total+1):
                res *= (b + c*i)/(self.data[i] - self.data[i-1] + b + c*i)
            res = log(res)
            res += self.total / a
            return res
        def f2(a,b,c):
            res = 0.0
            for i in range(1, self.total+1):
                res += a / (b + c*i) - (a + 1) / (self.data[i] - self.data[i-1] + b + c*i)
            return res
        def f3(a,b,c):
            res = 0
            for i in range(1, self.total+1):
                res += a * i / (b + c*i) - (a + 1) * i / (self.data[i] - self.data[i-1] + b + c*i)            
            return res
        def line(a,b):
            res = sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
            return res
        
        x0 = [0.1,0.1,0.1]
        x1 = [1000.0,1000.0,1000.0]
        square = 10.0
        try:
            while square > 0.01:
                x0[0] = x1[0]
                x0[1] = x1[1]
                x0[2] = x1[2]
                x1[0] = f1(x0[0], x0[1], x0[2])
                x1[1] = f2(x0[0], x0[1], x0[2])
                x1[2] = f3(x0[0], x0[1], x0[2])
                square = x1[0]**2+x1[1]**2+x1[2]**2
                x1[0] += x0[0]
                x1[1] += x0[1]
                x1[2] += x0[2]
        except: #ValueError:
            print("ZERO")
        return -1, (x1[1]+x1[2]*(self.total+1))/(x1[0]-1), x1

    def LogarithmicFunc(self, x):
        sum = 0
        for i in range(1, self.total+1 ):     
            sum += 1/(1 + x*self.data[i])
        sum /= x
        sum -= self.totaltime*self.total / ( (1 + x*self.totaltime) * (log(1 + x*self.totaltime)) )
        return sum
    
    def Logarithmic(self):
        b1 = self.Solve(self.LogarithmicFunc, 0.001, 2)
        b0 = self.total / log(1+b1*self.totaltime)
        tmp = b0*b1/(b1*self.totaltime + 1)
        mttf = 1/tmp
        return b0, b1, mttf
