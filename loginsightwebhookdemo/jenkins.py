#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# Parameters
JENKINSURL = ''
# Only required if not passed
JOBNAME = ''
TOKEN = ''


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/jenkins", methods=['POST'])
@app.route("/endpoint/jenkins/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/jenkins/<JOBNAME>/<TOKEN>", methods=['POST'])
@app.route("/endpoint/jenkins/<JOBNAME>/<TOKEN>/<ALERTID>", methods=['PUT'])
def jenkins(ALERTID=None, JOBNAME=None, TOKEN=None):
    """
    If called, run a Jenkins job without parameters -- request results are discarded.
    Requires `JENKINSURL defined in the form `https://jenkins.domain.com`.
    If `JOBNAME` and `TOKEN` are not passed then the must be defined
    For more information, see https://wiki.jenkins-ci.org/display/JENKINS/Remote+access+API
    """
    if not JENKINSURL or not JOBNAME or not TOKEN:
        return ("Parameters must be set, please edit the shim!", 500, None)

    # We need to make the Jenkins URL
    URL = JENKINSURL + "/job/" + JOBNAME + "/build?token=" + TOKEN

    # No need to parse the request as we just want to run a job
    #a = parse(request)
    #payload = {
    #    "body": a['info'],
    #    "title": a['AlertName'],
    #    "type": "link",
    #    "url": a['url'],
    #}
    payload = ''

    headers = ''

    if headers:
        return callapi(URL, json.dumps(payload), headers)
    else:
        return callapi(URL, json.dumps(payload))
