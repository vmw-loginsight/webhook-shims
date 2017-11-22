#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# zendesk parameters
ZENDESKURL = '' # required
ZENDESKUSER = '' # required if not passed in URL
ZENDESKPASS = '' # required if ZENDESKTOKEN or TOKEN is not specified
ZENDESKTOKEN = '' # required if ZENDESKPASS is not specifed or TOKEN is not passed in URL


@app.route("/endpoint/zendesk", methods=['POST'])
@app.route("/endpoint/zendesk/<EMAIL>/<TOKEN>", methods=['POST'])
@app.route("/endpoint/zendesk/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/zendesk/<EMAIL>/<TOKEN>/<ALERTID>", methods=['POST','PUT'])
def zendesk(ALERTID=None, EMAIL=None, TOKEN=None):
    """
    Create a new incident for every incoming webhook that does not already have an open incident.
    If an incident is already open, add a new comment to the open alert.
    Uniqueness is determined by the incoming webhook alert name.
    Requires ZENDESK* parameters to be defined.
    """
    bauth = request.authorization
    if bauth is not None:
        global ZENDESKUSER
        global ZENDESKPASS
        ZENDESKUSER = bauth.username
        ZENDESKPASS = bauth.password

    if (not ZENDESKURL or (not ZENDESKUSER and not EMAIL) or (not ZENDESKPASS and not ZENDESKTOKEN and not TOKEN)):
        return ("ZENDESK* parameters must be set, please edit the shim!", 500, None)
    if not ZENDESKUSER:
        USER = EMAIL
    else:
        USER = ZENDESKUSER

    # Prefer tokens over passwords
    if ZENDESKTOKEN or TOKEN:
        if ZENDESKTOKEN:
            USER = USER + '/token'
            PASS = ZENDESKTOKEN
        else:
            USER = USER + '/token'
            PASS = TOKEN
    else:
        PASS = ZENDESKPASS

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    a = parse(request)

    # Get the list of open incidents that contain the AlertName from the incoming webhook
    incident = callapi(ZENDESKURL + '/api/v2/search.json?query=type:ticket status:open subject:"' + a['AlertName'] + '"', 'get', None, headers, (USER, PASS))
    i = json.loads(incident)

    try: # Determine if there is an open incident already
        if i['results'][0]['id'] is not None:
            # Option 1: Do nothing
            #logging.info('Nothing to do, exiting.')
            #return ("OK", 200, None)

            # Option 2: Add a new comment
            # Limited to 30 updates per 10 minutes (https://developer.zendesk.com/rest_api/docs/core/introduction)
            payload = { 'ticket': { 'comment': { 'body': a['moreinfo'] } } }
            return callapi(ZENDESKURL + '/api/v2/tickets/' + str(i['results'][0]['id']) + '.json', 'put', json.dumps(payload), headers, (USER, PASS))
    except: # If no open incident then open one
        payload = {
            "ticket": {
                #"requester": {
                #    "name": "Log Insight",
                #    "email": USER
                #},
                "subject": a['AlertName'],
                "comment": {
                    "body": a['moreinfo'],
                },
                "type": 'incident',
                "tags": ["loginsight"]
            }
        }
        return callapi(ZENDESKURL + '/api/v2/tickets.json', 'post', json.dumps(payload), headers, (USER, PASS))
