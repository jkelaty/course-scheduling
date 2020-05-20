# Course Scheduling Using Constraint Satisfaction

- Our final project focusses on the problem of course scheduling. We wanted to devise a program that could be realistically deployed for use given certain data that should be readily available by a college or university. The program calls for a list of course data specifying the available rooms, qualified instructors, and desired time of day to schedule the course (i.e. morning, afternoon, evening). Optionally, the user can provide a list of additional soft constrains for the instructor's preferences for courses and times to be scheduled for.

## Contents

- [Implementation](#implementation)
- [Contributions](#contributions)
- [Visualization](#visualization)
- [Data](#data)

## Implementation
- **Local search**

- **Random restarts**
    - Implemented to satisfy the maximum number of soft constraints (instructor preferences)

## Contributions

### Team
- Algorithm implementation development

### Jonathan Kelaty
- Built visualization tool
- Scraped and normalized Hunter College course data

### Manal Zneit
- Wrote program implementation
- Created test datasets

## Visualization
- Visualization tool built using React
- Upload course data and visualize schedule
- Filter for constrained variables
- <a href="https://jkelaty.github.io/course-scheduling/" target="_blank">View visualization tool</a>

![visualization GIF](https://raw.githubusercontent.com/jkelaty/course-scheduling/master/img/visualization.gif)

## Data
- Course data was scrapped from CUNY course offerings (~2000 sections)
- Normalized times, rooms, and instructor assignments
