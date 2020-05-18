import React from 'react';

import Timeslot from './Timeslot.jsx';

export default function TimeTable(props) {

    let timeslots = []

    for (let i = 7; i <= 24; ++i) {
        timeslots.push(
            <Timeslot key={i} time={i} />
        )
    }

    return (
        <>
            <div className="cs-timetable">
                {timeslots}
            </div>
        </>
    );
}

