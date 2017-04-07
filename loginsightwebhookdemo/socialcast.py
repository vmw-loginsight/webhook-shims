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
@app.route("/endpoint/socialcast/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/socialcast/<ALERTID>/<int:NUMRESULTS>", methods=['POST','PUT'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>", methods=['POST'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/socialcast/<TEAM>/<I>/<X>/<ALERTID>/<int:NUMRESULTS>", methods=['POST','PUT'])
def socialcast(ALERTID=None, NUMRESULTS=10, TEAM=None, I=None, X=None):
    """
    Create a post on Socialcast containing log events.
    Limited to `NUMRESULTS` (default 10) or 1MB.
    If `TEAM/I/X` is not passed, requires `SOCIALCASTURL` defined in the form `https://TEAM.socialcast.com/api/webhooks/IIIIIIIIII/XXXXXXXXXXX`
    For more information see https://socialcast.github.io/socialcast/apidoc/incoming_webhook.html
    """
    if X is not None:
       URL = 'https://' + TEAM + '.socialcast.com/api/webhooks/' + I + '/' + X
    if not SOCIALCASTURL or not 'socialcast.com/api/webhooks' in SOCIALCASTURL:
        return ("SOCIALCASTURL parameter must be set properly, please edit the shim!\n", 500, None)
    else:
        URL = SOCIALCASTURL
    # Socialcast cares about the order of the information in the body
    # json.dumps() does not preserve the order so just use raw get_data()
    return callapi(URL, 'post', request.get_data())
