#!/usr/bin/env python


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = ""
__license__ = "Apache v2"
__verion__ = "1.0"


# Parameters
BUGZILLAURL = ''
# Basic auth -- required if TOKEN is not passed in URL
BUGZILLAUSER = ''
BUGZILLAPASS = ''
# Required fields -- if not passed in URL
BUGZILLAPRODUCT = ''
BUGZILLACOMPONENT = ''
BUGZILLAVERSION = ''
# If your Bugzilla SSL certification is not trusted,
# flip this flag to False to bypass certificate checking
VERIFY = True


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/bugzilla", methods=['POST'])
@app.route("/endpoint/bugzilla/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/bugzilla/<TOKEN>", methods=['POST'])
@app.route("/endpoint/bugzilla/<TOKEN>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/bugzilla/<TOKEN>/<PRODUCT>/<COMPONENT>/<VERSION>", methods=['POST'])
@app.route("/endpoint/bugzilla/<TOKEN>/<PRODUCT>/<COMPONENT>/<VERSION>/<ALERTID>", methods=['PUT'])
def bugzilla(ALERTID=None, TOKEN=None, PRODUCT=None, COMPONENT=None, VERSION=None):
    """
    Create a new bug for every incoming webhook that does not already have an open bug.
    If an bug is already open, add a new comment to the open bug.
    Uniqueness is determined by the incoming webhook alert name combined with bugzilla product and component.
    Requires BUGZILLA* parameters to be defined.
    """
    if (not BUGZILLAURL or
        (not BUGZILLAUSER and not BUGZILLAPASS and not TOKEN) or
        ((not BUGZILLAPRODUCT and BUGZILLACOMPONENT and BUGZILLAVERSION) and (not PRODUCT and not COMPONENT and not VERSION))):
            return ("BUGZILLA* parameters must be set, please edit the shim!", 500, None)

    a = parse(request)

    if TOKEN:
        auth = 'api_key=' + TOKEN
    else:
        auth = 'login=' + BUGZILLAUSER + '&password=' + BUGZILLAPASS
    if BUGZILLAPRODUCT:
        PRODUCT = BUGZILLAPRODUCT
        COMPONENT = BUGZILLACOMPONENT
        VERSION = BUGZILLAVERSION


    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    # Get the list of open bugs that contain the AlertName from the incoming webhook
    bug = callapi(BUGZILLAURL + '/rest/bug?' + auth + '&product=' + PRODUCT + '&component=' + COMPONENT + '&summary=' + a['AlertName'], 'get', None, headers, None, check = VERIFY)
    i = json.loads(bug)

    try: # Determine if there is an open bug already
        if i['bugs'][0]['id'] is not None:
            # Option 1: Do nothing
            #logging.info('Nothing to do, exiting.')
            #return ("OK", 200, None)

            # Option 2: Add a new comment
            payload = { 'comment': { 'body': a['moreinfo'] } }
            return callapi(BUGZILLAURL + '/rest/bug/' + str(i['bugs'][0]['id']) + '?' + auth, 'put', json.dumps(payload), headers, None, check = VERIFY)
    except: # If no open bug then open one
        payload = {
            "product" : PRODUCT,
            "component" : COMPONENT,
            "version" : VERSION,
            "summary" : a['AlertName'],
            "description": a['info'],
        }
        return callapi(BUGZILLAURL + '/rest/bug?' + auth, 'post', json.dumps(payload), headers, None, check = VERIFY)
