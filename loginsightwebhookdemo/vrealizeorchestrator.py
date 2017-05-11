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

##########################################################################################
# You can use the following methods for authentication
# *  Add a .netrc to the home director of the user running the shim with the vro fqdn, username
#    and password.  Leave USENETRC = True
# *  Basic auth by completing VROUSER and VROPASS below
# *  OAuth token by completing the VROTOKEN below (warning, the token will expire if unused)
# *  SSO HoK by completing the VROHOK below (warning, the HoK will expire if unused)
#
# You may also pass the OAuth or HoK values via the query as shown below.
# If you intend to use an auth method other than .netrc, flip USENETRC to False
##########################################################################################

USENETRC = True
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
    if not VROHOSTNAME:
	return("VROHOSTNAME parameter is not net, please edit the shim!", 500, None)
    if not USENETRC and (not VROUSER and not VROPASS and not VROTOKEN and not TOKEN and not VROHOK and not HOK):
        return ("VRO* authentication parameters must be set, please edit the shim!", 500, None)

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
    elif not USENETRC:
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
    # Execute the request
    response = callapi("https://" + VROHOSTNAME + "/vco/api/workflows/" + WORKFLOWID + "/executions", 'post', json.dumps(payload), HEADERS, AUTH, VERIFY)
    try: # Kludge to get around Log Insight bug (not accepting HTTP 202 as a valid response)
        if response[1] >= 200 and response[1] < 300:
            return ("OK", 200, None)
    except:
        return response
