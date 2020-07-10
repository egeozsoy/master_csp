import constraint
from pprint import pprint
import pandas as pd

class Lecture:
    def __init__(self,name,ec,area, theo=False):
        self.name = name
        self.ec = ec
        self.theo = theo
        self.area = area

    def __cmp__(self, other):
        return self.name < other.name

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

class ProblemWrapper:
    def __init__(self):
        self.problem = constraint.Problem()
        self.lectures = self.create_lectures()
        self.problem.addVariables(self.lectures, [0, 1])
        self.credit_limit = 65
        self.problem.addConstraint(self.credit_constraint, self.lectures)
        solutions = self.problem.getSolutions()
        pprint(solutions)
        print(len(solutions))

    def create_lectures(self):
        excel = pd.read_excel('tum_lectures.xlsx')
        current_area = None
        lectures = []
        for idx, row in excel.iterrows():
            if not isinstance(row[0], str):
                continue
            if 'ELECTIVE MODULES OF THE AREA' in row[0]:
                current_area = row[0].split('ELECTIVE MODULES OF THE AREA')[-1].split('"')[1]

            if row['ID'][:2] == 'IN':
                lectures.append(Lecture(name=row['Title'],ec=int(row['Credits']),area=current_area,theo=row['THEO']=='THEO'))
        return lectures[:50]

    def credit_constraint(self,*bools):
        sum = 0
        for idx in range(len(bools)):
            if bools[idx]:
                sum += self.lectures[idx].ec

        return sum >= self.credit_limit


def main():

    p = ProblemWrapper()
if __name__ == '__main__':
    main()