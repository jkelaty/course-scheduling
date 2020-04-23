import pandas as pd

"""
Authors: Jonathan Kelaty and Manal Zneit
CS 350 Final Project: Course Scheduling

"""



"""
    TODO:
        Add constraint functions
        Timeslot domain
        Implement Day/Time collision checking for same classroom (hashmap of classrooms?)
        Implement Day/Time collision checking for same instructor (hashmap of instructors?)

        ~ Instructor preferences
        ~ Distribution of courses over instructors and Day/Times

        ! Weighted constraints
        ! Backtracking
        ! All solutions
        ! Heuristic evaluation

    Notes:
        Do we consider 1/2/3/4 credit hour courses? Just 3? 3 and 4? (timeslots will differ)
        Do we want room # assignment to be related to course enrollment capacity? (rooms will have varrying capacities)
        Do we want to manually define acceptable timeslots, or let algorithm generate as needed (random timeslots)?
        Potential reference:
            http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.44.8460&rep=rep1&type=pdf
"""


class Solver():
    def __init__(self, courses):
        self.courses = courses

    def solve(self):
        return 0



"""
Pesudocode for backtracking search:
    if assignment is complete, then return assignment
    var = select_unassigned_variable
    for each value in order_domain_values
        if value is consistent with assignment then
            add {var = value} to assignment
            result = backtracking_search()
            if result != failure then result result
            remove {var = value} from assignment
    return failure


    Assign vars - room #, day/time, instructor
"""


class Timeslot:
    def __init__(self, days, time):
        self.days = days
        self.time = time

    # == operator overload used for checking if timeslots overlap
    # Could potentially be optimized?
    def __eq__(self, other):
        all_days = set(self.days + other.days)

        if len(all_days) == (len(self.days) + len(other.days)):
            return False
        elif ( self.time[0] <= other.time[0] <= self.time[1] or
               self.time[0] <= other.time[1] <= self.time[1] ):
            return True
        else:
            return False


class Course:

    # Timeslot domain (TEST)
    timeslots = [
        Timeslot( ['Mo', 'We'], (1000, 1115) ),
        Timeslot( ['Mo', 'We'], (1130, 1245) ),
        Timeslot( ['Tu', 'Th'], (1500, 1615) ),
        Timeslot( ['Fr'],       ( 900, 1015) )
    ]

    def __init__(self, subject, course, section, rooms, instructors):
        # Course attributes
        self.subject = subject
        self.course  = course
        self.section = section

        # Domains
        self.rooms       = rooms
        self.instructors = instructors

        # Variables
        self.timeslot   = None
        self.room       = None
        self.instructor = None

    # Print course - used for testing
    def __repr__(self):
        return f'{self.subject} {self.course}:{self.section}'


def read_in_csv():
    df = pd.read_csv('courses.csv')

    courses = dict()

    for _, row in df.iterrows():
        subject     = row['subject']
        course      = row['course']
        sections    = int(row['sections'])
        rooms       = [room for room in row['rooms'].split(',')]
        instructors = [professor for professor in row['instructors'].split(',')]

        if subject not in courses:
            courses[subject] = list()

        # Create unique course for each section, differs only in section #
        for i in range(1, sections + 1):
            course_obj = Course(subject, course, i, rooms, instructors)
            courses[subject].append(course_obj)

    return courses


def main():
    
    courses = read_in_csv()
    solver  = Solver(courses)
    results = solver.solve()

    print(results)

if __name__ == '__main__':
    main()
