#!/usr/bin/env python

"""
Hello! This template is available to help get you started with creating a shim.

Start by adjusting the `TEMPLATE` and `template` parameters.
Next, adjust the payload based on the API specification of your webhook destination.
Finally, add an import statement to __init__.py like:

import loginsightwebhookdemo.template
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

##### Internal consrtants. Don't change!

# vR Ops HTTP headers
#
VROPSHEADERS = { 'Accept': 'application/json', 'Content-Type': 'application/json', "Authorization": "Invalid"}

# Severity names for badges
SEVERITIES = [ "none", "info", "warning", "immediate", "critical"]

# Lock to make sure we don't mess up caches if flask calls us from multiple threads
cache_lock = threading.Lock()

# Determine path to compiled MIBs
this_dir = os.path.dirname(os.path.realpath(__file__))
print(this_dir)
mib_dir = os.path.join(this_dir, 'pysnmp_mibs')
print(mib_dir)

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
    print("SNMP trap")

    a = parse(request)

    print(a)
    ntfOrg = ntforg.NotificationOriginator(engine)

    resource_kind = ''
    alert_description = ''
    alert_impact = ''

    if ALERTID:
        alert = lookup_alert(ALERTID).json()
        resource = lookup_resource(a['resourceId']).json()
        resource_kind = resource['resourceKey']['resourceKindKey']
        alert_def = lookup_alert_definition(alert['alertDefinitionId']).json()
        alert_description = alert_def['description']

    alert_impact = ''
    if a['Health'] > 1:
        alert_impact = alert_impact + "health, "
    if a['Risk'] > 1:
        alert_impact = alert_impact + "risk, "
    if a['Efficiency'] > 1:
        alert_impact = alert_impact + "efficiency"
    if str.endswith(alert_impact, ", "):
        alert_impact = alert_impact[len(alert_impact)-2:]

    errorIndication = ntfOrg.sendNotification(
        ntforg.CommunityData('public'),
        ntforg.UdpTransportTarget(('localhost', 162)),
        'trap',
        ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareTrapProblemActive'),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertAliveServerName'), ORIGIN),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertEntityName'), a["resourceName"]),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertEntityType'), "General"),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertTimestamp'), a["updateDate"]),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertCriticality'), a["criticality"]),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertRootCause'), "TODO"),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertURL'), "TODO"),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertID'), a['alertId']),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertMessage'), "TODO"),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertMessage'), a['moreinfo']),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertType'), a['type']),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertSubtype'), a['subType']),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertHealth'), SEVERITIES[a['Health']]),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertRisk'), SEVERITIES[a['Risk']]),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertEfficiency'), SEVERITIES[a['Efficiency']]),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertMetricName'), ''),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertResourceKind'), resource_kind),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertDefinitionName'), a['AlertName']),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertDefinitionDesc'), alert_description),
        (ntforg.MibVariable('VMWARE-VCOPS-EVENT-MIB', 'vmwareAlertImpact'), alert_impact))

    if errorIndication:
        print('Notification not sent: %s' % errorIndication)

    return "OK"

