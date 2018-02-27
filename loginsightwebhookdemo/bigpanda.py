#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__version__ = "1.0"


BIGPANDAURL = 'https://api.bigpanda.io/data/v2/alerts'


@app.route("/endpoint/bigpanda/<TOKEN>/<APPKEY>", methods=['POST'])
@app.route("/endpoint/bigpanda/<TOKEN>/<APPKEY>/<ALERTID>", methods=['POST','PUT'])
def bigpanda(TOKEN=None, APPKEY=None, ALERTID=None):
    """
    Create a new incident for the bigpanda service identified by `APIKEY` in the URL.
    Uses https://docs.bigpanda.io/reference#alerts.
    """
    if not BIGPANDAURL:
        return ("BIGPANDAURL parameter must be set properly, please edit the shim!", 500, None)
    if not TOKEN:
        return ("TOKEN must be set in the URL (e.g. /endpoint/bigpanda/<TOKEN>/<APPKEY>", 500, None)
    if not APPKEY:
        return ("APPKEY must be set in the URL (e.g. /endpoint/bigpanda/<TOKEN>/<APPKEY>", 500, None)
    HEADERS = {"Authorization": "Bearer " + TOKEN}

    # Retrieve fields in notification
    a = parse(request)

    payload = {
        "app_key": APPKEY,
        "host": "Webhook Shim",
        "check": a['AlertName'],
        "description": a['moreinfo']
    }
    return callapi(BIGPANDAURL, 'post', json.dumps(payload), HEADERS)
