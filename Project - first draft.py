import pandas as pd
from itertools import product

class Course(object):
    def __init__(self, name):
        self.name = name
        self.prof = None
        self.room = None
        self.startTime = None
        self.duration = None

    def getName(self):
        return self.name

    def getProf(self):
        return self.prof

    def setProf(self, profName):
        self.prof = profName

    def getRoom(self):
        return self.room

    def setRoom(self, roomNumber):
        self.room = roomNumber

    def getStartTime(self):
        return self.startTime

    def setStartTime(self, x):
        self.startTime = x

    def getDuration(self):
        return self.duration

    def setDuration(self, classTime):
        self.duration = classTime

class Schedule(object):
    def __init__(self):
        self.schedule = []

    def getSchedule(self):
        return self.schedule

    def copy(self):
        copySchedule = Schedule()
        copySchedule.schedule = self.schedule
        return copySchedule

def ToList(entry):
    s = ''
    L = []
    for i in range(len(entry)):
        if entry[i] != ',':
            s += entry[i]
        else:
            L.append(s)
            s = ''
        if i == len(entry) - 1:
            L.append(s)
    return L

if __name__ == "__main__":

    #loading the data from the input file
    data = pd.read_csv('courses.csv', header=None)
    df = pd.DataFrame(data)

    # defining a schedule instance that contains all courses
    root = Schedule()
    for i in range(1, df.shape[0]):
        root.getSchedule().append(Course(df.iloc[i, 0] + ' ' + df.iloc[i, 1]))

    #setting the duration for each class (duration).
    #duration is the only constant attribute of a course over all the schedules (room, time, prof attributes might change)
    for i in range(len(root.getSchedule())):
        root.getSchedule()[i].setDuration(df.iloc[i+1, 6])

    # defining a dictionary (key = course name, value = course instance)
    schedule = {}
    for course in root.getSchedule():
        schedule[course.getName()] = course

    CoursesNames = []
    for i in range(1, df.shape[0]):
        CoursesNames.append(df.iloc[i, 0] + ' ' + df.iloc[i, 1])

    # a dictionary consisting of all tuples (rooms, timing, profs) of an instance
    courses = {}
    numOfCourses = len(root.getSchedule())
    for i in range(1, numOfCourses + 1):
        rooms = ToList(df.iloc[i, 3])
        startTime = ToList(df.iloc[i, 5])
        profs = ToList(df.iloc[i, 4])
        courses[df.iloc[i, 0] + ' ' + df.iloc[i, 1]] = list(product(rooms, startTime, profs))

    frontier = []   # consists of all the nodes in the frontier of the search tree
    explored = []   # keeps track of the explored nodes of the backtracking search
    repeated = {}   # needed in the constraints to remove any repeated values
    path = []       # path of the depth of the algorithm to determine a consistent schedule
    explored_instance = []

    # adding the first course to start the backtracking search
    for tup in courses[df.iloc[1, 0] + ' ' + df.iloc[1, 1]]:
        instance = Course(df.iloc[1, 0] + ' ' + df.iloc[1, 1])
        x = schedule[instance.getName()].getDuration()
        instance.setDuration(x)
        instance.setRoom(tup[0])
        instance.setStartTime(tup[1])
        instance.setProf(tup[2])
        frontier.append(instance)

    frontier.reverse()

    scheduleNB = 0      # to count the schedules
    current = frontier.pop()
    y = current     # y keeps track of the parent node in the search tree
    path.append(current)
    explored.append(current.getName())
    index = 0       # determines the levels of the search tree (i.e., each course has a level)
    repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration()), (current.getStartTime(), current.getProf()))
    elt = CoursesNames[index+1]

    while len(frontier) > 0:
        L = []  # list of consistent child nodes
        for tup in courses[elt]:

            flag = 0
            instance = Course(elt)      # expanding the node to add a new course node
            instance.setRoom(tup[0])
            instance.setStartTime(tup[1])
            instance.setProf(tup[2])
            x = schedule[instance.getName()].getDuration()
            instance.setDuration(x)

            for key in repeated:
                # if 2 courses are scheduled in the same room, they should have different time
                if instance.getRoom() == repeated[key][0][0]:   # constraint: Same room, different timing
                    A = list(range(int(instance.getStartTime()), int(instance.getStartTime()) + int(schedule[elt].getDuration())))
                    B = list(range(int(repeated[key][0][1]), int(repeated[key][0][1]) + int(repeated[key][0][2])))

                    if list(set(A) & set(B)) != []:     # if there's time conflict
                        flag = 1
                        break
                # if 2 courses are scheduled with the same professor, they should have different time
                if  instance.getProf() == repeated[key][1][1]:  # constraint: Same professor, different timing
                    A = list(range(int(instance.getStartTime()), int(instance.getStartTime()) + int(schedule[elt].getDuration())))
                    B = list(range(int(repeated[key][0][1]), int(repeated[key][0][1]) + int(repeated[key][0][2])))

                    if list(set(A) & set(B)) != []:     # if there's time conflict
                        flag = 1
                        break
            if flag == 0:   # if no time conflict, add the new course instance
                L.append(instance)
        L.reverse()
        frontier = frontier + L

        L = []

        if len(path) < (df.shape[0] - 1):

            current = frontier.pop()
            if current.getName() != y.getName():
                if current.getName() not in explored:
                    repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration()), (current.getStartTime(), current.getProf()))
                    path.append(current)
                    explored.append(current.getName())
                    y = current
                    index += 1

                else:
                    name = current.getName()
                    courseIndex = CoursesNames.index(name)
                    iterations = len(path) - courseIndex-1
                    for i in range(iterations):
                        path.pop()

                    explored = []
                    path.pop()
                    path.append(current)
                    repeated = {}
                    for i in path:
                        repeated[i.getName()] = ((i.getRoom(), i.getStartTime(), i.getDuration()), (i.getStartTime(), i.getProf()))
                        explored.append(i.getName())

                    y = current
                    index = index - iterations

            else:
                repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration()), (current.getStartTime(), current.getProf()))
                path.pop()
                path.append(current)
                y = current


        while len(path) == (df.shape[0] - 1): # finding the goal schedule
            scheduleNB += 1

            print("Schedule number:", scheduleNB)        #count the schedules
            for course in path:  #print out the consistent schedule
                print("Course name:", course.getName(), "Room:", course.getRoom(), "Start Time:", course.getStartTime(), "Prof:", course.getProf(), "Duration:", course.getDuration())
            print()

            current = frontier.pop()

            if current.getName() != y.getName():
                name = current.getName()
                courseIndex = CoursesNames.index(name)
                iterations = len(path) - courseIndex-1
                for i in range(iterations):
                    path.pop()

                path.pop()
                path.append(current)
                explored = []
                repeated = {}
                for i in path:
                    repeated[i.getName()] = ((i.getRoom(), i.getStartTime(), i.getDuration()), (i.getStartTime(), i.getProf()))
                    explored.append(i.getName())
                y = current
                index = index - iterations

            else:
                repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration()), (current.getStartTime(), current.getProf()))
                path.pop()
                path.append(current)
                y = current

        elt = CoursesNames[index+1]
