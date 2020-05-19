import React from 'react';

import Dayslot from './Dayslot.jsx';
import Course from './Course.jsx';

export default function DayTable(props) {
    let dayslots = []
    let course_index = 1;

    for (let i = 7; i <= 24; ++i) {
        let courses = [];
        let hour_index = 1;

        for (var course in props.display[props.day]) {
            if ( props.schedule[course]['time']['start']['hour'] === i ) {
                courses.push(
                    <Course key={course} course_index={course_index} hour_index={hour_index} course={props.schedule[course]} />
                );
                
                ++course_index;

                if ( hour_index < 10) {
                    ++hour_index;
                }
            }
        }

        dayslots.push(
            <Dayslot key={i} time={i} >
                {courses}
            </Dayslot>
        );
    }

    return (
        <>
            <div className="cs-daytable">
                {dayslots}
            </div>
        </>
    );
}

