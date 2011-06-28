from mechanize import Browser
import urllib, cPickle, pickle


def GetBug(n):
    firefox = Browser()
    firefox.set_handle_robots(False)
    firefox.addheaders[:0] = [["User-agent", "Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9) Gecko/2008062113 Iceweasel/3.0 (Debian-3.0~rc2-1) "]]
    while True:
        try:
            resp = firefox.open("http://bugs.eclipse.org/bugs/show_bug.cgi?id="+str(n))
            break
        except:
            pass
    #try:
    #    resp = urllib.urlopen("http://bugs.eclipse.org/"+str(n)).read()
    #except:
    #    pass
    result = {}
    result["number"] = n
    s = resp.read()
    #s = resp
    n = s.find("<input type=\"hidden\" id=\"product\" name=\"product\"")
    s = s[n:]
    n = s.find("value")
    s = s[n+7:]
    n = s.find("\"")
    result["product"] = s[:n]
    n = s.find("<input type=\"hidden\" id=\"component\" name=\"component\"")
    s = s[n:]
    n = s.find("value")
    s = s[n+7:]
    n = s.find("\"")
    result["component"] = s[:n]
    n = s.find("<a href=\"page.cgi?id=fields.html#status\">")
    s = s[n:]
    n = s.find("<td>")
    s = s[n+4:]
    n = s.find("<")
    result["status"] = s[:n]
    n = s.find("<a href=\"page.cgi?id=fields.html#resolution\">")
    s = s[n:]
    n = s.find("<td>")
    s = s[n+4:]
    n = s.find("<")
    result["resolution"] = s[:n]
    n = s.find("<input type=\"hidden\" id=\"bug_severity\" name=\"bug_severity\"")
    s = s[n:]
    n = s.find("value")
    s = s[n+7:]
    n = s.find("\"")
    result["severity"] = s[:n]
    n = s.find("<b>Opened:</b>")
    s = s[n:]
    n = s.find("</b>")
    s = s[n+5:]
    result["date"] = s[:10]
    print result
    return result
#5946
f = file("base2.txt", "r")
u = pickle.Unpickler(f)
lst = u.load()  
f.close()  
"""for i in range(5947,10000): 
    lst.append(GetBug(i))
    f = file("base2.txt", "w")
    p = cPickle.Pickler(f)
    p.dump(lst)
    f.close() """
    