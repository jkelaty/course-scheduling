# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:31:45 2020

@author: User
"""

import pandas as pd
from itertools import product
import math
import random

class Course(object):
    def __init__(self, name):
        self.name = name
        self.prof = None
        self.room = None
        self.startTime = None
        self.duration = None
        self.time = None
        self.weekDay = None
        self.evaluation = 0
        self.day = []
        
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
        
    def getTime(self):
        return self.time

    def setTime(self, x):
        self.time = x
        
    def getWeekDay(self):
        return self.weekDay
    
    def setWeekDay(self, x):
        self.weekDay = x
        
    def getEval(self):
        return self.evaluation
        
    def setEval(self, x):
        self.evaluation = x
        
    def getDay(self):
        return self.day
    
    def setDay(self, x):
        self.day = x
 
class Schedule(object):
    def __init__(self):
        self.schedule = []
    
    def getSchedule(self):
        return self.schedule     

def ToList(entry):
    s = ''
    L = []
    try:
        for i in range(len(entry)):
            if entry[i] != ',':
                s += entry[i]
            else:
                L.append(s)
                s = ''
            if i == len(entry) - 1:
                L.append(s)                
    except:
        L = []
    return L       

def sameDay(s1, s2):
    sameDay = 0
    if s1 in ['M', 'MW', 'MTH', 'MF']:
        if s2 in ['M', 'MW', 'MTH', 'MF']:
            sameDay = 1
                    
    if s1 in ['T', 'TTH', 'TF']:
        if s2 in ['T', 'TTH', 'TF']:
            sameDay = 1
                    
    if s1 in ['W', 'MW', 'WF']:
        if s2 in ['W', 'MW', 'WF']:
            sameDay = 1
            
    if s1 in ['TH', 'MTH', 'TTH']:
        if s2 in ['TH', 'MTH', 'TTH']:
            sameDay = 1      
                    
    if s1 in ['F', 'MF', 'TF', 'WF']:
        if s2 in ['F', 'MF', 'TF', 'WF']:
            sameDay = 1
            
    return sameDay
    
def smallData():    
    frontier = []   # consists of all the nodes in the frontier of the search tree
    explored = []   # keeps track of the explored nodes of the backtracking search
    repeated = {}   # needed in the constraints to remove any repeated values
    path = []       # path of the depth of the algorithm to determine a consistent schedule
    threshold = 0 
    itr = 0
    
    # adding the first course to start the backtracking search    
    for tup in courses[root.getSchedule()[0].getName()]:        
        instance = Course(root.getSchedule()[0].getName())
        x = schedule[instance.getName()].getDuration()
        instance.setDuration(x)
        y = schedule[instance.getName()].getDay()
        instance.setDay(y)
        w = schedule[instance.getName()].getDay()[0]
        instance.setWeekDay(w)     
        instance.setRoom(tup[0])
        instance.setStartTime(tup[1])
        instance.setProf(tup[2])   
        instance.setTime(root.getSchedule()[0].getTime())
        
        frontier.append(instance)
              
    frontier.reverse() 
        
    scheduleNB = 0      # to count the schedules
    current = frontier.pop()
    y = current     # y keeps track of the parent node in the search tree
    path.append(current)
    explored.append(current.getName())
    index = 0       # determines the levels of the search tree (i.e., each course has a level)
    repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration(), current.getWeekDay()), (current.getStartTime(), current.getProf(), current.getWeekDay()))
    
    elt = CoursesNames[index+1]
        
    while len(frontier) > 0:
        L = []  # list of consistent child nodes
        for tup in courses[elt]:       
                
            flag = 0
            instance = Course(elt)      # expanding the node to add a new course node
            instance.setRoom(tup[0])    
            instance.setStartTime(tup[1])
            instance.setProf(tup[2])
            instance.setWeekDay(tup[3])
            x = schedule[instance.getName()].getDuration()
            instance.setDuration(x)
            z = schedule[instance.getName()].getDay()
            instance.setDay(z)           
            
            if instance.getStartTime() in [8, 9, 10, 11, 12]:
                instance.setTime("Morning")
                
            elif instance.getStartTime() in [13, 14, 15, 16]:
                instance.setTime("Afternoon")
            
            elif instance.getStartTime() in [17, 18, 19, 20]:
                instance.setTime("Evening")            
                
            # implementing the hard constraints
            for key in repeated: # search with inference as a preprocessing step (constraint propagation - arc and path consistency)
                # if 2 courses are scheduled in the same room, they should have different time
                if instance.getRoom() == repeated[key][0][0]:   # constraint: Same room, different timing
                    A = list(range(instance.getStartTime(), math.ceil(instance.getStartTime() + schedule[elt].getDuration()+0.25) + 1))
                    B = list(range(repeated[key][0][1], int(repeated[key][0][1] + repeated[key][0][2]) + 1))
                    if list(set(A) & set(B)) != []:     # if there's time conflict
                        if sameDay(instance.getWeekDay(), repeated[key][0][3]) == 1:                          
                            flag = 1
                            break
                # if 2 courses are scheduled with the same professor, they should have different time
                if  instance.getProf() == repeated[key][1][1]:  # constraint: Same professor, different timing
                    A = list(range(instance.getStartTime(), math.ceil(instance.getStartTime() + schedule[elt].getDuration() + 0.25) + 1))
                    B = list(range(repeated[key][0][1], int(repeated[key][0][1] + repeated[key][0][2]) + 1))                    
                    if list(set(A) & set(B)) != []:     # if there's time conflict
                        if sameDay(instance.getWeekDay(), repeated[key][0][3]) == 1:
                            flag = 1
                            break        
            if flag == 0:   # if no time conflict, add the new course instance              
                
                L.append(instance)
                    
        L.reverse()
        frontier = frontier + L 
        L = []
            
        if len(path) < len(root.getSchedule()):          
            current = frontier.pop()
    
            if current.getName() != y.getName():
                if current.getName() not in explored:
                    repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration(), current.getWeekDay()), (current.getStartTime(), current.getProf(), current.getWeekDay()))              
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
                        repeated[i.getName()] = ((i.getRoom(), i.getStartTime(), i.getDuration(), i.getWeekDay()), (i.getStartTime(), i.getProf(), i.getWeekDay()))
                        explored.append(i.getName())
                    y = current
                    index = index - iterations                       
            else:
                repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration(), current.getWeekDay()), (current.getStartTime(), current.getProf(), current.getWeekDay()))
                path.pop()
                path.append(current)
                y = current
                    
        while len(path) == len(root.getSchedule()): # finding the goal schedule
            val = 0
            
            for course in path:
                evaluation(course)
                val = val + course.getEval()
                
            scheduleNB += 1  
            if val > threshold:
                res = pd.DataFrame()
                df3 = pd.DataFrame([['Subject', 'Course', 'Room', 'Class Day(s)', 'Class Time', 'Professor', 'Duration']])
                res = res.append(df3)
                itr += 1
                threshold = val  
                c = 0
                for course in path:  #print out the consistent schedule
                    evaluation(course)
                    c = c + 1
                    if course.getStartTime() > 12:
                        course.setStartTime(str(course.getStartTime() - 12)+':00 PM')
                    elif course.getStartTime() == 12:    
                        course.setStartTime(str(course.getStartTime()) + ':00 PM')
                    else:
                        course.setStartTime(str(course.getStartTime()) + ':00 AM')
                
                    x = course.getName()  
                    ind = x.index(' ')
                    r = x[:ind]
                    t = x[ind:]
                    df3 = pd.DataFrame([[r, t, course.getRoom(), course.getWeekDay(), course.getStartTime(), course.getProf(), str(int(course.getDuration()*60)) + ' mins']])
                    res = res.append(df3)
                itr = 1
                break
            
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
                    repeated[i.getName()] = ((i.getRoom(), i.getStartTime(), i.getDuration(), i.getWeekDay()), (i.getStartTime(), i.getProf(), i.getWeekDay()))
                    explored.append(i.getName())
                y = current
                index = index - iterations                     
            else:
                repeated[current.getName()] = ((current.getRoom(), current.getStartTime(), current.getDuration(), current.getWeekDay()), (current.getStartTime(), current.getProf(), current.getWeekDay()))
                path.pop()
                path.append(current)
                y = current
        if itr == 1:
            res.to_csv('output.csv', header=False, index=False)
            break
        elt = CoursesNames[index+1] 
    
def largeData():
    scheduleNb = 0
    val = 0
    threshold = 0 
    
    for n in range(30):
        repeated = {} 
        c = 0
        L = {}
        
        for k in range(len(root.getSchedule())):
            flag = 0
            elt = CoursesNames[k]
            i = root.getSchedule()[k]
            x = courses[i.getName()]
            for j in range(len(x)):
                flag = 0
                tup = x[random.randint(0, len(x) - 1)]
                
                for key in repeated: # search with inference as a preprocessing step (constraint propagation - arc and path consistency)
                    # if 2 courses are scheduled in the same room, they should have different time
                    if tup[0] == repeated[key][0][0]:   # constraint: Same room, different timing
                        A = list(range(tup[1], math.ceil(tup[1] + schedule[elt].getDuration()+0.25) + 1))
                        B = list(range(repeated[key][0][1], int(repeated[key][0][1] + repeated[key][0][2]) + 1))
                        if list(set(A) & set(B)) != []:     # if there's time conflict
                            if sameDay(tup[3], repeated[key][0][3]) == 1:  
                                flag = 1
                                break
                                
                    # if 2 courses are scheduled with the same professor, they should have different time
                    if  tup[2] == repeated[key][1][1]:  # constraint: Same professor, different timing
                        A = list(range(tup[1], math.ceil(tup[1] + schedule[elt].getDuration() + 0.25) + 1))
                        B = list(range(repeated[key][0][1], int(repeated[key][0][1] + repeated[key][0][2]) + 1))                    
                        if list(set(A) & set(B)) != []:     # if there's time conflict
                            if sameDay(tup[3], repeated[key][0][3]) == 1:
                                flag = 1
                                break
                                                 
                if flag == 0:   # if no time conflict, add the course to the schedule
                    repeated[i.getName()] = ((tup[0], tup[1], i.getDuration(), tup[3]), (tup[1], tup[2], tup[3]))              
                    L[i] = tup
                    if len(L) == len(root.getSchedule()):
                        val = 0                        
                        scheduleNb += 1
                        for t in CoursesNames:
                            s = schedule[t]
                            if L[s][1] in [8, 9, 10, 11, 12]:
                                s.setTime("Morning")
                
                            elif L[s][1] in [13, 14, 15, 16]:
                                s.setTime("Afternoon")
            
                            elif L[s][1] in [17, 18, 19, 20]:
                                s.setTime("Evening")                            
                            
                        for t in CoursesNames:
                            s= schedule[t]
                            s.setProf(L[s][2])
                            evaluation(s)
                            val = val + s.getEval()                        
                            
                        if val >= threshold:
                            threshold = val                                               
                            res = pd.DataFrame()
                            df3 = pd.DataFrame([['Subject', 'Course', 'Room', 'Class Day(s)', 'Class Time', 'Professor', 'Duration']])
                            res = res.append(df3)
                            
                            for t in CoursesNames:
                                s = schedule[t]   
                                c += 1                                
                                if L[s][1] > 12:
                                    s.setStartTime(str(L[s][1] - 12)+':00 PM')                                                           
                                elif L[s][1] == 12: 
                                    s.setStartTime(str(L[s][1])+':00 PM')
                                else:
                                    s.setStartTime(str(L[s][1])+':00 AM')
                                x = s.getName()  
                                ind = x.index(' ')
                                r = x[:ind]
                                t = x[ind:]
                                df3 = pd.DataFrame([[r, t, L[s][0], L[s][3], s.getStartTime(), L[s][2], str(int(s.getDuration()*60)) + ' mins']])
                                res = res.append(df3)
                    break
                
    try: 
        res.to_csv('output.csv', header=False, index=False)
    except:
        res = pd.DataFrame()
        df3 = pd.DataFrame([['Course Name', 'Room', 'Class Day(s)', 'Class Time', 'Professor', 'Duration', 'Daytime']])
        res = res.append(df3)
                
def evaluation(instance):
    p = 0
    prof = instance.getProf()            
    if prof in profTimePreference and instance.getTime() in profTimePreference[prof]:
        p += 1
    s = instance.getName()  
    index = s.index('-')
    t = s[:index]
    if prof in profCoursePreference and t in profCoursePreference[prof]:
        p += 1   
        
    instance.setEval(p)                    
    
if __name__ == "__main__":

    # assuming that each credit is a 50-min class 
    creditDuration = 50
        
    #loading the data from the input file
    file = input("Enter the data filename: ")
    data = pd.read_csv(file, header=None)
    df = pd.DataFrame(data)
             
    # defining a schedule instance that contains all courses
    root = Schedule()
    for i in range(1, df.shape[0]):
        for j in range(int(df.iloc[i, 2])):
            root.getSchedule().append(Course(df.iloc[i, 0] + ' ' + df.iloc[i, 1] + "-" + str(j + 1)))
    
    #setting the duration for each class (duration). 
    #duration is the only constant attribute of a course (room, time, prof attributes might change)    
    i = 1
    k = 0       
    while i < df.shape[0]:
        creditsNb = df.iloc[i, 5]
        time = int(creditsNb) * creditDuration
        time = time / 60    # finding the duration in hours
        classesPerWeek = int(df.iloc[i, 6])
        # specifying the duration of a class based on the nb of classes/week
        if classesPerWeek == 1:
            duration = time
            daysPerWeek = ['M', 'T', 'W', 'TH', 'F']
        elif classesPerWeek == 2:
            daysPerWeek = ['MW', 'TTH', 'MTH', 'MF', 'TF', 'WF']
            duration = time/2
        for j in range(int(df.iloc[i, 2])):               
            root.getSchedule()[k].setDuration(duration)
            root.getSchedule()[k].setDay(daysPerWeek)
            k = k + 1           
        i += 1
            
    # implementing the soft constraints  
    i = 1  
    k = 0   
    while i < df.shape[0]:
        try:
            profTimePreference1 = ToList(df.iloc[i, 8])
        except:
            profTimePreference1 = []
                           
        try:
            courseTimePreference = ToList(df.iloc[i, 9])
        except:
            courseTimePreference = []
        
        if profTimePreference1 != []:
            if courseTimePreference != []:
                if profTimePreference1[0] == courseTimePreference[0]:
                    for j in range(int(df.iloc[i, 2])):               
                        root.getSchedule()[k].setTime(profTimePreference1[0])
                        k = k + 1                                  
                else:   # if prof and course preferences are at odd, distribute the preferences over the sections
                    L = [courseTimePreference[0], profTimePreference1[0]]
                    for j in range(int(df.iloc[i, 2])):               
                        root.getSchedule()[k].setTime(L[j%len(L)])
                        k = k + 1                        
            else:
                for j in range(int(df.iloc[i, 2])):               
                    root.getSchedule()[k].setTime(profTimePreference1[0])
                    k = k + 1                       
        else:
            if courseTimePreference != []:
                for j in range(int(df.iloc[i, 2])):               
                    root.getSchedule()[k].setTime(courseTimePreference[0])
                    k = k + 1           
            else:   # if no course time is prefered, take any of the available times
                L = ['Morning', 'Afternoon', 'Evening']
                for j in range(int(df.iloc[i, 2])):  
                    root.getSchedule()[k].setTime(L[j%len(L)])
                    k = k + 1
        i += 1   
        
    # defining a dictionary that maps a course name to a course instance
    # (key = course name, value = course instance)
    schedule = {}
    for course in root.getSchedule():
        schedule[course.getName()] = course
            
    CoursesNames = []
    for i in root.getSchedule():
        CoursesNames.append(i.getName())
                    
    # a dictionary consisting of all tuples (rooms, timing, profs) of an instance
    courses = {}
    i = 1
    k = 0       
    while i < df.shape[0]:
        rooms = ToList(df.iloc[i, 3])
        random.shuffle(rooms)
        profs = ToList(df.iloc[i, 4])
        random.shuffle(profs)
        
        try:
            profPreference = ToList(df.iloc[i, 7])  
            random.shuffle(profPreference)
            for j in profs:
                if j not in profPreference:
                    profPreference.append(j)                   
        except:
            profPreference = profs   
        
        for l in range(int(df.iloc[i, 2])):  
                            
            if  root.getSchedule()[k].getTime() == 'Morning':
                root.getSchedule()[k].setStartTime((root.getSchedule()[k].getWeekDay(), [8, 9, 10, 11, 12]))
            elif root.getSchedule()[k].getTime() == 'Afternoon':
                root.getSchedule()[k].setStartTime((root.getSchedule()[k].getWeekDay(), [13, 14, 15, 16]))
            else:
                root.getSchedule()[k].setStartTime((root.getSchedule()[k].getWeekDay(), [17, 18, 19, 20]))
            time =  root.getSchedule()[k].getStartTime()[1] 
            days = root.getSchedule()[k].getDay() 
            if ToList(df.iloc[i, 7]) == []:
                random.shuffle(profPreference)
            courses[root.getSchedule()[k].getName()] = list(product(rooms, time, profPreference, days))
            k = k + 1           
        i += 1
        
    i = 1
    profTimePreference = {}
    profCoursePreference = {}
    
    file = input("Enter the soft preferences filename: ")
    preferenceData = pd.read_csv(file, header=None)
    df1 = pd.DataFrame(preferenceData)
        
    while i < df1.shape[0]:
        timePreference = ToList(df1.iloc[i, 1])
        coursePreference = ToList(df1.iloc[i, 2])
        if timePreference != []:
            profTimePreference[df1.iloc[i, 0]] = timePreference
        if coursePreference != []:
            profCoursePreference[df1.iloc[i, 0]] = coursePreference        
        i += 1
   
    if df.shape[0] < 50:
        smallData()
    else:
        largeData()
