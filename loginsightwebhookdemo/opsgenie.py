#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__version__ = "2.0"


# opsgenie post url defined by https://v2.developer.opsgenie.com/v2/docs/trigger-events - don't change
OPSGENIEURL = 'https://api.opsgenie.com/v2/alerts'


@app.route("/endpoint/opsgenie/<APIKEY>", methods=['POST'])
@app.route("/endpoint/opsgenie/<APIKEY>/<ALERTID>", methods=['POST','PUT'])
def opsgenie(APIKEY=None, TEAM=None, ALERTID=None):
    """
    Create a new incident for the opsgenie service identified by `APIKEY` in the URL.
    Uses https://docs.opsgenie.com/docs/alert-api.
    """
    if not OPSGENIEURL:
        return ("OPSGENIEURL parameter must be set properly, please edit the shim!", 500, None)
    if not APIKEY:
        return ("APIKEY must be set in the URL (e.g. /endpoint/opsgenie/<APIKEY>", 500, None)
    HEADERS = {"Authorization": "GenieKey " + APIKEY}

    # Retrieve fields in notification
    a = parse(request)

    payload = {
        "alias": a['AlertName'],
        "message": a['AlertName'],
        "description": a['moreinfo']
    }
    return callapi(OPSGENIEURL, 'post', json.dumps(payload), HEADERS)
