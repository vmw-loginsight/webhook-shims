#!/usr/bin/env python

"""
Hello! This template is available to help get you started with creating a shim.

Start by adjusting the `TEMPLATE` and `template` parameters.
Next, adjust the payload based on the API specification of your webhook destination.
Finally, add an import statement to __init__.py like:

import loginsightwebhookdemo.template
"""


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = ""
__license__ = "Apache v2"
__verion__ = "1.0"


# Parameters
TEMPLATEURL = ''
# Basic auth
#TEMPLATEUSER = ''
#TEMPLATEPASS = ''
# Token auth
#TEMPLATETOKEN = ''


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/template", methods=['POST'])
@app.route("/endpoint/template/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/template/<TOKEN>", methods=['POST'])
@app.route("/endpoint/template/<TOKEN>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/template/<EMAIL>/<TOKEN>", methods=['POST'])
@app.route("/endpoint/template/<EMAIL>/<TOKEN>/<ALERTID>", methods=['PUT'])
def template(ALERTID=None, TOKEN=None, EMAIL=None):
    """
    Information about this shim.
    Requires TEMPLATE* parameters to be defined.
    """
    if (not TEMPLATEURL or (not TEMPLATEUSER and not EMAIL) or (not TEMPLATEPASS and not TEMPLATETOKEN and not TOKEN)):
        return ("TEMPLATE* parameters must be set, please edit the shim!", 500, None)
    if not TEMPLATEUSER:
        USER = EMAIL
    else:
        USER = TEMPLATEUSER
    # Prefer tokens over passwords
    if TEMPLATETOKEN or TOKEN:
        if TEMPLATETOKEN:
            USER = USER + '/token'
            PASS = TEMPLATETOKEN
        else:
            USER = USER + '/token'
            PASS = TOKEN
    else:
        PASS = TEMPLATEPASS

    a = parse(request)

    payload = {
        "body": a['info'],
        "title": a['AlertName'],
        "type": "link",
        "url": a['url'],
    }

    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if not headers:
        headers = None

    #########################
    # Fire and Forgot Systems
    #########################

    return callapi(TEMPLATEURL, 'post', json.dumps(payload), headers)

    ######################################
    # Check, Fire, and Forget Systems
    # Incident / Ticket Management Systems
    ######################################

    ## Get the list of open incidents that contain the AlertName from the incoming webhook
    #incident = callapi(TEMPLATEURL + '/api/v2/search.json?query=type:ticket status:open subject:"' + a['AlertName'] + '"', 'get', None, headers, (USER, PASS))
    #try:
    #    i = json.loads(incident)
    #except:
    #    return incident

    #try: # Determine if there is an open incident already
    #    if i['results'][0]['id'] is not None:
    #        # Option 1: Do nothing
    #        #logging.info('Nothing to do, exiting.')
    #        #return ("OK", 200, None)

    #        # Option 2: Add a new comment
    #        payload = { 'ticket': { 'comment': { 'body': a['moreinfo'] } } }
    #        return callapi(TEMPLATEURL + '/api/v2/tickets/' + str(i['results'][0]['id']) + '.json', 'put', json.dumps(payload), headers, (USER, PASS))
    #except: # If no open incident then open one
    #    payload = {
    #        "ticket": {
    #            "subject": a['AlertName'],
    #            "comment": {
    #                "body": a['moreinfo'],
    #            },
    #            "type": 'incident',
    #        }
    #    }
    #    return callapi(TEMPLATEURL + '/api/v2/tickets.json', 'post', json.dumps(payload), headers, (USER, PASS))
