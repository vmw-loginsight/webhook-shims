#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, sendevent
from flask import request
import logging


__author__ = "Adith Sudhakar"
__license__ = "Apache v2"


# Pushbullet URL, probably doesn't need to be changed
PUSHBULLETURL = 'https://api.pushbullet.com/v2/pushes'
# Obtain the Pushbullet Access Token from https://www.pushbullet.com/#settings/account
# Protect this access token - anyone who has access to it will be able to perform actions on your behalf.
PUSHBULLETTOKEN = ''


@app.route("/endpoint/pushbullet", methods=['POST'])
def pushbullet():
    """
    Send a `link` notification to all devices on pushbullet with a link back to the alert's query.
    Requires `PUSHBULLETTOKEN` defined, see https://www.pushbullet.com/#settings/account
    """
    if not PUSHBULLETURL:
        return ("PUSHBULLET parameter must be set, please edit the shim!", 500, None)
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

    return sendevent(PUSHBULLETURL, json.dumps(payload), headers)
