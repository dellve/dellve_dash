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
RUN_DETAIL_TAG = 'run_detail'

GPU_CHARTS_TAG = 'gpu_charts'
GPU_CHARTS = [ {'title' : 'Load (% GPU and Mem Utilization)' , 'source': 'nv.load' },
                    {'title' : 'Memory', 'source': 'nv.memory' },
                    {'title' : 'Temperature', 'source': 'nv.temperature' },
                    {'title' : 'Frequency', 'source': 'nv.frequency' },
                    {'title' : 'ECC Errors', 'source': 'nv.ecc_errors' } ]


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
