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
    }

    componentDidMount() {
        this.read_in_files();
    }

    read_in_files() {
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

        if ( this.courses && this.instructors ) {

            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    courses: this.courses,
                    preferences: this.instructors
                })
            };
            
            fetch('https://course-scheduling-jkelaty.herokuapp.com/schedule', requestOptions)
                .then(response => response.text())
                .then((job_id) => {
                    _this.ping_scheduler(job_id.replace('rq:job:', ''));
                })
                .catch(error => {
                    _this.setState({
                        error: true
                    });
                });
        }
    }

    ping_scheduler(job_id) {
        let _this = this;

        fetch('https://course-scheduling-jkelaty.herokuapp.com/schedule/' + job_id, { method: 'Get' })
            .then(response => response.text())
            .then((res) => {
                if ( res === 'Not yet' ) {
                    setTimeout(function() {
                        _this.ping_scheduler(job_id);
                    }, 3000);
                }
                else {
                    _this.setState({
                        schedule: JSON.parse(res)
                    });
                }
            })
            .catch(error => {
                this.setState({
                    error: true
                });
            });
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

