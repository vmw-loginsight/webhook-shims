#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__version__ = "1.0"


# opsgenie post url defined by https://v2.developer.opsgenie.com/v2/docs/trigger-events - don't change
OPSGENIEURL = 'https://api.opsgenie.com/v1/json/alert'


@app.route("/endpoint/opsgenie/<APIKEY>", methods=['POST'])
@app.route("/endpoint/opsgenie/<APIKEY>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/opsgenie/<APIKEY>/<TEAM>", methods=['POST'])
@app.route("/endpoint/opsgenie/<APIKEY>/<TEAM>/<ALERTID>", methods=['PUT'])
def opsgenie(APIKEY=None, TEAM=None, ALERTID=None):
    """
    Create a new incident for the opsgenie service identified by `APIKEY` in the URL.
    Uses https://www.opsgenie.com/docs/web-api/alert-api#createAlertRequest.
    """
    if not APIKEY:
        return ("APIKEY must be set in the URL (e.g. /endpoint/opsgenie/<APIKEY>", 500, None)

    # Retrieve fields in notification
    a = parse(request)

    payload = {
        "apiKey": APIKEY,
        "alias": a['AlertName'],
        "message": a['AlertName'],
        "details": {
            "notes": a['info'],
            "events": str(a['Messages']),
        },
        "description": a['moreinfo']
    }
    if TEAM is not None:
        payload.append({"teams": [TEAM]})
    return callapi(OPSGENIEURL, 'post', json.dumps(payload))
