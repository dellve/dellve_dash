# DellVE Dash :sparkles: :tada: :dancer: :princess: :metal: :fire:
[![Build Status](https://travis-ci.org/dellve/dellve-dash.svg?branch=master)](https://travis-ci.org/dellve/dellve-dash)  
Front-end application to accompany the DellVE Benchmark Suite  

Author: Abigail Johnson  
Live: http://dellve-dash.mybluemix.net/

## 1.0 Features
#### 1.1 Portal Home
+ Connect to visual dashboard of any DellVE enabled server  
#### 1.2 System Overview
+ Real time system monitoring, interactive graphs, and alerts
#### 1.3 Benchmarks
+ Start, stop, and monitor the progress of any DellVE benchmark
+ View real-time monitoring of system GPUs (nvidia)

## 2.0 Backend Dependencies
To utilize DellVE Dash, the server configuration you enter into Portal Home must be equipped with the following:   
### 2.1 Netdata Dependencies
#### 2.1.1 Base Install (CentOS on default port 19999)
```
curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata-all    
git clone https://github.com/firehol/netdata.git --depth=1    
cd netdata   
./netdata-installer.sh    
```
#### 2.1.2 Nvidia GPU Profiler Extension
```
cd /tmp/  
git clone https://github.com/Splo0sh/netdata_nv_plugin --depth 1  
sudo cp netdata_nv_plugin/nv.chart.py /usr/libexec/netdata/python.d/  
sudo cp netdata_nv_plugin/python_modules/pynvml.py /usr/libexec/netdata/python.d/python_modules/  
sudo cp netdata_nv_plugin/nv.conf /etc/netdata/python.d/
```   

For further information/details on how to install the netdata dependencies on other systems, visit <https://github.com/firehol/netdata/wiki/Installation>, <https://github.com/coraxx/netdata_nv_plugin>  

### 2.2 DellVE Benchmark Suite
See <https://github.com/dellve/dellve_benchend>

## 3.0 Installation (Local)
```
git clone https://github.com/dellve/dellve-dash  
cd dellve-dash  
pip3 install -r requirements.txt  
python3 dellve/dellve.py
```

## 4.0 Deployment
This application uses a continuous delivery pipeline. Whenever an approved commit has been made to the master branch, the application will be automatically redeployed to the dellve-dash instance on Bluemix.

To deploy this application to a seperate Bluemix instance, follow the instructions below:  

#### 4.1 Prerequisites
You'll need the following:
* [Bluemix account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

#### 4.2 Deploying to Bluemix
From the Bluemix Dashboard:    
[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy)   
or, from the command line:     
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

## 5.0 Testing
TODO

## 6.0 License
TODO

## 7.0 TODOs
#### 7.1 Functional
    - [x] Remove server config whitelist and implement home form verification    
    - [x] Attach dellve API endpoint to run config form (start/stop buttons)     
    - [x] Add progress bar/long polling functionality
    - [x] Continuous Integration build/deploy
    - [...] Ensure proper reinitialization of run panel on page return     
        -- ( if user leaves benchmark page in middle of run, ensure stop button and proper benchmark progress is displayed if the benchmark is still running by the time they return )  
    - [...] Add benchmark detail panel (expand on benchmark progress complete)  
    - [ ] Python unit tests
    - [ ] Interaction/js tests
    - [ ] Change runtime/build to python2.7
    - [ ] Ensure only user who starts benchmark can stop it ( likely need to do on backend to prevent injection)  

#### 7.2 Vanity
    - [ ] (maybe) Add minimizer control snippet to run config and detail panels
    - [...] Fix styling!
        - [...] fix css to properly adapt mobile and make uniform across browsers (looks like shit in safari)  
        - [ ] Unify DellVE logo alignment amongst pages
        - [...] margins  
        - [ ] extract css from html   
        - [ ] remove excess styling  
    - [ ] About section
    - [x] Throw custom error page and/or display alert modal on invalid server config input (currently re-renders portal home on error )  
    - [ ] Export Run Detail

#### 7.3 Other Future improvements
    - [...] Refactor views into modular React components

## 8.0 Notes
+ Application must be accessed via http instead of https for netdata dependencies to load  
