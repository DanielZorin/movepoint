f = open("final_results.txt", "r")
lines = f.readlines()
f.close()
results = {}
for s in lines:
	parts = s.split(";")
	if not parts[0] in results.keys():
		results[parts[0]] = {}
	if not (int(parts[1]), int(parts[3])) in results[parts[0]].keys():
		results[parts[0]][(int(parts[1]), int(parts[3]))] = []
	if int(parts[4]) < int(parts[1]):
		results[parts[0]][(int(parts[1]), int(parts[3]))].append(int(parts[4]))
f = open("final_results_parsed.txt", "w")
for test in results.keys():
	s = test + "\n---;s1;s2;s3;s0\n"
	sizes = sorted(list(set(v[0] for v in results[test].keys())))
	res = []
	def avg(x):
		return sum(x) / len(x)
	for i in sizes:
		res.append([i, avg(results[test][(i, 0)]), avg(results[test][(i, 1)]), avg(results[test][(i, 2)]), avg(results[test][(i, 3)])])
	for r in res:
		s += ';'.join([str(x) for x in r]) + "\n"
	f.write(s.replace(".", ","))
f.close()

f = open("results_parallel.txt", "r")
lines = f.readlines()
f.close()
results = {0:{}, 1:{}, 2:{}}
for s in lines:
	parts = s.split(";")
	if not (int(parts[0]), int(parts[3])) in results[int(parts[2])].keys():
		results[int(parts[2])][(int(parts[0]), int(parts[3]))] = []
	if int(parts[4]) < int(parts[0]):
		results[int(parts[2])][(int(parts[0]), int(parts[3]))].append(int(parts[4]))
f = open("results_parallel_parsed.txt", "w")
for test in results.keys():
	s = "s" + str(test) + "\n---;1;3;5;7\n"
	sizes = sorted(list(set(v[0] for v in results[test].keys())))
	res = []
	def avg(x):
		return sum(x) / len(x)
	for i in sizes:
		res.append([i, avg(results[test][(i, 1)]), avg(results[test][(i, 3)]), avg(results[test][(i, 5)]), avg(results[test][(i, 7)])])
	for r in res:
		s += ';'.join([str(x) for x in r]) + "\n"
	f.write(s.replace(".", ","))
f.close()

f = open("results_antenna.txt", "r")
lines = f.readlines()
f.close()
results = {}
for s in lines:
	parts = s.split(";")
	if not parts[0] in results.keys():
		results[parts[0]] = {}
	key = (int(parts[1]), int(parts[2]))
	if not key in results[parts[0]]:
		results[parts[0]][key] = []
	results[parts[0]][key].append(float(parts[4]))
f = open("results_antenna_parsed.txt", "w")
for test in results.keys():
	s = test + "\n---;m=1;m=2;m=3\n"
	sizes = sorted(list(set(v[0] for v in results[test].keys())))
	res = []
	res = []
	def avg(x):
		return sum(x) / len(x)
	for i in sizes:
		res.append([i, avg(results[test][(i, 1)]), avg(results[test][(i, 2)]), avg(results[test][(i, 3)])])
	for r in res:
		s += ';'.join([str(x) for x in r]) + "\n"
	f.write(s.replace(".", ","))
f.close()