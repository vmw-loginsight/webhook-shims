#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# ServiceNow parameters
SERVICENOWURL = ''
SERVICENOWUSER = ''
SERVICENOWPASS = ''


@app.route("/endpoint/servicenow", methods=['POST'])
@app.route("/endpoint/servicenow/<ALERTID>", methods=['PUT'])
def servicenow(ALERTID=None):
    """
    Create a new incident for every incoming webhook that does not already have an open incident.
    If an incident is already open, add a new comment to the open alert.
    Uniqueness is determined by the incoming webhook alert name.
    Requires SERVICENOW* parameters to be defined.
    """

    if not SERVICENOWURL or not SERVICENOWUSER or not SERVICENOWPASS:
        return ("SERVICENOW* parameters must be set, please edit the shim!", 500, None)

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    a = parse(request)
    payload = { "comments": a['moreinfo'] }

    # Get the list of open incidents that contain the AlertName from the incoming webhook
    incident = callapi(SERVICENOWURL + '/incident.do?JSONv2&sysparm_query=active=true^short_description=' + a['AlertName'], 'get', None, headers, (SERVICENOWUSER, SERVICENOWPASS))

    i = json.loads(incident)
    try: # Determine if there is an open incident already
        if i['records'][0]['sys_id'] is not None:
            # Option 1: Do nothing
            #logging.info('Nothing to do, exiting.')
            #return ("OK", 200, None)

            # Option 2: Add a new comment
            return callapi(SERVICENOWURL + '/api/now/v1/table/incident/' + i['records'][0]['sys_id'], 'put', json.dumps(payload), headers, (SERVICENOWUSER, SERVICENOWPASS))
    except: # If no open incident then open one
        payload.update({ "short_description": a['AlertName'] })
        return callapi(SERVICENOWURL + '/api/now/v1/table/incident', 'post', json.dumps(payload), headers, (SERVICENOWUSER, SERVICENOWPASS))
