import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from dellve import dellve
from urllib.request import urlopen
from flask import Flask
from flask_testing import LiveServerTestCase

# TODO: use mock and extract these constants
valid_config = '?server=10.157.26.8&netdata_port=5555&dellve_port=9999'
invalid_config = '?'

# Testing with LiveServer
# TODO: Expand on tests (assert more than status code)
class BasicTest(LiveServerTestCase):
    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0
        return app

    def setUp(self):
        dellve.app.config['TESTING'] = True
        self.app = dellve.app.test_client()

    # Basic test case - go to portal home
    def test_portal_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_benchmark_invalid_config(self):
        response = self.app.get('/benchmarks' + invalid_config ) # no server params supplied
        self.assertEqual(response.status_code, 422)

    def test_benchmark_valid_config(self):
        response = self.app.get('/benchmarks' + valid_config)
        self.assertEqual(response.status_code, 200)

    def test_system_overview(self):
        response = self.app.get('/system-overview' + valid_config)
        self.assertEqual(response.status_code, 200)

    def test_invalid_progress_proxy(self):
        response = self.app.get('/progress-proxy' + invalid_config ) # no server config
        self.assertEqual(response.status_code, 422)

    def test_valid_progress_proxy(self):
        response = self.app.get('/progress-proxy?url_base=10.157.26.8:9999')
        self.assertEqual(response.status_code, 200)
