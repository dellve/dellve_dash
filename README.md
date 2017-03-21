# DellVE Dash
Front-end application to accompany the DellVE Benchmark Suite  
Author: Abigail Johnson

## Features
#### Portal Home
+ Connect to visual dashboard of any DellVE enabled server  
#### System Overview
+ Real time system monitoring, interactive graphs, and alerts
#### Benchmarks
+ Start, stop, and monitor the progress of any DellVE benchmark
+ View real-time monitoring of system GPUs (nvidia)

## Installation
1. To run the project locally
+ cd into this project's root directory
+ Run `pip3 install -r requirements.txt` to install the app's dependencies
+ Run `python3 app.py`
+ Access the running app in a browser at <http://localhost:5000>

## Deployment
TODO

## License
TODO

## TODOs
#### Functional
    - Attach dellve API endpoint to run config form
    - Add progress/detail panel to Benchmarks page (under run config)
    - Remove server config whitelist and implement home form verification
#### Vanity
    - (maybe) Add minimizer control snippet to run config and detail panels
    - Fix styling!
        -- fix css to properly adapt mobile and make uniform across browsers (looks like shit in safari)  
        -- slider tick detail white  
        -- margins  
        -- extract css from html   
        -- remove excess styling  
    - About section
    - Throw custom error page and/or display alert modal on invalid server config input (currently re-renders portal home on error )
    - Refactor views into modular React components
