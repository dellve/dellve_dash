import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
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
    "cf-deployment-tracker==1.0.2",
    "pytest-flask==0.10.0",
    "coverage==4.1",
    "pytest==2.9.2",
    "pytest-cov==2.3.0",
    "Flask-Testing>=0.6.2"
]

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--strict',
            '--verbose',
            '--tb=long',
            'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='dellve-dash',
    version='1.0.0',
    author='Abigail M. Johnson',
    author_email='abigailjohnson@utexas.edu',
    description='Front-end application to accompany the DellVE Benchmark Suite',
    long_description=long_description,
    packages='dellve',
    include_package_data=True,
    package_data= {'dellve': ['templates/**', 'static/*/*']},
    url='https://github.com/dellve/dellve-dash',
    install_requires=requires,
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest},
    test_suite='tests.test_test',
    extras_require={'testing': ['pytest'],}
)
