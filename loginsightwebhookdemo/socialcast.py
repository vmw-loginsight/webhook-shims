#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"
__version__ = "1.1"

# Socialcast community Integration URL, defined in the form `https://demo.socialcast.com/api/webhooks/IIIIIIIIII/XXXXXXXXXXX`
SOCIALCASTURL = ''


@app.route("/endpoint/socialcast", methods=['POST'])
@app.route("/endpoint/socialcast/<int:NUMRESULTS>", methods=['POST'])
@app.route("/endpoint/socialcast/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/socialcast/<int:NUMRESULTS>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>", methods=['POST'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>/<int:NUMRESULTS>", methods=['POST'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>/<int:NUMRESULTS>/<ALERTID>", methods=['PUT'])
def socialcast(ALERTID=None, NUMRESULTS=10, TEAM=None, I=None, X=None):
    """
    Create a post on Socialcast containing log events.
    Limited to `NUMRESULTS` (default 10) or 1MB.
    If `TEAM/I/X` is not passed, requires `SOCIALCASTURL` defined in the form `https://TEAM.socialcast.com/api/webhooks/IIIIIIIIII/XXXXXXXXXXX`
    For more information see https://socialcast.github.io/socialcast/apidoc/incoming_webhook.html
    """
    if (X is not None):
        SOCIALCASTURL = 'https://' + TEAM + '.socialcast.com/api/webhooks/' + I + '/' + X
    if not SOCIALCASTURL:
        return ("SOCIALCASTURL parameter must be set, please edit the shim!\n", 500, None)
    # Socialcast cares about the order of the information in the body
    # json.dumps() does not preserve the order so just use raw get_data()
    return callapi(SOCIALCASTURL, 'post', request.get_data())
