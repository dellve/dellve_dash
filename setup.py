from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Dependencies
requires = [
    "Flask==0.11.1",
    "cf-deployment-tracker==1.0.2"
]

setup(
    name='dellve-dash',
    version='1.0.0',
    author='Abigail M. Johnson',
    author_email='abigailjohnson@utexas.edu',
    description='Front-end application to accompany the DellVE Benchmark Suite',
    long_description=long_description,
    url='https://github.com/dellve/dellve-dash',
    #url='http://dellve-dash.mybluemix.net',
    install_requires=requires
)
