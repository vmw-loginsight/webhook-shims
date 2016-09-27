#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, sendevent
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
@app.route("/endpoint/servicenow/<TOKEN>", methods=['POST'])
@app.route("/endpoint/servicenow/<TOKEN>/<ALERTID>", methods=['PUT'])
def servicenow(ALERTID=None, TOKEN=None):
    """
    NOT READY - DO NOT USE!
    """
    if not SERVICENOWURL or not SERVICENOWUSER or not SERVICENOWPASS:
        return ("SERVICENOW* parameters must be set, please edit the shim!", 500, None)

    a = parse(request)

    payload = {
        "body": a['info'],
        "title": a['AlertName'],
        "type": "link",
        "url": a['url'],
    }
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    return sendevent(SERVICENOWURL, json.dumps(payload), headers, (SERVICENOWUSER, SERVICENOWPASS))
