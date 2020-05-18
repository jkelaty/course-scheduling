import React from 'react';

export default function Course(props) {
    return (
        <>
            <div
                className="cs-course"
                style={{
                    '--start-hour'   : props.course['time']['start']['hour'],
                    '--start-minute' : props.course['time']['start']['minute'],
                    '--end-hour'     : props.course['time']['end']['hour'],
                    '--end-minute'   : props.course['time']['end']['minute'],
                    '--color'        : props.course['color'],
                    '--course-index' : props.course_index,
                    '--hour-index'   : props.hour_index
                }}>

                <div className="cs-course-code">
                    {props.course['course']}
                </div>

                <div className="cs-course-instructor">
                    {'Instructor: ' + props.course['instructor']}
                </div>

                <div className="cs-course-room">
                    {'Room: ' + props.course['room']}
                </div>

                <div className="cs-course-time">
                    {'Time: ' + props.course['time_f']}
                </div>

                <div className="cs-course-days">
                    {'Day(s): ' + props.course['days_f']}
                </div>
            </div>
        </>
    );
}

