#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# Parameters
PIVOTALTRACKERURL = 'https://www.pivotaltracker.com/services/v5/projects/'
# Only required if not passed in URL
PIVOTALTRACKERTOKEN = ''
PIVOTALTRACKERPROJECT = ''


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/pivotaltracker", methods=['POST'])
@app.route("/endpoint/pivotaltracker/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/pivotaltracker/<TOKEN>", methods=['POST'])
@app.route("/endpoint/pivotaltracker/<TOKEN>/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/pivotaltracker/<TOKEN>/<PROJECT>", methods=['POST'])
@app.route("/endpoint/pivotaltracker/<TOKEN>/<PROJECT>/<ALERTID>", methods=['POST','PUT'])
def pivotaltracker(ALERTID=None, TOKEN=None, PROJECT=None):
    """
    Create a new bug for every incoming webhook that does not already have an existing one.
    If a bug already exists, do nothing.
    Uniqueness is determined by the incoming webhook alert name.
    Requires PIVOTALTRACKER* parameters to be defined.
    """
    if (not PIVOTALTRACKERURL or (not PIVOTALTRACKERTOKEN and not TOKEN) or (not PIVOTALTRACKERPROJECT and not PROJECT)):
        return ("PIVOTALTRACKER* parameters must be set, please edit the shim!", 500, None)
    if not PROJECT:
        TOKEN = PIVOTALTRACKERTOKEN
        PROJECT = PIVOTALTRACKERPROJECT

    a = parse(request)

    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {'Content-type': 'application/json', 'X-TrackerToken': TOKEN}

    # Get the list of open bugs that contain the AlertName from the incoming webhook
    bug = callapi(PIVOTALTRACKERURL + PROJECT + '/stories?filter=name:"' + a['AlertName'] + '"', 'get', None, headers, None)
    try:
        b = json.loads(bug)
    except:
        return bug

    try: # Determine if there is an open incident already
        if b[0] is not None:
            # Option 1: Do nothing
            logging.debug('Nothing to do, exiting.')
            return ("OK", 200, None)

            # Option 2: Add a new comment
            #payload = { 'ticket': { 'comment': { 'body': a['moreinfo'] } } }
            #return callapi(PIVOTALTRACKERURL + '/api/v2/tickets/' + str(i['results'][0]['id']) + '.json', 'put', json.dumps(payload), headers, (USER, PASS))
    except: # If no open bug then open one
        payload = {
            "name": a['AlertName'],
            "description": a['moreinfo'],
            "story_type": "bug"
        }
        return callapi(PIVOTALTRACKERURL + PROJECT + '/stories', 'post', json.dumps(payload), headers, None)
