import React from 'react';

export default function DaySlot(props) {
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
            <div className="cs-dayslot">
                <div className="cs-dayslot-subtime" />
                <div className="cs-dayslot-subtime" />
                <div className="cs-dayslot-subtime" />
                <div className="cs-dayslot-subtime" />
                
                {props.children}
            </div>
        </>
    );
}

