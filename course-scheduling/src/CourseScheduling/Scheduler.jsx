import React from 'react';

import ScheduleViewer from './ScheduleViewer/ScheduleViewer.jsx';
import PacmanLoad from 'react-spinners/PacmanLoader';


export default class Scheduler extends React.Component {
    constructor(props) {
        super(props);

        this.courses_file     = props.courses;
        this.instructors_file = props.instructors;

        this.courses     = null;
        this.instructors = null;

        this.state = {
            schedule: null,
            error: false
        };

        this.run_scheduler();
    }

    run_scheduler() {
        let _this = this;

        if ( _this.courses_file ) {
            let courses_reader = new FileReader();
            courses_reader.onload = function(e) {
                _this.courses = courses_reader.result;
                _this.received_file();
            }
            courses_reader.readAsText( _this.courses_file );
        }

        if ( _this.instructors_file ) {
            let instructors_reader = new FileReader();
            instructors_reader.onload = function(e) {
                _this.instructors = instructors_reader.result;
                _this.received_file();
            }
            instructors_reader.readAsText( _this.instructors_file );
        }
    }

    received_file() {
        let _this = this;

        if ( _this.courses && _this.instructors ) {            
            var form = new FormData();
            form.append("courses",     _this.courses);
            form.append("preferences", _this.instructors);
            
            var settings = {
                "url": "https://course-scheduling-jkelaty.herokuapp.com/schedule/",
                "method": "POST",
                "timeout": 0,
                "processData": false,
                "mimeType": "multipart/form-data",
                "contentType": false,
                "crossDomain": true,
                "data": form
            };
            
            window.$.ajax(settings)
                .done(function(response) {
                    _this.setState({
                        schedule: JSON.parse(response)
                    });
                })
                .fail(function(xhr, status, error) {
                    _this.setState({
                        error: true
                    });
                });
        }
    }

    render() {
        return (
            <>
                { this.state.error ?
                
                    <div className="cs-error">
                        <p>Uh oh! Something went wrong :(</p>
                        <p>Reload the app and try again</p>
                    </div>
                
                : this.state.schedule ?

                    <ScheduleViewer schedule = {this.state.schedule} />

                :

                    <div className="cs-loading">
                        <PacmanLoad size='50px' color='white' />
                    </div>
                }
            </>
        );
    }
}
