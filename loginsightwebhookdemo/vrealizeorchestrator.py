#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import base64
import re

__author__ = "John Dias and Steve Flanders"
__license__ = "Apache v2"
__version__ = "1.3"


# vRealize Orchestrator server workflow hostname:port (default port is 8281)
VROHOSTNAME = ''
# Either basic auth or OAuth token or SSO HoK is required
# OAuth token and SSO HoK can be specified in the URL
VROUSER = ''
VROPASS = ''
VROTOKEN = ''
VROHOK = ''
# For some labs, using self-signed will result in error during request due to cert check
# flip this flag to False to bypass certificate checking in those cases
VERIFY = True


@app.route("/endpoint/vro/<WORKFLOWID>", methods=['POST'])
@app.route("/endpoint/vro/<WORKFLOWID>/<ALERTID>", methods=['PUT', 'POST'])
@app.route("/endpoint/vro/<WORKFLOWID>/oauth/<TOKEN>", methods=['POST'])
@app.route("/endpoint/vro/<WORKFLOWID>/oauth/<TOKEN>/<ALERTID>", methods=['PUT', 'POST'])
@app.route("/endpoint/vro/<WORKFLOWID>/sso/<HOK>", methods=['POST'])
@app.route("/endpoint/vro/<WORKFLOWID>/sso/<HOK>/<ALERTID>", methods=['PUT', 'POST'])
def vro(WORKFLOWID=None, TOKEN=None, HOK=None, ALERTID=None):
    """
    Start a vRealize Orchestrator workflow, passing the entire JSON alert as a base64-encoded string.
    The `WORKFLOWID` and optionally `TOKEN` is passed in the webhook URL.
    The workflow is responsible for parsing base64 -> json -> messages
    """
    if not WORKFLOWID:
        return ("WORKFLOWID must be set in the URL (e.g. /endpoint/vro/<WORKFLOWID>", 500, None)
    if not re.match('[a-z0-9-]+', WORKFLOWID, flags=re.IGNORECASE):
        return ("WORKFLOWID must consist of alphanumeric and dash characters only", 500, None)
    if not VROHOSTNAME or (not VROUSER and not VROPASS and not VROTOKEN and not TOKEN and not VROHOK and not HOK):
        return ("VRO* parameters must be set, please edit the shim!", 500, None)

    if TOKEN is None and VROTOKEN:
        TOKEN = VROTOKEN
    elif HOK is None and VROHOK:
        HOK = VROHOK

    AUTH = None
    HEADERS = None
    if TOKEN is not None:
        HEADERS = {"Authorization": TOKEN}
    elif HOK is not None:
        HEADERS = {"Authorization": "Bearer " + HOK}
    else:
        AUTH = (VROUSER, VROPASS)

    if ALERTID is None: # LI payload
        a = parse(request)

        payload = {
            "parameters": [
                {
                    "value": {
                        "string": {
                            "value": base64.b64encode(request.get_data())
                        }
                    },
                    "type": "string",
                    "name": "messages",
                    "scope": "local"
                },
                {
                    "value": {
                        "string": {
                            "value": a['AlertName']
                        }
                    },
                    "type": "string",
                    "name": "alertName",
                    "scope": "local"
                },
                {
                    "value": {
                        "number": {
                            "value": a['NumHits']
                        }
                    },
                    "type": "number",
                    "name": "hitCount",
                    "scope": "local"
                }
            ]
        }
    else: # vROps payload
        # If you would like, you can parse the payload from vROps.  However, it is
        # probably easier to just pass the ALERTID as workflow input to a wrapper and
        # look up the alert from vRO.  This gets around the problem of having to encode
        # the alert payload for vRO.
        # a = parse(request)

        payload = {
            "parameters": [
                {
                    "value": {
                        "string": {
                            "value": ALERTID
                        }
                    },
                    "type": "string",
                    "name": "alertId",
                    "scope": "local"
                }
            ]
        }
    return callapi("https://" + VROHOSTNAME + "/vco/api/workflows/" + WORKFLOWID + "/executions", 'post', json.dumps(payload), HEADERS, AUTH, VERIFY)
