import pickle
#s = {"a":"t", "t":[7,8]}
f = open("settings.txt", "wb")
#f.write(str(s))
s = {"current":"test", 
     "list":[{"name":"test", 
              "models":["Goel-Okumoto", "Jelinski-Moranda"], 
              "file":"projects/test.txt"}]
     }
p = pickle.Pickler(f)
pickle.dump(s, f)
print (s)
f.close()
