'''
Constraint Satisfaction Problem to find best lectures to complete
Needs to be modified to suit a certain need. Is more of a template now
Requires python-constraint
'''

from collections import defaultdict

import constraint

from helpers.lecture import Lecture


class ProblemWrapper:
    def __init__(self):
        self.credit_limit = 120
        self.theo_limit = 10
        self.area_limit = [18, 8, 8]
        self.lectures = [Lecture(name='Computer Vision I: Variational Methods', ec=8, area='COMPUTER GRAPHICS AND VISION', theo=True, grade=3.0),
                         Lecture(name='Computer Vision II: Multiple View Geometry', ec=8, area='COMPUTER GRAPHICS AND VISION', theo=True, grade=None),
                         Lecture(name='Natural Language Processing', ec=6, area='MACHINE LEARNING AND ANALYTICS', grade=2.3),
                         Lecture(name='Introduction to Deep Learning', ec=6, area='MACHINE LEARNING AND ANALYTICS', grade=1.0),
                         Lecture(name='Advanced Deep Learning for Computer Vision', ec=8, area='COMPUTER GRAPHICS AND VISION', grade=None),
                         Lecture(name='Seminar', ec=5, area='None', grade=1.0),
                         Lecture(name='Practical Course', ec=10, area='None', grade=None),
                         Lecture(name='IDP', ec=16, area='None', grade=None),
                         Lecture(name='Guided Research', ec=10, area='None', grade=None),
                         Lecture(name='Thesis', ec=30, area='None', grade=None),
                         Lecture(name='Language1', ec=3, area='None', grade=1.7),
                         Lecture(name='Language2', ec=3, area='None', grade=None),
                         Lecture(name='BIO LECTURE', ec=6, area='BIO', grade=None),
                         Lecture(name='BIO LECTURE2', ec=6, area='BIO', grade=None),
                         ]

        self.problem = constraint.Problem()
        self.problem.addVariables(self.lectures, [0, 1])

        self.problem.addConstraint(self.credit_constraint, self.lectures)
        self.problem.addConstraint(self.theo_constraint, self.lectures)
        self.problem.addConstraint(self.area_constraint, self.lectures)
        solutions = self.problem.getSolutions()
        solutions = self.solution_sorting(solutions)
        print(f'{len(solutions)} solution found\n')
        for i in range(min(3, len(solutions))):
            print(f'Credits: {self.get_credits_for_solution(solutions[i])}')
            print(f'Grade: {self.get_grade_average_for_solution(solutions[i])}\n')
            print(self.solution_to_str(solutions[i]))
            print()

    def credit_constraint(self, *bools):
        total_sum = 0
        for idx in range(len(bools)):
            if bools[idx]:
                total_sum += self.lectures[idx].ec
                if total_sum >= self.credit_limit * 1.3:
                    return False
        return total_sum >= self.credit_limit

    def theo_constraint(self, *bools):
        theo_credits = 0
        for idx in range(len(bools)):
            if bools[idx] and self.lectures[idx].theo:
                theo_credits += self.lectures[idx].ec

                if theo_credits >= self.theo_limit * 2:
                    return False

        return theo_credits >= self.theo_limit

    def area_constraint(self, *bools):
        areas = defaultdict(int)
        for idx in range(len(bools)):
            if bools[idx]:
                areas[self.lectures[idx].area] += self.lectures[idx].ec

        areas.pop('None', None)
        sorted_areas = sorted(areas.values(), reverse=True)
        if len(sorted_areas) >= 3 and sorted_areas[0] >= 18 and sorted_areas[1] >= 8 and sorted_areas[2] >= 8:
            return True
        else:
            return False

    def get_credits_for_solution(self, solution):
        total_ec = 0
        for key, value in solution.items():
            if value == 0:
                continue

            total_ec += key.ec

        return total_ec

    def get_grade_average_for_solution(self, solution, default_grade=None):
        total_ec = 0
        total_points = 0
        for key, value in solution.items():
            if value == 0:
                continue

            grade = key.grade
            if grade is None:
                grade = default_grade

            if grade is not None:
                total_points += grade * key.ec
                total_ec += key.ec

        return total_points / total_ec

    def solution_sorting(self, solutions):
        ecs = []
        for solution in solutions:
            ecs.append(self.get_grade_average_for_solution(solution))

        solutions = [x for _, x in sorted(zip(ecs, solutions), key=lambda pair: pair[0])]

        return solutions

    def solution_to_str(self, solution):
        out = ''
        for key, value in solution.items():
            if value:
                out += f'{key}\n'

        return out


if __name__ == '__main__':
    problem_wrapper = ProblemWrapper()
