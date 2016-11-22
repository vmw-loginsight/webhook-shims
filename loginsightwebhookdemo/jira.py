#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# jira parameters
JIRAURL = ''
JIRAUSER = ''
JIRAPASS = ''


@app.route("/endpoint/jira/<PROJECT>", methods=['POST'])
@app.route("/endpoint/jira/<PROJECT>/<ALERTID>", methods=['PUT'])
def jira(ALERTID=None, PROJECT=None):
    """
    Create a new incident for every incoming webhook that does not already have an unresolved incident.
    If an incident is currently unresolved, add a new comment to the unresolved alert.
    Requires JIRA* parameters to be defined.
    """

    if not JIRAURL or not JIRAUSER or not JIRAPASS or not PROJECT:
        return ("JIRA* parameters must be set, please edit the shim!", 500, None)

    headers = {'Content-type': 'application/json'}
    a = parse(request)

    # Get the list of unresolved incidents that contain the AlertName from the incoming webhook
    incident = callapi(JIRAURL + '/rest/api/2/search?jql=project=' + PROJECT + '+AND+resolution=unresolved+AND+summary~"' + a['AlertName'] + '"', 'get', None, headers, (JIRAUSER, JIRAPASS))

    i = json.loads(incident)
    try: # Determine if there is an unresolved incident already
        if i['issues'][0]['key'] is not None:
            # Option 1: Do nothing
            #logging.info('Nothing to do, exiting.')
            #return ("OK", 200, None)

            # Option 2: Add a new comment
            payload = { "body": a['moreinfo'] }
            return callapi(JIRAURL + '/rest/api/2/issue/' + i['issues'][0]['key'] + '/comment', 'put', json.dumps(payload), headers, (JIRAUSER, JIRAPASS))
    except: # If no open incident then open one
        payload = {
            "project": {
                "key": PROJECT
            },
            "fields": {
                "summary": a['AlertName'],
                "description": a['moreinfo'],
                "issuetype": {
                    "name": "Bug"
                }
            }
        }
        return callapi(JIRAURL + '/rest/api/2/issue/', 'post', json.dumps(payload), headers, (JIRAUSER, JIRAPASS))
