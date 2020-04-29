import sys
import copy

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

        self.room_assignments       = dict()
        self.instructor_assignments = dict()

    def solve(self):
        unassigned_section = self.is_complete_assignment()

        if not unassigned_section:
            return self.courses

        result = None

        print(unassigned_section)

        if not unassigned_section.timeslot:
            for timeslot in Course.timeslots:

                unassigned_section.timeslot = timeslot
                if self.is_valid_assignment():
                    result = self.solve()
                    if result:
                        return result
                else:
                    unassigned_section.timeslot = None

        elif not unassigned_section.room:
            for room in unassigned_section.rooms:

                unassigned_section.room = room

                if room not in self.room_assignments:
                    self.room_assignments[room] = list()
                self.room_assignments[room].append(unassigned_section)

                if self.is_valid_assignment():
                    result = self.solve()
                    if result:
                        return result
                else:
                    unassigned_section.room = None
                    self.room_assignments[room].remove(unassigned_section)

        elif not unassigned_section.instructor:
            for instructor in unassigned_section.instructors:

                unassigned_section.instructor = instructor

                if instructor not in self.instructor_assignments:
                    self.instructor_assignments[instructor] = list()
                self.instructor_assignments[instructor].append(unassigned_section)

                if self.is_valid_assignment():
                    result = self.solve()
                    if result:
                        return result
                else:
                    unassigned_section.instructor = None
                    self.instructor_assignments[instructor].remove(unassigned_section)
        
        return result

    def is_complete_assignment(self):
        for subject in self.courses:
            for section in self.courses[subject]:
                if not section.timeslot or not section.room or not section.instructor:
                    return section
        return None

    def is_valid_assignment(self):
        return self.room_collision() and self.instructor_collision()

    def room_collision(self):
        for room in self.room_assignments:

            sections = self.room_assignments[room]

            for i in range(len(sections)):
                if not sections[i].timeslot:
                    continue
                for j in range(i + 1, len(sections)):
                    if not sections[j].timeslot:
                        continue
                    elif sections[i].timeslot == sections[j].timeslot:
                        #print(sections[i].timeslot, sections[j].timeslot)
                        return False

        return True

    def instructor_collision(self):
        for instructor in self.instructor_assignments:

            sections = self.instructor_assignments[instructor]

            for i in range(len(sections)):
                if not sections[i].timeslot:
                    continue
                for j in range(i + 1, len(sections)):
                    if not sections[j].timeslot:
                        continue
                    elif sections[i].timeslot == sections[j].timeslot:
                        #print(instructor, sections[i].timeslot, sections[j].timeslot)
                        return False

        return True


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

    def __repr__(self):
        return f'{self.days} : {self.time}'


class Course:

    # Timeslot domain (TEST)
    timeslots = [
        #Timeslot( ['Mo', 'We'], ( 800,  915) ),
        #Timeslot( ['Mo', 'We'], (1000, 1115) ),
        #Timeslot( ['Mo', 'We'], (1600, 1715) ),
        #Timeslot( ['Tu', 'Th'], (1400, 1515) ),
        #Timeslot( ['Tu', 'Th'], (1000, 1115) ),
        #Timeslot( ['Tu', 'Th'], (1530, 1645) ),
        #Timeslot( ['Tu', 'Th'], (1500, 1615) ),
        #Timeslot( ['Fr'],       ( 900, 1015) )
    ]

    start = 800
    for _ in range(12):
        timeslots.append( Timeslot( ['Mo', 'We'], ( start,  start + 115) ) )
        timeslots.append( Timeslot( ['Tu', 'Th'], ( start,  start + 115) ) )
        timeslots.append( Timeslot( ['Fr'],       ( start,  start + 115) ) )
        start += 100

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


def write_to_csv(schedule):
    data = list()

    for subject in schedule:
        for section in schedule[subject]:
            data.append( [section.subject, section.course, section.section, section.timeslot.days, section.timeslot.time, section.room, section.instructor] )

    pd.DataFrame(data).to_csv('schedule.csv', index=False, header=['subject','course','section','days','time','room','instructor'])


def main():
    
    courses  = read_in_csv()
    solver   = Solver(courses)
    schedule = solver.solve()
    write_to_csv(schedule)

if __name__ == '__main__':
    main()
