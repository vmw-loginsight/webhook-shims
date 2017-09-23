#!/usr/bin/env python


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "John Dias"
__license__ = "Apache v2"
__verion__ = "1.0"


# This shim also calls back to vROps for additional info so
# the vROps parameters are required 

# Parameters
moogsoftURL = 'http://35.196.173.191:3284/'
vropsURL = 'https://10.140.50.30/suite-api/'
# Basic auth
moogsoftUSER = 'jdias'
moogsoftPASS = 'password'
vropsUser = 'admin'
vropsPass = 'VMware1!'
# Token auth
moogsoftTOKEN = ''
# For some labs, using self-signed will result in error during request due to cert check
# flip this flag to False to bypass certificate checking in those cases
VERIFY = False

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
    if (not moogsoftURL or (not moogsoftUSER ) or (not moogsoftPASS)):
        return ("moogsoft* parameters must be set, please edit the shim!", 500, None)

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
#######################################
#Example includes retrieving additional 
# data not found in alert payload
#######################################

    recommendation = recommendations(a['alertId'])

    payload =      {
        "signature":a['adapterKind']+"::"+a['type']+"::"+a['subType'],
        "source_id":a['resourceId'],
        "external_id":ALERTID,
        "manager":a['hookName'],
        "source":a['resourceName'],
        "class":a['subType'],
        "agent":a['adapterKind'],
        "agent_location":"",
        "type":a['type']+"::"+a['subType'],
        "severity":sevMap[a['criticality']],
        "description":a['AlertName'],
        "first_occurred":a['startDate']/1000,
        "agent_time":a['updateDate']/1000,
        "recommendation": [recommendation]
    }



    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if not headers:
        headers = None

    
    print(json.dumps(payload))
    return callapi(moogsoftURL, 'post', json.dumps(payload), headers, check=VERIFY)
