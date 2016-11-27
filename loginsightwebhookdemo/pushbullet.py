#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Adith Sudhakar"
__license__ = "Apache v2"
__verion__ = "1.1"


# Pushbullet URL, probably doesn't need to be changed
PUSHBULLETURL = 'https://api.pushbullet.com/v2/pushes'
# Obtain the Pushbullet Access Token from https://www.pushbullet.com/#settings/account
# Protect this access token - anyone who has access to it will be able to perform actions on your behalf.
PUSHBULLETTOKEN = ''


@app.route("/endpoint/pushbullet", methods=['POST'])
@app.route("/endpoint/pushbullet/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/pushbullet/<TOKEN>", methods=['POST'])
@app.route("/endpoint/pushbullet/<TOKEN>/<ALERTID>", methods=['PUT'])
def pushbullet(ALERTID=None, TOKEN=None):
    """
    Send a `link` notification to all devices on pushbullet with a link back to the alert's query.
    If `TOKEN` is not passed, requires `PUSHBULLETTOKEN` defined, see https://www.pushbullet.com/#settings/account
    """
    if not PUSHBULLETURL:
        return ("PUSHBULLET parameter must be set, please edit the shim!", 500, None)
    if (TOKEN is not None):
        PUSHBULLETTOKEN = TOKEN
    if not PUSHBULLETTOKEN:
        return ("PUSHBULLETTOKEN parameter must be set, please edit the shim!", 500, None)

    a = parse(request)

    payload = {
        "body": a['info'],
        "title": a['AlertName'],
        "type": "link",
        "url": a['url'],
    }

    headers = {'Content-type': 'application/json', 'Access-Token': PUSHBULLETTOKEN}

    return callapi(PUSHBULLETURL, 'post', json.dumps(payload), headers)
