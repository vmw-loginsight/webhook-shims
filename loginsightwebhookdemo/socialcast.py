#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, sendevent
from flask import request
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"


# Socialcast community Integration URL, defined in the form `https://demo.socialcast.com/api/webhooks/IIIIIIIIII/XXXXXXXXXXX`
SOCIALCASTURL = ''


@app.route("/endpoint/socialcast", methods=['POST'])
@app.route("/endpoint/socialcast/<int:NUMRESULTS>", methods=['POST'])
def socialcast(NUMRESULTS=10):
    """
    Create a post on Socialcast containing log events.
    Limited to `NUMRESULTS` (default 10) or 1MB.
    Requires `SOCIALCASTURL` defined in the form `https://demo.socialcast.com/api/webhooks/IIIIIIIIII/XXXXXXXXXXX`
    For more information see https://socialcast.github.io/socialcast/apidoc/incoming_webhook.html
    """
    if not SOCIALCASTURL:
        return ("SOCIALCASTURL parameter must be set, please edit the shim!\n", 500, None)
    # Socialcast cares about the order of the information in the body
    # json.dumps() does not preserve the order so just use raw get_data()
    return sendevent(SOCIALCASTURL, request.get_data())
