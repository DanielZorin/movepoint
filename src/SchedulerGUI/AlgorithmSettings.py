from PyQt4.QtCore import QObject

class AlgorithmSettings(QObject):
    def __init__(self):
        QObject.__init__(self)

    def GetAnnealingSettings(self, method, algorithm):
        return [
        [self.tr("Number of iterations"), method.numberOfIterations],
        [self.tr("Strategy"), algorithm.strategies],
        [self.tr("Temperature function"), algorithm.threshold],
        [self.tr("Raise temperature"), algorithm.raiseTemperature],
        [self.tr("Vertices limit"), algorithm.choice_vertices],
        [self.tr("Positions limit"), algorithm.choice_places],
        [self.tr("Operation probabilities: optimize reliability"), 
            {self.tr("Deadline not violated"): algorithm.opt_reliability["time-normal"],
             self.tr("Deadline violated"): algorithm.opt_reliability["time-exceed"]}],
        [self.tr("Operation probabilities: optimize time"), 
            {self.tr("Deadline not violated"): algorithm.opt_time["time-normal"],
             self.tr("Deadline violated"): algorithm.opt_time["time-exceed"]}]]
        
    def UpdateAnnealingSettings(self, dict, method, algorithm):
        '''Deserializes the class from a dictionary of parameters'''
        algorithm.opt_reliability["time-normal"] = dict[6][1][self.tr("Deadline not violated")]
        algorithm.opt_reliability["time-exceed"] = dict[6][1][self.tr("Deadline violated")]
        algorithm.opt_time["time-normal"] = dict[7][1][self.tr("Deadline not violated")]
        algorithm.opt_time["time-exceed"] = dict[7][1][self.tr("Deadline violated")]
        algorithm.choice_vertices = dict[4][1]
        algorithm.choice_places = dict[5][1]
        algorithm.strategies = dict[1][1]
        algorithm.threshold = dict[2][1]
        algorithm.raiseTemperature = dict[3][1]
        method.numberOfIterations = dict[0][1]

    def GetGeneticsSettings(self, method, algorithm):
        return [
        [self.tr("Number of iterations"), method.numberOfIterations]
                ]
        
    def UpdateGeneticsSettings(self, dict, method, algorithm):
        method.numberOfIterations = dict[0][1]

    def GetMethodSettings(self, project):
        if project.UsesAnnealing():
            return self.GetAnnealingSettings(project.method, project.method.algorithm)
        else:
            return self.GetGeneticsSettings(project.method, project.method.algorithm)

    def UpdateMethodSettings(self, dict, project):
        if project.UsesAnnealing():
            return self.UpdateAnnealingSettings(dict, project.method, project.method.algorithm)
        else:
            return self.UpdateGeneticsSettings(dict, project.method, project.method.algorithm)