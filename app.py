from flask import Flask, render_template, json, jsonify, request, url_for, redirect, Response
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

@app.route('/')
def main():
    return render_template(HOME_PAGE)

@app.route('/system-overview', methods=['GET'])
def get_system_metrics():
    if dellve_enabled(request.args) and netdata_enabled(request.args):
        return apply_template(TEMPLATE_DIR + SYS_PAGE, request.args)
    else:
        return render_template(HOME_PAGE) # TODO: throw custom error page

@app.route('/benchmarks', methods=['GET'] )
def get_benchmark_page():
    mutable_dict = {}
    dellve_verified = True
    try:
        # 1. get list of benchmarks
        benchmarks = requests.get('http://' + str(request.args[SERVER_TAG]) + ':' + str(request.args[DELLVE_TAG]) + DVE_BENCH_LIST).json()
        print ('Benchmarks: ', benchmarks)
        # 2. Restore proper start/stop controls, last detail panel,
        #    last user-selected benchmark, and progress bar
        run_detail = requests.get( "http://" + str(request.args[SERVER_TAG]) + ":" + str(request.args[DELLVE_TAG])  + DVE_PROGRESS).json()
        print ('Last runtime detail: ', run_detail)
        # 3. Add args to template
        arg_tags = [ SERVER_TAG , NETDATA_TAG, DELLVE_TAG ]
        for tag in arg_tags:
            mutable_dict[tag] = request.args[tag]
        mutable_dict[BENCHMARK_TAG] = benchmarks
        mutable_dict[RUN_DETAIL_TAG] = run_detail
    except:
        print ('Unable to create dynamic benchmark list')
        dellve_verified = False
    # 4. Verify netdata enabled and render appropriate page
    if dellve_verified and netdata_enabled(request.args):
        return apply_template(TEMPLATE_DIR + BENCH_PAGE, mutable_dict)
    else:
        return render_template(HOME_PAGE) # TODO: throw custom error

# Helper proxy for get_progress polling (ajax rejects cross origin)
@app.route('/progress-proxy', methods=['GET'])
def get_progress_proxy():
    r = requests.get( "http://" + request.args[URL_TAG]  + DVE_PROGRESS).json()
    return jsonify(r)

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

# Helper Function to determine whether a server has
# a proper netdata installation and netdata plugin
def netdata_enabled(params):
    url = 'http://' + str(params[SERVER_TAG]) + ':' + str(params[NETDATA_TAG]) + NETDATA_SUFFIX
    return valid_api_endpoint(url)

# Helper Function to determine whether a server has
# the proper dellve dependencies and listening api
def dellve_enabled(params):
    url = 'http://' + str(params[SERVER_TAG]) + ':' + str(params[DELLVE_TAG]) + DVE_BENCH_LIST
    return valid_api_endpoint(url)

# Helper function to test for existence of HTTP endpoint
def valid_api_endpoint(url):
    try:
        r = requests.get(url)
        return True
    # Destination not found
    except:
        return False

if __name__ == "__main__":
    app.run(host=DEFAULT_HOST,port=port, debug=True)
