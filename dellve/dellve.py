from flask import Flask, render_template, json, jsonify, request
import requests
import jinja2
import os
import conf as c
import cf_deployment_tracker

app = Flask(__name__)

# Emit Bluemix deployment event
cf_deployment_tracker.track()

# CloudFoundry env
if os.getenv(c.CF_APP_ENV):
    port = int(os.getenv(c.CF_APP_ENV))
else:
    port = c.DEFAULT_PORT

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
    return render_template(c.INVALID_CONFIG_PAGE), 422

@app.route('/')
def get_portal_home():
    return render_template(c.HOME_PAGE)

@app.route('/system-overview', methods=['GET'])
def get_system_overview_page():
    validate_server_config(request.args)
    return apply_template(c.TEMPLATE_DIR + c.SYS_PAGE, request.args)

@app.route('/benchmarks', methods=['GET'] )
def get_benchmarks_page():
    # 1. Validate server config params
    validate_server_config(request.args)
    # 2. Get list of available benchmarks
    benchmarks = requests.get('http://' + str(request.args[c.SERVER_TAG]) + ':' + str(request.args[c.DELLVE_TAG]) + c.DVE_BENCH_LIST, timeout=c.DEFAULT_TIMEOUT).json()
    print ('Benchmarks: ', benchmarks)
    # 3. Restore proper start/stop controls, last detail panel, etc.
    run_detail = requests.get( "http://" + str(request.args[c.SERVER_TAG]) + ":" + str(request.args[c.DELLVE_TAG])  + c.DVE_PROGRESS, timeout=c.DEFAULT_TIMEOUT).json()
    print ('Last runtime detail: ', run_detail)
    # 4. Add template args
    mutable_dict = {}
    arg_tags = [ c.SERVER_TAG , c.NETDATA_TAG, c.DELLVE_TAG ]
    for tag in arg_tags:
        mutable_dict[tag] = request.args[tag]
    mutable_dict[c.BENCHMARK_TAG] = benchmarks
    mutable_dict[c.RUN_DETAIL_TAG] = run_detail
    return apply_template(c.TEMPLATE_DIR + c.BENCH_PAGE, mutable_dict)

# Helper proxy for get_progress polling (ajax rejects cross origin)
@app.route('/progress-proxy', methods=['GET'])
def progress_proxy():
    try:
        r = requests.get("http://" + request.args[c.URL_TAG] + c.DVE_PROGRESS, timeout=c.DEFAULT_TIMEOUT).json()
        print(r)
        return jsonify(r)
    except:
        raise InvalidServerConfig()

# Utility Function to raise error on invalid server config
def validate_server_config(params):
    try:
        url = 'http://' + str(params[c.SERVER_TAG]) + ':' + str(params[c.NETDATA_TAG]) + c.NETDATA_SUFFIX
        print(url)
        assert requests.get(url, timeout=c.DEFAULT_TIMEOUT).status_code == 200
        url = 'http://' + str(params[c.SERVER_TAG]) + ':' + str(params[c.DELLVE_TAG]) + c.DVE_BENCH_LIST
        print(url)
        assert requests.get(url, timeout=c.DEFAULT_TIMEOUT).status_code == 200
    except:
        raise InvalidServerConfig()

# Helper method for applying jinja templates
def apply_template(template_path, args):
    template_env = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.dirname(__file__) ) )
    template = template_env.get_template(template_path)
    t_vars = {}
    t_vars[ c.SERVER_TAG ] = str( args[ c.SERVER_TAG ] )
    t_vars[ c.NETDATA_TAG ] = str( args[ c.NETDATA_TAG ] )
    t_vars[ c.DELLVE_TAG ] = str( args[ c.DELLVE_TAG ] )
    try:
        t_vars[ c.RUN_DETAIL_TAG ] =  args[ c.RUN_DETAIL_TAG ]
        t_vars[ c.BENCHMARK_TAG ] =  args[ c.BENCHMARK_TAG ]
    except:
        dummy = True
    return template.render(t_vars)

if __name__ == "__main__":
    app.run(host=c.DEFAULT_HOST,port=port, debug=True)
