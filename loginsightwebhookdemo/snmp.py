#!/usr/bin/env python

"""
This example implements most of the functionality of the native trap sender in vR Ops and LogInsight.
It's not intended as a replacement for any native functionality, but as a template for those who need to
customize traps beyond what the standard SNMP adapter does.

This example uses the standard vR Ops MIB, but can easily be changed to use any MIB.
"""

import os
import urllib
import urlparse
import requests
import threading
from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413 import context
from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.smi import builder, compiler

__author__ = "Pontus Rydin"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"
__version__ = "1.0"

# Parameters
TARGETHOST = '192.168.110.10'
TARGETPORT = 162
ORIGIN="vrops-01a.corp.local"

# vR Ops connection parameters. Leave unspecified for LI
VROPSURL = 'https://vrops-01a.corp.local'
VROPSUSER = 'admin'
VROPSPASS = 'VMware1!'
VROPSAUTHSOURCE = "Local Users"

# =======Internal constants. Don't change!

# vR Ops HTTP headers
#
VROPSHEADERS = { 'Accept': 'application/json', 'Content-Type': 'application/json', "Authorization": "Invalid"}

# Severity names for badges
SEVERITIES = [ "none", "info", "warning", "immediate", "critical"]

# Lock to make sure we don't mess up caches if flask calls us from multiple threads
cache_lock = threading.Lock()

# Determine path to compiled MIBs
this_dir = os.path.dirname(os.path.realpath(__file__))
mib_dir = os.path.join(this_dir, 'pysnmp_mibs')

# Add custom MIB dir to engine
engine = SnmpEngine()
ctx = context.SnmpContext(engine)
mibBuilder = ctx.getMibInstrum().getMibBuilder()
mibSources = mibBuilder.getMibSources() + (builder.DirMibSource(mib_dir),); 
mibBuilder.setMibSources(*mibSources)

# Preload VMware MIB
mibBuilder.loadModules('SNMPv2-MIB', 'SNMP-COMMUNITY-MIB', 'VMWARE-VCOPS-EVENT-MIB')


def vropsGet(url):
    response = requests.get(VROPSURL + url, verify=False, headers=VROPSHEADERS)
    if response.status_code == 401:
        with cache_lock:
            # Acquire a new token
            print("vR Ops token expired, getting a new one...")
            payload = { "username": VROPSUSER, "password": VROPSPASS, "authSource": VROPSAUTHSOURCE }
            response = requests.post(VROPSURL + "/suite-api/api/auth/token/acquire",
                json.dumps(payload), 
                headers = { "Accept": "application/json", "Content-Type": "application/json"},
                verify=False)
            if response.status_code != 200:
                raise Exception("Authentication failed. Status code: " + str(response.status_code))
            tokenJson = response.json()
            token = tokenJson["token"]
            VROPSHEADERS["Authorization"] = "vRealizeOpsToken " + token
        
        # Try again
        print(VROPSHEADERS)
        response = requests.get(VROPSURL + url, verify=False, headers=VROPSHEADERS)
        if response.status_code != 200:
            raise Exception("GET " + url + " failed. Status: " + str(response.status_code))
    return response


def lookup_alert(alertId):
    response = vropsGet("/suite-api/api/alerts/" + alertId)
    print("Lookup alert: " + response.content)
    return response


def lookup_resource(resourceId):
    response = vropsGet("/suite-api/api/resources/" + resourceId)
    print("Lookup resource: " + response.content)
    return response


def lookup_alert_definition(definitionId):
    response = vropsGet("/suite-api/api/alertdefinitions/" + definitionId)
    print("Lookup alert definition: " + response.content)
    return response


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/snmp", methods=['POST'])
@app.route("/endpoint/snmp/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/snmp/<TOKEN>", methods=['POST'])
@app.route("/endpoint/snmp/<TOKEN>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/snmp/<EMAIL>/<TOKEN>", methods=['POST'])
@app.route("/endpoint/snmp/<EMAIL>/<TOKEN>/<ALERTID>", methods=['PUT'])
def snmp(ALERTID=None, TOKEN=None, EMAIL=None):
    """
    Sends a customized SNMP trap.
    """

    a = parse(request)
    resource_kind = ''
    alert_description = ''
    alert_impact = ''

    if VROPSURL and ALERTID:
        alert = lookup_alert(ALERTID).json()
        resource = lookup_resource(a['resourceId']).json()
        resource_kind = resource['resourceKey']['resourceKindKey']
        alert_def = lookup_alert_definition(alert['alertDefinitionId']).json()
        alert_description = alert_def['description']

    alert_impact = ''
    if 'Health' in a and a['Health'] > 1:
        alert_impact = alert_impact + "health, "
    if 'Risk' in a and a['Risk'] > 1:
        alert_impact = alert_impact + "risk, "
    if 'Efficiency' in a and a['Efficiency'] > 1:
        alert_impact = alert_impact + "efficiency"
    if str.endswith(alert_impact, ", "):
        alert_impact = alert_impact[len(alert_impact)-2:]

    # Send the trap
    errorIndication = send_trap(a, alert_description, alert_impact, resource_kind)

    if errorIndication:
        print('Notification not sent: %s' % errorIndication)

    return "OK"


def decode_severity(s):
    if s:
        try:
            return SEVERITIES[int(s)]
        except ValueError:
            return None
    else:
        return None


def create_mibvar(name, value):
    return ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', name), value


def send_trap(a, alert_description, alert_impact, resource_kind):
    ntf_org = ntforg.NotificationOriginator(engine)
    errorIndication = ntf_org.sendNotification(
        ntforg.CommunityData('public'),
        ntforg.UdpTransportTarget(('localhost', 162)),
        'trap',
        ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareTrapProblemActive'),
        create_mibvar('vmwareAlertAliveServerName', ORIGIN),
        create_mibvar('vmwareAlertEntityName', a.get("resourceName", None)),
        create_mibvar('vmwareAlertEntityType', "General"),
        create_mibvar('vmwareAlertTimestamp', a.get("updateDate", None)),
        create_mibvar('vmwareAlertCriticality', a.get("criticality", None)),
        create_mibvar('vmwareAlertRootCause', "TODO"),
        create_mibvar('vmwareAlertURL', "TODO"),
        create_mibvar('vmwareAlertID', a.get('alertId', None)),
        create_mibvar('vmwareAlertMessage', "TODO"),
        create_mibvar('vmwareAlertMessage', a.get('moreinfo', None)),
        create_mibvar('vmwareAlertType', a.get('type', None)),
        create_mibvar('vmwareAlertSubtype', a.get('subType', None)),
        create_mibvar('vmwareAlertHealth', decode_severity(a.get('Health', None))),
        create_mibvar('vmwareAlertRisk', decode_severity(a.get('Risk', None))),
        create_mibvar('vmwareAlertEfficiency', decode_severity(a.get('Efficiency', None))),
        create_mibvar('vmwareAlertMetricName', ''),
        create_mibvar('vmwareAlertResourceKind', resource_kind),
        create_mibvar('vmwareAlertDefinitionName', a.get('AlertName', None)),
        create_mibvar('vmwareAlertDefinitionDesc', alert_description),
        create_mibvar('vmwareAlertImpact', alert_impact))
    return errorIndication

