import React from 'react';

import Scheduler from './Scheduler.jsx'

import './CourseScheduling.scss';
import '../../node_modules/font-awesome/css/font-awesome.min.css';

import github_logo from '../Github-Mark.png';

export default class CourseScheduling extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      ready: false,
      courses: null,
      instructors: null
    };
  }

  verifyCourses() {
    let courses_file = document.getElementById('courses-file').files[0];

    if ( courses_file && courses_file.name.toLowerCase().endsWith('.csv') ) {
      this.setState({
        courses: courses_file
      });
    }
  }

  verifyInstructors() {
    let instructors_file = document.getElementById('preferences-file').files[0];

    if ( instructors_file && instructors_file.name.toLowerCase().endsWith('.csv') ) {
      this.setState({
        instructors: instructors_file
      });
    }
  }

  ready() {
    if ( this.state.courses && this.state.instructors ) {
      this.setState({
        ready: true
      });
    }
  }

  reset() {
    this.setState({
      ready: false,
      courses: null,
      instructors: null
    });
  }

  render() {
    return (
      <>
        { this.Header() }

        { this.state.ready ?

          <>
            { this.Reset() }

            <Scheduler courses = {this.state.courses} instructors = {this.state.instructors} />
          </>

        : this.StartPage() }
      </>
    );
  }

  Reset() {
    return (
      <>
        <a title="Reset" href="#/" onClick={() => this.reset()}>
          <div className="cs-reset">
            <i className="fas fa-undo" />
          </div>
        </a>
      </>
    );
  }

  Header() {
    return (
      <>
        <h1 className="cs-header">
          <a href="/course-scheduling">
            <i className="fas fa-graduation-cap cs-header-cap"></i>
            Course Scheduling
          </a>
        </h1>
  
        <div className="cs-project-info">
          <p className="cs-contributors">Contributors: Jonathan Kelaty, Manal Zneit</p>
  
          <p className="cs-project-link">
            <a href="https://github.com/jkelaty/course-scheduling" target="_blank" rel="noopener noreferrer">
              <span>GitHub</span>
              <img src={github_logo} alt="github-mark" />
            </a>
          </p>
        </div>
      </>
    );
  }

  StartPage() {
    return (
      <>
        <div className="cs-info-wrapper">
          <p className="cs-info">
            This is a supplemental visualization tool for our CSCI 350/761 Artificial
            Intelligence final project. Our project addresses the problem of course
            scheduling for universities as a Constraint Satisfaction Problem. Our
            objective when designing the interface for this project was to create a
            tool that can be practically used using readily available information
            provided by any institution. To use this tool, simply upload a CSV with course
            information and a CSV containing instructor's preferences for certain scheduling
            parameters. Sample CSVs and templates can be found below.
          </p>
  
          <div className="cs-upload">
            <label htmlFor="courses">Courses: </label>
            <input onChange={() => this.verifyCourses()} type="file" id="courses-file" name="courses" accept=".csv" />

            <br />
            <br />

            <a className="cs-file-download-link" href="./templates/sample-courses.csv" download>Sample CSV</a>
            <br />
            <a className="cs-file-download-link" href="./templates/template-courses.csv" download>Template CSV</a>

            <br />
            <br />

            <label htmlFor="preferences">Preferences: </label>
            <input onChange={() => this.verifyInstructors()} type="file" id="preferences-file" name="preferences" accept=".csv" />

            <br />
            <br />

            <a className="cs-file-download-link" href="./templates/sample-preferences.csv" download>Sample CSV</a>
            <br />
            <a className="cs-file-download-link" href="./templates/template-preferences.csv" download>Template CSV</a>

            <br />
            <br />
            
            { this.state.courses && this.state.instructors ?
              <input type="submit" onClick={() => this.ready()} />
            :
              <input type="submit" disabled /> }
          </div>
        </div>
      </>
    );
  }
}

