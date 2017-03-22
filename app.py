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
    if valid_config_params( args ):
        return apply_template(TEMPLATE_DIR + SYS_PAGE, args)
    # TODO: throw custom error page
    else:
        return render_template(HOME_PAGE)

@app.route('/benchmarks', methods=['GET'] )
def get_benchmark_page():
    args = request.args
    if valid_config_params( args ):
        return apply_template(TEMPLATE_DIR + BENCH_PAGE, args)
    # TODO: throw custom error page
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
    return template.render(t_vars)

# Verify that user provided server configuration has
# a proper dellve installation and dependecies
def valid_config_params(params):
    return True if dellve_enabled(params) and netdata_enabled(params) else False

# Helper Function to determine whether a server has
# a proper netdata installation and netdata plugin
def netdata_enabled(params):
    url = 'http://' + str(params[SERVER_TAG]) + ':' + str(params[NETDATA_TAG]) + NETDATA_SUFFIX
    print(url)
    return valid_api_endpoint(url)

# Helper Function to determine whether a server has
# a proper netdata
def dellve_enabled(params):
    return True # TODO: uncomment once API deployed
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
