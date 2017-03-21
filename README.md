# DellVE Dash
Front-end application to accompany the DellVE Benchmark Suite
Author: Abigail Johnson

## Features
  Portal Home
	Connect to visual dashboard of any DellVE enabled server
  System Overview
	Real time system monitoring, interactive graphs, and alerts
  Benchmarks
	Start, stop, and monitor the progress of any DellVE benchmark
	View real-time monitoring of system GPUs (nvidia)

## Run the app locally
1. [Install Python][]
+ cd into this project's root directory
+ Run `pip install -r requirements.txt` to install the app's dependencies
+ Run `python app.py`
+ Access the running app in a browser at <http://localhost:5000>

## TODOs
-Attach dellve API endpoint to run config form
-Some styling (slider tick white; margins; extract css from html; remove excess styling)
-About section
-Remove server config whitelist and implement home form verification
