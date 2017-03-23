from flask import Flask, render_template, json, jsonify, request, url_for, redirect
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

@app.route('/system_metrics', methods=['GET'])
def get_system_metrics():
    args = request.args
    if dellve_enabled(args) and netdata_enabled(args):
        return apply_template(TEMPLATE_DIR + SYS_PAGE, args)
    # TODO: throw custom error page
    else:
        return render_template(HOME_PAGE)

@app.route('/benchmarks', methods=['GET'] )
def get_benchmark_page():
    args = request.args
    mutable_dict = {}
    dellve_verified = True
    try:
        # get list of benchmarks
        url = 'http://' + str(args[SERVER_TAG]) + ':' + str(args[DELLVE_TAG]) + DVE_BENCH_LIST
        benchmarks = requests.get(url).json()
        print( 'Benchmarks: ', benchmarks )
        arg_tags = [ SERVER_TAG , NETDATA_TAG, DELLVE_TAG ]
        # can't append benchmarks to args directly (immutable), so copy data over
        for tag in arg_tags:
            mutable_dict[tag] = args[tag]
        mutable_dict[BENCHMARK_TAG] = benchmarks
    except:
        print('Unable to create dynamic benchmark list')
        dellve_verified = False
    # Verify netdata enabled and return appropriate page
    # TODO: throw custom error
    if dellve_verified and netdata_enabled(args):
        return apply_template(TEMPLATE_DIR + BENCH_PAGE, mutable_dict)
    else:
        return render_template(HOME_PAGE)

# Helper method for applying jinja templates
def apply_template(template_path, args):
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader( os.path.dirname(__file__) ) )
    template = template_env.get_template(template_path)
    t_vars = {}
    t_vars[ SERVER_TAG ] = str( args[ SERVER_TAG ] )
    t_vars[ NETDATA_TAG ] = str( args[ NETDATA_TAG ] )
    t_vars[ DELLVE_TAG ] = str( args[ DELLVE_TAG ] )
    try:
        t_vars[ BENCHMARK_TAG ] = args[ BENCHMARK_TAG ]
    # Not all templates pass benchmarks; dummy exception
    except:
        dummy = True
    return template.render(t_vars)

# Helper Function to determine whether a server has
# a proper netdata installation and netdata plugin
def netdata_enabled(params):
    url = 'http://' + str(params[SERVER_TAG]) + ':' + str(params[NETDATA_TAG]) + NETDATA_SUFFIX
    print(url)
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
