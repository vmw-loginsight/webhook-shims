#!/usr/bin/env python


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__verion__ = "1.0"


# Parameters
GROOVEURL = ''
# Below parameters can also be sent via the URL
GROOVEFROM = ''
GROOVETO = ''

# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/groove/<TOKEN>", methods=['POST'])
@app.route("/endpoint/groove/<TOKEN>/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/groove/<TOKEN>/<FROM>/<TO>", methods=['POST'])
@app.route("/endpoint/groove/<TOKEN>/<FROM>/<TO>/<ALERTID>", methods=['POST','PUT'])
def groove(ALERTID=None, TOKEN=None, FROM=None, TO=None):
    """
    Create a new ticket for every incoming webhook.
    Groove does not support searching for open tickets by subject today.
    Requires GROOVE* parameters to be defined.
    """
    if not GROOVEURL or (not GROOVEFROM and not FROM) or (not GROOVETO and not TO):
        return ("GROOVE* parameters must be set, please edit the shim!", 500, None)
    if TOKEN is None:
        return ("TOKEN must be passed in the URL, please edit the incoming webhook!", 500, None)
    if GROOVEFROM and not FROM:
        FROM = GROOVEFROM
    if GROOVETO and not TO:
        TO = GROOVETO

    a = parse(request)

    headers = { 'Content-type': 'application/json', 'Authorization': 'Bearer ' + TOKEN }

    # Unfortunately, the Groove API does not support searching for open tickets by subject today
    # https://www.groovehq.com/docs/tickets#finding-one-ticket
    # As a result, every incoming webhook will result in a new ticket
    # Commented sections has been wired for when the Groove API is updated to support the use case

    ## Get the list of open incidents that contain the AlertName from the incoming webhook
    # payload = {
    #     "state": "notstarted,opened,pending",
    #     "subject": a['AlertName']
    # }
    # incident = callapi(GROOVEURL + '/tickets', 'get', payload, headers)
    #
    # try:
    #   i = json.loads(incident)
    # except:
    #   return incident

    # try: # Determine if there is an open incident already
    #     if i['tickets'][0]['number'] is not None:
    #         # Option 1: Do nothing
    #         #logging.info('Nothing to do, exiting.')
    #         #return ("OK", 200, None)

    #         # Option 2: Add a new message
    #         payload = { 'body': a['moreinfo'] }
    #         return callapi(GROOVEURL + '/tickets/' + str(i['tickets'][0]['number']) + '/messages', 'put', json.dumps(payload), headers)
    # except: # If no open incident then open one
    payload = {
        "ticket": {
            "body": a['moreinfo'],
            "from": FROM,
            "to": TO,
            "subject": a['AlertName'],
            "tags": ["loginsight"]
        }
    }
    return callapi(GROOVEURL + '/tickets', 'post', json.dumps(payload), headers)
