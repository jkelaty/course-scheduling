import React from 'react';

import Filters from './Filters.jsx';
import TimeTable from './TimeTable.jsx';
import DayTable from './DayTable.jsx';

import { CSSTransition } from 'react-transition-group';

import './ScheduleViewer.scss';


export default class ScheduleViewer extends React.Component {
    constructor(props) {
        super(props);

        this.schedule = {};

        this.data = {
            subjects:    {},
            courses:     {},
            instructors: {},
            rooms:       {},
            colors:      {}
        };

        this.parseSchedule(this.props.schedule);

        this.state = {
            display_schedule : this.getDisplaySchedule(),
            filters_active: false,
            filters_helper: true,
            filters: {
                subjects:    {},
                courses:     {},
                instructors: {},
                rooms:       {}
            }
        };

        this.callback = this.changeFilters.bind(this);
    }

    parseSchedule(schedule_arr) {
        for (let i = 1; i < schedule_arr.length; ++i) {
            let subject = schedule_arr[i][0];
            let section = schedule_arr[i][1]

            if ( section[0] !== ' ' ) {
                section = ' ' + section;
            }

            let course = subject + section;

            let days        = '';
            let days_string = String(schedule_arr[i][3]);
            var days_array  = {}

            while ( days_string !== '' ) {
                if ( days_string[0] === 'M' ) {
                    days_array['Monday'] = true;
                    days_string = days_string.substring(1);
                    days += "Mo, ";
                }
                else if ( days_string[0] === 'W' ) {
                    days_array['Wednesday'] = true;
                    days_string = days_string.substring(1);
                    days += "We, ";
                }
                else if ( days_string[0] === 'F' ) {
                    days_array['Friday'] = true;
                    days_string = days_string.substring(1);
                    days += "Fr, ";
                }
                else if ( days_string.substring(0,2) === 'TH' ) {
                    days_array['Thursday'] = true;
                    days_string = days_string.substring(2);
                    days += "Th, ";
                }
                else if ( days_string[0] === 'T' ) {
                    days_array['Tuesday'] = true;
                    days_string = days_string.substring(1);
                    days += "Tu, ";
                }
                else {
                    break;
                }
            }

            if ( days !== '' ) {
                days = days.substring(0, days.length - 2);
            }

            let times = schedule_arr[i][4];

            var time = {
                start: {
                    hour: 12,
                    minute: 0
                },
                end: {
                    hour: 12,
                    minute: 0
                }
            };

            if ( times ) {
                let duration    = parseInt(schedule_arr[i][6]);
                let time_array  = times.split(' ');
                let time_start  = time_array[0].split(':');
                let time_end    = time_array[0].split(':');
                let time_period = time_array[1];

                for (let j = 0; j < time_start.length; ++j) {
                    time_start[j] = parseInt( time_start[j] );
                    time_end[j]   = parseInt( time_end[j]   );
                }

                if ( time_period === 'PM' && time_start[0] !== 12 ) {
                    time_start[0] += 12;
                    time_end[0]   += 12;
                }

                time_end[0] += parseInt(duration / 60);
                time_end[1] += duration % 60;
                time_end[0] += parseInt(time_end[1] / 60);
                time_end[1] %= 60

                time['start']['hour']   = time_start[0];
                time['start']['minute'] = time_start[1];
                time['end']['hour']     = time_end[0];
                time['end']['minute']   = time_end[1];

                times += ' - ';

                if ( time['end']['hour'] > 12 ) {
                    times += (time['end']['hour'] - 12);
                }
                else {
                    times += time['end']['hour'];
                }
                
                if ( time['end']['minute'] < 10 ) {
                    times += ':0';
                }
                else {
                    times += ':';
                }

                times += time['end']['minute'];

                if ( time['end']['hour'] >= 12 ) {
                    times += ' PM';
                }
                else {
                    times += ' AM';
                }
            }

            let instructor = schedule_arr[i][5];
            let room       = schedule_arr[i][2];
            let color      = '';

            if ( subject in this.data.colors ) {
                color = this.data.colors[subject];
            }
            else {
                while ( color.length < 7 ) {
                    color = '#' + Math.floor(Math.random()*16777215).toString(16);
                }
                this.data.colors[subject] = color;
            }

            this.schedule[course]               = {};
            this.schedule[course]['course']     = course;
            this.schedule[course]['subject']    = subject;
            this.schedule[course]['section']    = section;
            this.schedule[course]['days']       = days_array;
            this.schedule[course]['time']       = time;
            this.schedule[course]['room']       = room;
            this.schedule[course]['instructor'] = instructor;
            this.schedule[course]['color']      = color;
            this.schedule[course]['days_f']     = days;
            this.schedule[course]['time_f']     = times;

            this.data.subjects[subject]       = true;
            this.data.courses[course]         = true;
            this.data.instructors[instructor] = true;
            this.data.rooms[room]             = true;
        }
    }

