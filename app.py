from flask import Flask, render_template, json, jsonify, request
import requests
import jinja2
import os
from conf import *
import cf_deployment_tracker

app = Flask(__name__)

# Emit Bluemix deployment event
cf_deployment_tracker.track()

# CloudFoundry env
if os.getenv(CF_APP_ENV):
    port = int(os.getenv(CF_APP_ENV))
else:
    port = DEFAULT_PORT

# Class to handle invalid server configurations provided via forms or direct HTTP requests
# Def Invalid Config:
#    - Missing required config params ( dellve_port, netdata_port, server_ip )
#    - Given config params missing required dependencies
#        - DellVE api not installed/visable
#        - Netdata or nvidia pluggin not installed/visable
class InvalidServerConfig(Exception):
    status_code = 422 # Unprocessable Response
    def __init__(self):
        Exception.__init__(self)
        self.message = "Invalid Server Configuration"
        
# Show invalid server config page on invalid server config
@app.errorhandler(InvalidServerConfig)
def handle_invalid_server_config(error):
    return render_template(INVALID_CONFIG_PAGE)

@app.route('/')
def get_portal_home():
    return render_template(HOME_PAGE)

@app.route('/system-overview', methods=['GET'])
def get_system_overview_page():
    validate_server_config(request.args)
    return apply_template(TEMPLATE_DIR + SYS_PAGE, request.args)

@app.route('/benchmarks', methods=['GET'] )
def get_benchmarks_page():
    # 1. Validate server config params
    validate_server_config(request.args)
    # 2. Get list of available benchmarks
    benchmarks = requests.get('http://' + str(request.args[SERVER_TAG]) + ':' + str(request.args[DELLVE_TAG]) + DVE_BENCH_LIST, timeout=DEFAULT_TIMEOUT).json()
    print ('Benchmarks: ', benchmarks)
    # 3. Restore proper start/stop controls, last detail panel, etc.
    run_detail = requests.get( "http://" + str(request.args[SERVER_TAG]) + ":" + str(request.args[DELLVE_TAG])  + DVE_PROGRESS, timeout=DEFAULT_TIMEOUT).json()
    print ('Last runtime detail: ', run_detail)
    # 4. Add template args
    mutable_dict = {}
    arg_tags = [ SERVER_TAG , NETDATA_TAG, DELLVE_TAG ]
    for tag in arg_tags:
        mutable_dict[tag] = request.args[tag]
    mutable_dict[BENCHMARK_TAG] = benchmarks
    mutable_dict[RUN_DETAIL_TAG] = run_detail
    return apply_template(TEMPLATE_DIR + BENCH_PAGE, mutable_dict)

# Helper proxy for get_progress polling (ajax rejects cross origin)
@app.route('/progress-proxy', methods=['GET'])
def progress_proxy():
    try:
        r = requests.get("http://" + request.args[URL_TAG]  + DVE_PROGRESS, timeout=DEFAULT_TIMEOUT).json()
        return jsonify(r)
    except:
        raise InvalidServerConfig()

# Utility Function to raise error on invalid server config
def validate_server_config(params):
    try:
        url = 'http://' + str(params[SERVER_TAG]) + ':' + str(params[NETDATA_TAG]) + NETDATA_SUFFIX
        assert requests.get(url, timeout=DEFAULT_TIMEOUT).status_code == 200
        url = 'http://' + str(params[SERVER_TAG]) + ':' + str(params[DELLVE_TAG]) + DVE_BENCH_LIST
        assert requests.get(url, timeout=DEFAULT_TIMEOUT).status_code == 200
    except:
        raise InvalidServerConfig()

# Helper method for applying jinja templates
def apply_template(template_path, args):
    template_env = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.dirname(__file__) ) )
    template = template_env.get_template(template_path)
    t_vars = {}
    t_vars[ SERVER_TAG ] = str( args[ SERVER_TAG ] )
    t_vars[ NETDATA_TAG ] = str( args[ NETDATA_TAG ] )
    t_vars[ DELLVE_TAG ] = str( args[ DELLVE_TAG ] )
    try:
        t_vars[ RUN_DETAIL_TAG ] =  args[ RUN_DETAIL_TAG ]
        t_vars[ BENCHMARK_TAG ] =  args[ BENCHMARK_TAG ]
    except:
        dummy = True
    return template.render(t_vars)

if __name__ == "__main__":
    app.run(host=DEFAULT_HOST,port=port, debug=True)
