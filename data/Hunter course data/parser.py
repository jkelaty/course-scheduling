import pandas as pd
import random

from datetime import datetime

times = ['Morning', 'Afternoon', 'Evening']

def get_credits(time, num_days):
    if time is not '' and num_days > 0:
        timesA = [datetime.strptime(item, "%I:%M%p") for item in time.split(" - ")]
        timesH = (timesA[1].hour   - timesA[0].hour) * 60
        timesM =  timesA[1].minute - timesA[0].minute
        total  = (timesH + timesM) * num_days / 60
        return total
    else:
        return 3

def convert_time(time):
    return times[random.randint(0,2)]

class Subject:
    def __init__(self, _subject):
        self.subject     = _subject
        self.instructors = set()
        self.rooms       = set()
        self.courses     = dict()

class Course:
    def __init__(self, _subject, _course, _title, _credits):
        self.subject = _subject
        self.course  = _course
        self.title   = _title
        self.credits = _credits

        self.sections = {
            'Morning'   : 0,
            'Afternoon' : 0,
            'Evening'   : 0
        }

# Input/Output
INPUT_FILE  = 'courses.csv'
OUTPUT_FILE = 'test.csv'

df = pd.read_csv(INPUT_FILE)
df.fillna('', inplace=True)

courses = dict()

for _, row in df.iterrows():
    subject    = row['course'].split()[0]
    course     = row['course']
    title      = row['title']
    time       = convert_time(row['time'])
    num_days   = len(row['days_of_week']) / 2
    credit_hrs = int(round(get_credits(row['time'], num_days)))

    instructor = row['instructor']
    room       = row['room']

    if subject not in courses:
        courses[subject] = Subject(subject)

    if course not in courses[subject].courses:
        courses[subject].courses[course] = Course(subject, course, title, credit_hrs)

    courses[subject].courses[course].sections[time] += 1

    if instructor is not '':
        courses[subject].instructors.add(instructor)
    if room is not '':
        courses[subject].rooms.add(room)

data = list()

for subject in courses:
    for course in courses[subject].courses:
        for section in courses[subject].courses[course].sections:
            if courses[subject].courses[course].sections[section] > 0:
                data.append([
                    course,
                    courses[subject].courses[course].sections[section],
                    ','.join(courses[subject].rooms),
                    ','.join(courses[subject].instructors),
                    section,
                    courses[subject].courses[course].credits
                ])

header = [
    'course',
    'sections',
    'rooms',
    'instructors',
    'time',
    'credits'
]

pd.DataFrame(data).to_csv(OUTPUT_FILE, header=header, index=False)

