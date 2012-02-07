'''
Created on 09.04.2011

@author: juan
'''

class SRGMTestingWindow(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    # TODO: this is the old implementation of testing
    # It won't work here, but it's left for reference for implementing something better
    def Compare(self):
        #Fills the table of comparison
        try:
            f = open("projects/"+self.currentProject+".log", "rb")
            u = pickle.Unpickler(f)
            log = u.load()
            f.close()
        except:
            log = []
        #log = [-1,-1,-1,-1,-1]
        numbers = []
        a, p, b, a0, a1 = self.computer.GoelOkumoto()
        model = {}
        model["estimate"] = a
        if a == -2:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (a*(1-math.exp(-p*t))/i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[0]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = a / log[0]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        a, p, b = self.computer.JelinskiMoranda()
        model = {}
        model["estimate"] = a
        if a == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (a*(1-math.exp(-p*int(t))) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[1]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = a / log[1]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        a, b, p = -1, -1, [-1, -1, -1]#self.computer.LittlewoodVerrall()
        model = {}
        model["estimate"] = (100*(p[0]-1)**2 - p[1]**2)/(2*p[2]*(p[0]-1))
        if model["estimate"] < 0:
            model["estimate"] = - model["estimate"]
        if b == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += ((p[0]-1)/(4*p[2]*(p[0]-1)) * math.sqrt(2*p[2]*(p[0]-1)*t + p[1]**2) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[2]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = model["estimate"] / log[2]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        #numbers.append({"converge":"no", "accuracy":0, "stability":0, "recommend":"no"})
        a, p, b = self.computer.SShaped()
        model = {}
        model["estimate"] = a
        if a == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (a*(1-(1+p)*math.exp(-p*t)) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[3]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = a / log[3]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        b0, b1, b = self.computer.Logarithmic()
        model = {}
        model["estimate"] = (b0*b1*10 - 1) / b1
        if a == -1:
            model["converge"] = "no"
            model["accuracy"] = 0
            model["stability"] = 0
            model["recommend"] = "no"
        else:
            model["converge"] = "yes"
            i = 0
            sum = 0
            for t in self.computer.data:
                i += 1
                sum += (b0*math.log(t*b1 + 1) / i)**2
            model["accuracy"] = sum / i
            if log == []:
                model["stability"] = 1
            else:
                if log[4]["estimate"] == -1:
                    model["stability"] = 1
                else:
                    model["stability"] = model["estimate"] / log[4]["estimate"]
            if model["accuracy"] < 0.81 or model["accuracy"] > 1.21:
                model["recommend"] = "no"
            else:
                if model["stability"] > 0.9 and model["stability"] < 1.1:
                    model["recommend"] = "yes"
                else:
                    model["recommend"] = "no"
        numbers.append(model)
        f = open("projects/"+self.currentProject+".log", "wb")
        p = pickle.Pickler(f)
        p.dump(numbers)
        f.close()
        self.ui.tableWidget.setItem(0,0, QtGui.QTableWidgetItem(numbers[0]["converge"]))
        self.ui.tableWidget.setItem(0,1, QtGui.QTableWidgetItem(numbers[1]["converge"]))
        self.ui.tableWidget.setItem(0,2, QtGui.QTableWidgetItem(numbers[2]["converge"]))
        self.ui.tableWidget.setItem(0,3, QtGui.QTableWidgetItem(numbers[3]["converge"]))
        self.ui.tableWidget.setItem(0,4, QtGui.QTableWidgetItem(numbers[4]["converge"]))
        self.ui.tableWidget.setItem(1,0, QtGui.QTableWidgetItem(str(numbers[0]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,1, QtGui.QTableWidgetItem(str(numbers[1]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,2, QtGui.QTableWidgetItem(str(numbers[2]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,3, QtGui.QTableWidgetItem(str(numbers[3]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(1,4, QtGui.QTableWidgetItem(str(numbers[4]["accuracy"])[:6]))
        self.ui.tableWidget.setItem(2,0, QtGui.QTableWidgetItem(str(numbers[0]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,1, QtGui.QTableWidgetItem(str(numbers[1]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,2, QtGui.QTableWidgetItem(str(numbers[2]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,3, QtGui.QTableWidgetItem(str(numbers[3]["stability"])[:6]))
        self.ui.tableWidget.setItem(2,4, QtGui.QTableWidgetItem(str(numbers[4]["stability"])[:6]))
        self.ui.tableWidget.setItem(3,0, QtGui.QTableWidgetItem(numbers[0]["recommend"]))
        self.ui.tableWidget.setItem(3,1, QtGui.QTableWidgetItem(numbers[1]["recommend"]))
        self.ui.tableWidget.setItem(3,2, QtGui.QTableWidgetItem(numbers[2]["recommend"]))
        self.ui.tableWidget.setItem(3,3, QtGui.QTableWidgetItem(numbers[3]["recommend"]))
        self.ui.tableWidget.setItem(3,4, QtGui.QTableWidgetItem(numbers[4]["recommend"]))
        