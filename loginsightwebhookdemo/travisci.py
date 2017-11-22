#!/usr/bin/env python


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# Parameters
TRAVISCIURL = 'https://api.travis-ci.org/repo/'
# Only required if not passed in URL
TRAVISCITOKEN = ''
TRAVISCIREPO = ''
TRAVISCIBRANCH = ''


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/travisci", methods=['POST'])
@app.route("/endpoint/travisci/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/travisci/<TOKEN>", methods=['POST'])
@app.route("/endpoint/travisci/<TOKEN>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/travisci/<TOKEN>/<REPO>", methods=['POST'])
@app.route("/endpoint/travisci/<TOKEN>/<REPO>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/travisci/<TOKEN>/<REPO>/<BRANCH>", methods=['POST'])
@app.route("/endpoint/travisci/<TOKEN>/<REPO>/<BRANCH>/<ALERTID>", methods=['PUT'])
def travisci(ALERTID=None, TOKEN=None, REPO=None, BRANCH=None):
    """
    If called, run a Travis CI job.
    If `TOKEN`, `REPO`, and/or `BRANCH` are not passed then the must be defined
    For more information, see https://docs.travis-ci.com/user/triggering-builds
    """
    if (not TRAVISCIURL or (not TRAVISCITOKEN and not TOKEN) or (not TRAVISCIREPO and not REPO) or (not TRAVISCIBRANCH and not BRANCH)):
        return ("TRAVISCI* parameters must be set, please edit the shim!", 500, None)
    # Prefer tokens over passwords
    if not TOKEN:
        TOKEN = TRAVISCITOKEN
    if not REPO:
        REPO = TRAVISCIREPO
    if not BRANCH:
        BRANCH = TRAVISCIBRANCH

    a = parse(request)

    payload = {
        "request": {
            "message": "Override the commit message: this is an api request",
            "branch": BRANCH,
            "token": TOKEN
        }
    }

    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Accept': 'application/vnd.travis-ci.2+json',
        'Client': 'LogInsight/1.0',
        'Authorization': 'token ' + TOKEN,
        'Travis-API-Version': '3'
    }

    return callapi(TRAVISCIURL + REPO + '/requests', 'post', json.dumps(payload), headers)