    getDisplaySchedule(filters = null) {
        var display_schedule = {
            Monday:    {},
            Tuesday:   {},
            Wednesday: {},
            Thursday:  {},
            Friday:    {}
        };

        for (var course in this.schedule) {
            for (var day in display_schedule) {
                if ( day in this.schedule[course]['days'] ) {
                    if ( filters && this.validFilters(filters) ) {
                        if ( this.schedule[course]['subject']    in filters.subjects    ||
                             this.schedule[course]['course']     in filters.courses     ||
                             this.schedule[course]['instructor'] in filters.instructors ||
                             this.schedule[course]['room']       in filters.rooms
                        ) {
                            display_schedule[day][course] = true;
                        }
                    }
                    else {
                        display_schedule[day][course] = true;
                    }
                }
            }
        }

        return display_schedule;
    }

    validFilters(filters) {
        for (var type in filters) {
            if ( ! window.$.isEmptyObject(filters[type]) ) {
                return true;
            }
        }
        return false;
    }

    openFilters() {
        this.setState({
            filters_active: ! this.state.filters_active,
            filters_helper: false
        });
    }

    changeFilters(new_filters) {
        this.setState({
            display_schedule: this.getDisplaySchedule(new_filters),
            filters_active: false,
            filters: new_filters
        });
    }

    render() {
        if ( this.state.display_schedule ) {
            return (
                <>
                    <div className="cs-table-header-wrapper">
                        <div className="cs-timetable-header">

                            {this.state.filters_helper ? 
                                <i className="fas fa-arrow-down cs-filters-arrow"></i>
                            :
                                null
                            }

                            <a className="cs-table-filter" href="#/" onClick={() => this.openFilters()}>
                                <i className="fas fa-filter"></i>
                            </a>
                        </div>
                        
                        <div className="cs-daytable-header">Monday    </div>
                        <div className="cs-daytable-header">Tuesday   </div>
                        <div className="cs-daytable-header">Wednesday </div>
                        <div className="cs-daytable-header">Thursday  </div>
                        <div className="cs-daytable-header">Friday    </div>

                        <CSSTransition
                            appear  = {true}
                            timeout = {300}
                            in      = {this.state.filters_active} >

                            <Filters
                                data     = {this.data}
                                callback = {this.callback} />
                        
                        </CSSTransition>
                    </div>

                    <div className="cs-table-wrapper">
                        <TimeTable />

                        <DayTable schedule={this.schedule} display={this.state.display_schedule} day={'Monday'}    />
                        <DayTable schedule={this.schedule} display={this.state.display_schedule} day={'Tuesday'}   />
                        <DayTable schedule={this.schedule} display={this.state.display_schedule} day={'Wednesday'} />
                        <DayTable schedule={this.schedule} display={this.state.display_schedule} day={'Thursday'}  />
                        <DayTable schedule={this.schedule} display={this.state.display_schedule} day={'Friday'}    />
                    </div>
                </>
            );
        }
        else {
            return ( <> </> );
        }
    }
}

