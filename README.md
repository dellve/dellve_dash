# DellVE Dash :sparkles: :tada: :rocket: :metal: :octocat:
Front-end application to accompany the DellVE Benchmark Suite  

Author: Abigail Johnson  
Live: http://dellve-dash.mybluemix.net/ 

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

## Deployment
This application uses a continuous delivery pipeline. Whenever an approved commit has been made to the master branch, the application will be automatically redeployed to the dellve-dash instance on Bluemix.

To deploy this application to a seperate Bluemix instance, follow the instructions below:  

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
    - [x] Remove server config whitelist and implement home form verification    
    - [x] Attach dellve API endpoint to run config form (start/stop buttons)     
    - [x] Add progress bar/long polling functionality
    - [ ] Ensure proper reinitialization of run panel on page return     
        -- ( if user leaves benchmark page in middle of run, ensure stop button and proper benchmark progress is displayed if the benchmark is still running by the time they return )  
    - [ ] Add benchmark detail panel (expand on benchmark progress complete)  

#### Vanity
    - [ ] (maybe) Add minimizer control snippet to run config and detail panels
    - [ ] Fix styling!
        - [ ] fix css to properly adapt mobile and make uniform across browsers (looks like shit in safari)  
        - [ ] Unify DellVE logo alignment amongst pages
        - [ ] margins  
        - [ ] extract css from html   
        - [ ] remove excess styling  
    - [ ] About section
    - [ ] Throw custom error page and/or display alert modal on invalid server config input (currently re-renders portal home on error )

#### Other Future improvements
    - [ ] Refactor views into modular React components

## Note
Application must be accessed via http instead of https for netdata dependencies to load
