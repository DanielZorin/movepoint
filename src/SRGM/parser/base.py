import cPickle
import xml.dom.minidom

def Parse(date):
    y = int(date[0:4])
    m = int(date[5:7])
    d = int(date[8:10])
    return y, m, d

def DivideDates(a,b):
    y1, m1, d1 = Parse(a)
    y2, m2, d2 = Parse(b)
    months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    sum = 0
    if y1 != y2:
        sum += months[m1] - d1
        for i in range(m1+1, 13):
            sum += months[i]
        if y1 + 1 != y2:
            for i in range(y1+1, y2):
                sum += 365
        for i in range(1, m2):
            sum += months[i]
        sum += d2
    else:
        if m1 != m2:
            sum += months[m1] - d1
            for i in range(m1+1, m2):
                sum += months[i]
            sum += d2
        else:
            sum += d2 - d1
    return sum

def ToXml(lst):
    projects = []
    dates = []
    severity = {}
    items = {}
    i = 0
    for error in lst:
        if not error["product"] in projects:
            projects.append(error["product"])
        if not severity.has_key(error["severity"]):
            severity[error["severity"]] = len(severity) + 1
        if not items.has_key(error["component"]):
            items[error["component"]] = len(items) + 1  
        dates.append(error["date"])
        i += 1
        print i
    print severity
    dates.sort()
    i = 0
    while dates[i] == '':
        i += 1
    starttime = dates[i+1]
    print starttime, dates
    #print items  
    return
    for p in projects:
        if p != "":
            dom = xml.dom.minidom.Document()
            root = dom.createElement("errors")
            dom.appendChild(root)
            for error in lst:
                if error["product"] == p and error["date"] != '':
                    #print error
                    node = dom.createElement("error")
                    time = dom.createElement("time")
                    time.appendChild(dom.createTextNode( str(DivideDates(starttime, error["date"])+1) ))
                    severitynode = dom.createElement("severity")
                    severitynode.appendChild(dom.createTextNode(str(severity[error["severity"]])))
                    itemnode = dom.createElement("item")
                    itemnode.appendChild(dom.createTextNode(str(items[error["component"]])))
                    node.appendChild(time)
                    node.appendChild(severitynode)
                    node.appendChild(itemnode)
                    root.appendChild(node)     
            f = file(p+".xml", "w")
            dom.writexml(f)
            f.close()
            print p

f = file("eclipse.txt", "r")
u = cPickle.Unpickler(f)
lst = u.load()
ToXml(lst)
#print Parse("2005-12-23")