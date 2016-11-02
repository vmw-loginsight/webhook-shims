#!/usr/bin/env python

"""
Hello! This template is available to help get you started with creating a shim.

Start by adjusting the `TEMPLATE` and `template` parameters.
Next, adjust the payload based on the API specification of your webhook destination.
Finally, add an import statement to __init__.py like:

import loginsightwebhookdemo.template
"""


from loginsightwebhookdemo import app, parse, sendevent
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


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/template", methods=['POST'])
@app.route("/endpoint/template/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/template/<TOKEN>", methods=['POST'])
@app.route("/endpoint/template/<TOKEN>/<ALERTID>", methods=['PUT'])
def template(ALERTID=None, TOKEN=None):
    """
    Information about this shim.
    """
    if not TEMPLATEURL or not TEMPLATEUSER or not TEMPLATEPASS:
        return ("TEMPLATE* parameters must be set, please edit the shim!", 500, None)

    a = parse(request)

    payload = {
        "body": a['info'],
        "title": a['AlertName'],
        "type": "link",
        "url": a['url'],
    }

    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    #headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    headers = ''

    if headers:
        return sendevent(TEMPLATEURL, json.dumps(payload), headers)
    else:
        return sendevent(TEMPLATEURL, json.dumps(payload))
    #return sendevent(TEMPLATEURL, json.dumps(payload), headers, (TEMPLATEUSER, TEMPLATEPASS))
