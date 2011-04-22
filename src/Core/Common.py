import math, copy

def factorial(x):
    '''Returns factorial of an integer value'''
    if x <= 0:
        return 1
    if x == 1:
        return 1
    return x * factorial(x - 1)

def findroot(f, a, b, eps=0.001):
    ''' Solves the equation f(z) = x with dichotomy method 
    assuming that the root is in [a,b] with precision eps'''
    k = (a + b) / 2
    fa = f(a)
    fk = f(k)
    if b - a < eps:
        return b
    if(fk*fa < 0):
        return findroot(f, a, k, eps)
    else:
        return findroot(f, k, b, eps)

def sign(x):
    ''' Returns sign of x '''
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def combinationNumber(b, m):
    ''' Returns the ordinal number of a given combination
    
    :param b: A list of numbers from 1 to m
    :param m: Maximal number in the combination
    
    Assume m=5, n=2. Then all combinations C(m,n) can be sorted "alphabetically", i.e. (2,3) will precede
    (2,4), (1,3) will precede (2,1) and so on. This function returns the number of a given combination.
    n isn't passed explicitly because it's the length of b'''
    n = len(b)
    if n == 0:
        return 0
    if b[n-1] == 0:
        return int(combinationNumber(b[:n-1], m))
    else:
        c = factorial(n-1) / (factorial(m) * factorial(n-1-m))
        return int(c + combinationNumber(b[:n-1], m-1))
    
def getCombinationByNumber(n0, m0, k0):
    ''' Finds k0 combination among all combinations C(n0, m0) sorted alphabetically.'''
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
               
def Dominates(x, y):
    ''' Compares two solutions in terms of Pareto domination. x and y are dictionaries "cost"->int, "rel"->float
    If x and y are equal, this function returns True.
    
    .. warning:: the implementation is unstable'''
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
    ''' Compares two solutions in terms of Pareto domination. x and y are dictionaries "cost"->int, "rel"->float
    If x and y are equal, this function returns False.
    
    .. warning:: the implementation is unstable'''
    if (x["cost"] < y["cost"]) and ((x["rel"] - y["rel"]) > 0.000000000000001):
        return True 
    else:
        return False

def ExistsDominating(elem, x):
    '''Checks if any element of x dominates elem or is equal to elem'''
    for x0 in x:
        if Dominates(x0, elem):
            return True
    return False

def ExistsDominatingStrictly(elem, x):
    ''' Checks if any element of x dominates elem'''
    for x0 in x:
        if DominatesStrictly(x0, elem):
            return True
    return False
  
def Cmeasure(x, y):
    ''' C(X,Y) '''
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