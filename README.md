# DellVE Dash
Front-end application to accompany the DellVE Benchmark Suite  
Author: Abigail Johnson

## 1.0 Features
#### Portal Home
+ Connect to visual dashboard of any DellVE enabled server  
#### System Overview
+ Real time system monitoring, interactive graphs, and alerts
#### Benchmarks
+ Start, stop, and monitor the progress of any DellVE benchmark
+ View real-time monitoring of system GPUs (nvidia)

## 2.0 Run the app locally
1. [Install Python]
+ cd into this project's root directory
+ Run `pip install -r requirements.txt` to install the app's dependencies
+ Run `python app.py`
+ Access the running app in a browser at <http://localhost:5000>

## 3.0 TODOs
#### Functional
    - Attach dellve API endpoint to run config form
    - Add progress/detail panel to Benchmarks page (under run config)
    - Remove server config whitelist and implement home form verification
#### Vanity
    - (maybe) Add minimizer control snippet to run config and detail panels
    - Some styling (slider tick detail white; margins; extract css from html; fix css to properly adapt mobile; remove excess styling)
    - About section
    - Refactor views into modular React components
