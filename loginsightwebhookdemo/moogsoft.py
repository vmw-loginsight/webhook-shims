#!/usr/bin/env python


"""
This shim only supports vROps payloads due to requirements for Moogsoft payload (resourceId, criticality/severity,
and update status such as "closed" or "updated".  If alerting from Log Insight is required, it should be handled
through forwarding the query alert to vROps.

The recommendations are not part of the alert payload so callbacks to vROps are made to retreive them and include
them in the payload for Moog.  Additionally, the impacted resource properties are also provided in the moog payload.

Moog expects a severity of 0 when an alert is cancelled.

Moog expects timestamp in seconds.

See Moogsoft documentation for payload key descriptions and expected values.  Thanks to Ray Webb with Moogsoft for
help testing this shim.
"""

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "John Dias"
__license__ = "Apache v2"
__verion__ = "1.0"


# This shim also calls back to vROps for additional info so
# the vROps parameters are required

# Parameters
# Example: https://<IP of moog server>:<port>
moogsoftURL = ''
# Example: https://<IP of vROPs node>/suite-api/
vropsURL = ''
# Basic auth
moogsoftUSER = ''
moogsoftPASS = ''
vropsUser = ''
vropsPass = ''

# For some labs, using self-signed will result in error during request due to cert check
# flip this flag to False to bypass certificate checking in those cases NOT RECOMMENDED FOR PRODUCTION
VERIFY = True

###########################################
# Call backs for getting more information
# from vROps for impacted resource
###########################################

def recommendations(ALERTID=None):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    alertURL = vropsURL+"api/alerts/"+ALERTID
    auth = (vropsUser, vropsPass)
    response = callapi(alertURL, method='get', payload=None, headers=headers, auth=auth, check=VERIFY)
# Fetch the alert to grab alert def ID
    alertInfo = json.loads(response)
    alertDescURL = vropsURL+"api/alertdefinitions/"+alertInfo['alertDefinitionId']
    response = callapi(alertDescURL, method='get', payload=None, headers=headers, auth=auth, check=VERIFY)
# Fetch recommendations from alert def
    recommendations = json.loads(response)
    if recommendations['states'][0]['recommendationPriorityMap']:
        for recommendation in recommendations['states'][0]['recommendationPriorityMap']:
            if recommendations['states'][0]['recommendationPriorityMap'][recommendation] == 1:
                alertDescURL = vropsURL+"api/recommendations/"+recommendation
                response = callapi(alertDescURL, method='get', payload=None, headers=headers, auth=auth, check=VERIFY)
                recText = json.loads(response)
                return recText['description']
    else:
        return

def fetchResourceProperties(resourceId=None):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    alertURL = vropsURL+"api/resources/"+resourceId+"/properties"
    auth = (vropsUser, vropsPass)
    response = callapi(alertURL, method='get', payload=None, headers=headers, auth=auth, check=VERIFY)
    rawProps = json.loads(response)

    props = {}
    for prop in rawProps['property']:
        props[prop["name"]] = prop["value"]
    return props

# Route without <ALERTID> are for LI, with are for vROps
# Adding PUT and POST for vROps so REST Notification test works
# vROps (as of 6.6.1) will attempt both methods and fail if both
# do not respond
# TODO : Add this capability to all shims
@app.route("/endpoint/moogsoft", methods=['POST'])
@app.route("/endpoint/moogsoft/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/moogsoft/<ALERTID>", methods=['POST'])

def moogsoft(ALERTID=None):

    """
    Information about this shim.
    Requires moogsoft* parameters to be defined.
    """
    bauth = request.authorization
    if bauth is not None:
        global moogsoftUSER
        global moogsoftPASS
        moogsoftUSER = bauth.username
        moogsoftPASS = bauth.password

    if (not moogsoftURL or (not moogsoftUSER ) or (not moogsoftPASS) or (not vropsURL) or (not vropsUser) or (not vropsPass)):
        return ("moogsoft* and vrops* parameters must be set, please edit the shim!", 500, None)

    a = parse(request)

########################################
#Map vROps crticiality to moog sev here
########################################
    sevMap = {
        "ALERT_CRITICALITY_LEVEL_CRITICAL":5,
        "ALERT_CRITICALITY_LEVEL_IMMEDIATE":4,
        "ALERT_CRITICALITY_LEVEL_WARNING":3,
        "ALERT_CRITICALITY_LEVEL_INFO":2
    }
    link = vropsURL+"/ui/index.action#/object/"+a['resourceId']+"/alertsAndSymptoms/alerts/"+ALERTID
    recommendation = recommendations(a['alertId'])
    resourceProperties = fetchResourceProperties(a['resourceId'])

    payload = {
        "signature":ALERTID,
        "source_id":a['resourceId'],
        "external_id":ALERTID,
        "manager":a['hookName'],
        "source":a['resourceName'] if (a['resourceName'] != "") else "undefined",
        "class":a['subType'],
        "agent":a['adapterKind'],
        "agent_location":"",
        "type":a['type']+"::"+a['subType'],
        "severity":sevMap[a['criticality']] if (a['status'] != 'CANCELED') else 0,
        "description":a['AlertName'],
        "agent_time":a['updateDate']/1000,
        "recommendation":recommendation,
        "resource_properties":resourceProperties,
        "link":link
    }

    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if not headers:
        headers = None

    return callapi(moogsoftURL, 'post', json.dumps(payload), headers, check=VERIFY)
