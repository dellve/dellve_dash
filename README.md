# DellVE Dash
Front-end application to accompany the DellVE Benchmark Suite  
Author: Abigail Johnson
Live: https://dellve-dash.mybluemix.net/

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
#### Prerequisites
You'll need the following:
* [Bluemix account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

#### Deploying to Bluemix
[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy)
or....
```
cf api https://api.ng.bluemix.net
cf login
cf push
```
This can take a minute. If there is an error in the deployment process you can use the command `cf logs <Your-App-Name> --recent` to troubleshoot.
When deployment completes you should see a message indicating that your app is running.  View your app at the URL listed in the output of the push command.  You can also issue the
  ```
cf apps
  ```
command to view your apps status and see the URL.

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
