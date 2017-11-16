#!/usr/bin/env python

import os, sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements

try:
    from loginsightwebhookdemo import __version__ as loginsightwebhookdemoversion  # TODO Replace with a static variant?
except ImportError:
    loginsightwebhookdemoversion = "0.dev0"

# Hack from https://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool
# parse_requirements() returns generator of pip.req.InstallRequirement objects
try:
    if os.environ['PYTHONPATH']:
        HDIR = os.environ['PYTHONPATH']
except:
    try:
        if os.environ['TRAVIS_BUILD_DIR']:
            HDIR = os.environ['TRAVIS_BUILD_DIR']
    except:
        HDIR = '.'
install_reqs = parse_requirements(HDIR + '/requirements.txt', session='hack')
test_reqs = parse_requirements(HDIR + '/test-requirements.txt', session='hack')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]
treqs = [str(ir.req) for ir in test_reqs]

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]
    description = "Run tests in the current environment"

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.args = []

    def run(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest

        try:
            args = shlex.split(self.args)
        except AttributeError:
            args = []
        errno = pytest.main(args)
        sys.exit(errno)


class ToxTest(TestCommand):
    user_options = [('tox-args=', "t", "Arguments to pass to pytest")]
    description = "Run tests in all configured tox environments"

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.args = []

    def run(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        from tox.__main__ import main

        try:
            args = shlex.split(self.args)
        except AttributeError:
            args = []
        errno = main(args)
        sys.exit(errno)

setup(
    name='loginsightwebhookdemo',
    version=loginsightwebhookdemoversion,
    url='http://github.com/vmw-loginsight/loginsightwebhookdemo/',
    license='Apache Software License 2.0',
    author='Steve Flanders',
    install_requires=reqs,
    tests_require=treqs,
    description='VMware vRealize Log Insight Webhook Shim',
    author_email='stevefl@vmware.com',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'li = loginsightwebhookdemo.__init__:main'
        ]
    },
    cmdclass={'test': PyTest, 'tox': ToxTest}
)
