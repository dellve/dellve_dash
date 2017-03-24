import os

##############################################
#       Application Constants
##############################################

# Query Params and template variable names
SERVER_TAG = 'server'
DELLVE_TAG = 'dellve_port'
NETDATA_TAG = 'netdata_port'
BENCHMARK_TAG = 'benchmarks'
URL_TAG = 'url_base'
PROGRESS_TAG = 'progress'
RUN_DETAIL_TAG = 'run_detail'

# External API Endpoints used for dependency verification and form submission
NETDATA_SUFFIX = '/api/v1/charts/data?chart=netdata.plugin_pythond_nv'
DVE_BENCH_LIST = '/benchmark/'# TODO: ammend as API is determined

# Local/Bluemix Deployment
DEFAULT_PORT = 8080
DEFAULT_HOST = '0.0.0.0'
CF_APP_ENV = 'VCAP_APP_PORT'

# Templates
TEMPLATE_DIR = 'templates/'
HOME_PAGE = 'portal_home.html'
SYS_PAGE = 'system_metrics.html'
BENCH_PAGE = 'benchmark.html'
