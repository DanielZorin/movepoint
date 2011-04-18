import math, copy

#Returns factorial of an integer value
def factorial(x):
    if x <= 0:
        return 1
    if x == 1:
        return 1
    return x * factorial(x - 1)

# Solves the equation f(res) = x
def findroot(f, x, a, b):
    k = x
    fa = f(a)
    fb = f(b)
    fk = f(k)
    if b - a < 0.001:
        return b
    if(fk*fa < 0):
        return findroot(f, a, k)
    else:
        return findroot(f, k, b)

def erf(x):
    pass

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

# Calculates error function
def erfinv(x):
    if abs(x) < 0.9:
        a = 0.53728*x**3 + 0.813198*x
    else:
        # An asymptotic formula
        u = math.log(2/math.pi/(abs(x)-1)**2)
        a = sign(x) * math.sqrt(u - math.log(u))/math.sqrt(2)
    return findroot(lambda t: erf(t)-x, a, 0, 100000)

#Returns ordinal number of a given combination
def combinationNumber(b, m):
    n = len(b)
    if n == 0:
        return 0
    if b[n-1] == 0:
        return int(combinationNumber(b[:n-1], m))
    else:
        c = factorial(n-1) / (factorial(m) * factorial(n-1-m))
        return int(c + combinationNumber(b[:n-1], m-1))
    
def getCombinationByNumber(n0, m0, k0):
    n = n0
    m = m0
    k = k0
    #print "<Logic error>", n, m, k
    v = list(range(0, m + 1))
    p = m
    i = 0
    if m == n:
        if k == 1:
            return range(0, m)
        else:
            raise "Wrong combination number"
    while p >= 1:
        i += 1
        if i == k:
            for vi in range(len(v)):
                v[vi] -= 1
            return v[1:]
        if v[m] == n:
            p -= 1
        else:
            p = m
        if p >= 0:
            tmp = list(range(p, m + 1))
            tmp.reverse()
            for j in tmp:
                v[j] = v[p] + j - p + 1
    raise "Wrong combination number"
               
#Compares two solutions in terms of Pareto domination
def Dominates(x, y):
    if (x["cost"] < y["cost"]) and ((x["rel"] - y["rel"]) > 0.000000000000001):
        return True
    if (x["cost"] == y["cost"]) and ((x["rel"] - y["rel"]) > 0.000000000000001):
        return True
    if (x["cost"] < y["cost"]) or (((x["rel"] - y["rel"]) < 0.00000000000001) and ((x["rel"] - y["rel"]) > 0.0)):
        return True    
    # Identical solutions are fine too.
    if (x["cost"] == y["cost"]) or (((x["rel"] - y["rel"]) < 0.00000000000001) and ((x["rel"] - y["rel"]) > 0.0)):
        return True
    else:
        return False
    
def DominatesStrictly(x, y):
    if (x["cost"] < y["cost"]) and ((x["rel"] - y["rel"]) > 0.000000000000001):
        return True 
    else:
        return False

#Checks if any element of x dominates elem
def ExistsDominating(elem, x):
    for x0 in x:
        if Dominates(x0, elem):
            return True
    return False

#Checks if any element of x dominates elem
def ExistsDominatingStrictly(elem, x):
    for x0 in x:
        if DominatesStrictly(x0, elem):
            return True
    return False

# C(X,Y)   
def Cmeasure(x, y):
    top = 0.0
    bottom = float(len(y))
    for elem in y:
        if ExistsDominating(elem, x):
            top += 1.0
    return top / bottom

def LenMeasure(x, y):
    lens = [] 
    for a in x:
        minn = 9000
        for b in y:
            q = math.sqrt( (float(b["cost"]-a["cost"])/100.0)**2 + (b["rel"]-a["rel"])**2)
            if q < minn:
                minn = q
        lens.append(minn)
    return min(lens)/max(lens)

def Vmeasure(x0, y0):
    x = copy.deepcopy(x0)
    y = copy.deepcopy(y0)
    xl = 0
    yl = 0
    c = None
    max = 0.0
    for a in x:
        if a["rel"] > max:
            max = a["rel"]
            c = copy.deepcopy(a)
    del x[x.index(c)]   
    while True:
        if len(x) == 0:
            break
        minn = 9000
        cc = None
        for c0 in x:
            q = math.sqrt( (float(c0["cost"]-c["cost"])/100.0)**2 + (c0["rel"]-c["rel"])**2)
            if q < minn:
                minn = q
                cc = c0
        xl += minn
        del x[x.index(cc)]
        if len(x) == 0:
            break
        c = x[0]
        x = x[1:]
        
    c = None
    max = 0.0
    for a in y:
        if a["rel"] > max:
            max = a["rel"]
            c = copy.deepcopy(a)
    del y[y.index(c)] 
    while True:
        if len(y) == 0:
            break
        minn = 9000
        cc = None
        for c0 in y:
            q = math.sqrt( (float(c0["cost"]-c["cost"])/100.0)**2 + (c0["rel"]-c["rel"])**2)
            if q < minn:
                minn = q
                cc = c0
        yl += minn
        del y[y.index(cc)]
        if len(y) == 0:
            break
        c = y[0]
        y = y[1:]
    return yl / xl