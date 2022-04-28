import json
import copy

class PredictionModel():
    def __init__(self, database):
        self.database = database

        record = database["frequentPatterns"].find_one()
        self.closed_patterns = record
    
    def isConflict(self,source,dest):
        for k,v in source.items():
            if k in dest and dest.get(k) != v:
                return True
        return False
    
    def hasCommonFeatures(self,source,dest):
        for k,v in source.items():
            if k in dest and dest.get(k) == v:
                return True
        return False

    def unique(self,source,dest):
        uniq = False
        for k,v in source.items():
            if k not in dest:
                uniq = True
        return uniq
    
    def findSolutions(self, userSolution):
        solutions = []
        patternList = []
        orgpatterns = self.closed_patterns['patterns']
        for pattern in orgpatterns:
            if not self.isConflict(pattern,userSolution) and self.hasCommonFeatures(pattern,userSolution):
                patternList.append(pattern)
        unusedpatterns = patternList
        while unusedpatterns:
            solution = copy.deepcopy(userSolution)
            patterns = []
            for pattern in unusedpatterns:
                if not self.isConflict(pattern,solution) and self.unique(pattern,solution):
                    solution.update(pattern)
                    patterns.append(pattern)
            
            for pattern in patternList:
                if not self.isConflict(pattern,solution) and self.unique(pattern,solution):
                    solution.update(pattern)
                    patterns.append(pattern)
            solutions.append(solution)
            if len(solutions) > 5:
                break
            for pattern in patterns:
                unusedpatterns.remove(pattern)
        return solutions

if __name__ == '__main__':
    model = PredictionModel()
    userSolution = {'Title': 'ASE GROUP MEETING','Category':'Team Meeting', 'Period': 'Semester', 'Day' : 'Thursday'}
    solutions = model.findSolutions(userSolution)
    for sol in solutions:
        print("sol -> ",sol)