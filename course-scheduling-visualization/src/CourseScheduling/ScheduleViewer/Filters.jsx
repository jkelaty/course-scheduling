import React from 'react';

import Select from 'react-select';


export default class Filters extends React.Component {
    constructor(props) {
        super(props);

        this.callback = props.callback;
        this.data     = props.data;

        this.subjects    = this.getOptions('subjects');
        this.courses     = this.getOptions('courses');
        this.instructors = this.getOptions('instructors');
        this.rooms       = this.getOptions('rooms');

        this.state = {
            subjects:    null,
            courses:     null,
            instructors: null,
            rooms:       null
        };

        this.subjectsChange    = this.handleSubjectsChange.bind(this);
        this.coursesChange     = this.handleCoursesChange.bind(this);
        this.instructorsChange = this.handleInstructorsChange.bind(this);
        this.roomsChange       = this.handleRoomsChange.bind(this);
    }

    getOptions(option) {
        var options = []

        for (var instructor in this.data[option]) {
            options.push({
                type:  option,
                value: instructor,
                label: instructor
            });
        }

        return options;
    }

    applyFilters() {
        var filters = {
            subjects:    {},
            courses:     {},
            instructors: {},
            rooms:       {}
        };

        for (var type in filters) {
            if ( this.state[type] ) {
                for (let i = 0; i < this.state[type].length; ++i) {
                    filters[type][this.state[type][i].label] = true;
                }
            }
        }

        this.callback(filters);
    }

    handleSubjectsChange(new_filters) {
        this.setState({
            subjects: new_filters
        });
    }

    handleCoursesChange(new_filters) {
        this.setState({
            courses: new_filters
        });
    }

    handleInstructorsChange(new_filters) {
        this.setState({
            instructors: new_filters
        });
    }

    handleRoomsChange(new_filters) {
        this.setState({
            rooms: new_filters
        });
    }

    render() {
        return (
            <>
                <div className="cs-filters-wrapper">

                    <label className="cs-filters-label" htmlFor="cs-filters-subjects">Subjects:</label>
                    <Select
                        className="cs-filters-filter"
                        id="cs-filters-subjects"
                        value={this.state.subjects}
                        isMulti={true}
                        options={this.subjects}
                        onChange={this.subjectsChange}
                    />

                    <br />

                    <label className="cs-filters-label" htmlFor="cs-filters-courses">Courses:</label>
                    <Select
                        className="cs-filters-filter"
                        id="cs-filters-courses"
                        value={this.state.courses}
                        isMulti={true}
                        options={this.courses}
                        onChange={this.coursesChange}
                    />

                    <br />

                    <label className="cs-filters-label" htmlFor="cs-filters-instructors">Instructors:</label>
                    <Select
                        className="cs-filters-filter"
                        id="cs-filters-instructors"
                        value={this.state.instructors}
                        isMulti={true}
                        options={this.instructors}
                        onChange={this.instructorsChange}
                    />

                    <br />

                    <label className="cs-filters-label" htmlFor="cs-filters-rooms">Rooms:</label>
                    <Select
                        className="cs-filters-filter"
                        id="cs-filters-rooms"
                        value={this.state.rooms}
                        isMulti={true}
                        options={this.rooms}
                        onChange={this.roomsChange}
                    />

                    <br />
                    <br />

                    <button className="cs-filters-apply" onClick={() => this.applyFilters()}>Apply</button>
                </div>
            </>
        );
    }
}

