import React from 'react';

export default function Timeslot(props) {
    let time = props.time;
    let is_morning = true;

    if ( time >= 12 && time < 24 ) {
        is_morning = false;
    }

    time %= 12;

    if ( time === 0 ) {
        time = 12;
    }

    if ( is_morning ) {
        time = time + 'am';
    }
    else {
        time = time + 'pm';
    }

    return (
        <>
            <div className="cs-timeslot">
                <div className="cs-timeslot-hour">{time}</div>
                <div className="cs-timeslot-subtime">00</div>
                <div className="cs-timeslot-subtime">15</div>
                <div className="cs-timeslot-subtime">30</div>
                <div className="cs-timeslot-subtime">45</div>
            </div>
        </>
    );
}

