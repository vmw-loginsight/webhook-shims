#!/usr/bin/env python

"""
#Demo webhook shims for Log Insight and vRealize Operations Manager

This is a demo shim, implemented using Flask, that accepts alert webhooks from:

1) VMware vRealize Log Insight 3.3 or newer

2) VMware vRealize Operations Manager 6.0 or newer (6.2 or newer recommended)

You can invoke `runserver.py [<port>]` directly on your development machine or run the Flask app under any WSGI webserver.
Don't run it on the Log Insight or vRealize Operations Manager virtual appliance, though.
Some shims require manually setting variables within the shim, while others work via URLs. Only modify variables BEFORE the app.route section in each shim.

As a demonstration, these shims are optimized for readability.
There is minimal error handling and no attempt to retransmit.
HTTP errors are passed back to the incoming system.
THESE SHIMS COME WITH NO SUPPORT - USE AT YOUR OWN RISK.
Please send feedback to https://github.com/vmw-loginsight/webhook-shims/issues or mailto:li-cord@vmware.com - pull requests welcome.

Known issues: 1) vRealize Operations Manager returns an error when testing a rest plugin to this shim though the test does work (cosmetic issue)

The following functions parse the webhook payload from the above products, translate and send it to other services.
Note that `<ALERTID>` is sent as part of vRealize Operations Manager webhooks and should not be specified when configuring incoming webhooks.
"""

from distutils.util import strtobool
from flask import Flask, Markup, request, json
import requests
import logging
import re
import base64


app = Flask(__name__)


__author__ = "Alan Castonguay and Steve Flanders"
__copyright__ = "Copyright 2016-2018"
__credits__ = ["Alan Castonguay", "Steve Flanders"]
__license__ = "Apache v2"
__maintainer__ = "Alan Castonguay and Steve Flanders"
__email__ = "li-cord@vmware.com"
__status__ = "Beta"
__version__ = "2.2"


def _minimal_markdown(markdown):
    """
    Given an html-safe Markdown object, replace some markdown with its html equivilant.
    This is the bare minimum necessary for example docstrings.
    For production use, leverage https://github.com/waylan/Python-Markdown instead.
    """
    assert(type(markdown) == Markup)
    s = str(markdown)
    s = re.sub(r'^#\s*(.*)\n*$', '<h1>\g<1></h1>', s, flags=re.MULTILINE)
    s = s.replace('\n\n', '<br><br>\n\n')
    s = re.sub(r'(\s)(https?://[^\s]+)(\s)', '\g<1><a href="\g<2>">\g<2></a>\g<3>', s, flags=re.IGNORECASE)
    s = re.sub(r'(\s)mailto:([^\s]+@[^\s]+)(\s)', '\g<1><a href="mailto:\g<2>">\g<2></a>\g<3>', s, flags=re.IGNORECASE)
    s = re.sub(r'`(.*?)`', '<code>\g<1></code>', s, flags=re.IGNORECASE)
    return Markup(s)


def parse(request):
    """
    Parse incoming JSON.
    Returns a dict or logs an exception.
    """
    try:
        payload = request.get_json()
        if (payload is None):
            logging.exception("Payload is empty, did you specify a Header in the request?")
            raise
        alert = {}
        alert = parseLI(payload, alert)
        alert = parsevROps(payload, alert)
    except:
        logging.info("Body=%s" % request.get_data())
        logging.exception("Unexpected payload, is it in proper JSON format?")
        raise
    logging.info("Parsed=%s" % alert)
    return alert


def parseLI(payload, alert):
    """
    Parse LI JSON from alert webhook.
    Returns a dict.
    """
    if (not 'AlertName' in payload):
        return alert
    alert.update({
        "hookName": "Log Insight",
        "color": "red",
        "AlertName": payload['AlertName']                   if ('AlertName' in payload) else "<None>",
        "info": payload['Info']                             if ('Info' in payload and payload['Info'] is not None) else "",
        "Messages": payload['messages']                     if ('messages' in payload) else "",
        "url": payload['Url']                               if ('Url' in payload and payload['Url'] is not None) else "",
        "editurl": payload['EditUrl']                       if ('EditUrl' in payload and payload['EditUrl'] is not None) else "",
        "HasMoreResults": str(payload['HasMoreResults'])    if 'HasMoreResults' in payload else False,
        # may be less than length of messages, if there's more events
        "NumHits": str(payload['NumHits'])                  if 'NumHits' in payload else False,
        "icon": "http://blogs.vmware.com/management/files/2015/04/li-logo.png",
    })
    if ('Info' in payload and payload['Info'] is not None):
        alert.update({"info": payload['Info']})
    elif ('messages' in payload and payload['messages'] is not None and len(payload['messages']) > 0):
        alert.update({"info": payload['messages'][0]['text']})
    else:
        alert.update({"info": ""})
    if ('Messages' in alert and not alert['Messages']): # If a test alert
        alert.update({
            "moreinfo": ("Hello from the webhook shim! This is a test webhook alert.\n\n") + \
                ("Alert Name: ") + alert['AlertName'] + \
                ("\nAlert Info: ") + alert['info'] + \
                ("\nAlert Details: ") + str(alert['Messages']),
        })
    else:
        alert.update({
            "moreinfo": ("Alert Name: ") + alert['AlertName'] + \
                ("\nAlert Info: ") + alert['info'] + \
                ("\nAlert Details: ") + str(alert['Messages']) + \
                ("\n\nYou can view this alert by clicking: %s" % alert['url'] if alert['url'] else "") + \
                ("\nYou can edit this alert by clicking: %s" % alert['editurl'] if alert['editurl'] else ""),
        })
    if alert['HasMoreResults']:
        alert.update({
            "fields": [
                { "name": 'HasMoreResults',     "content": alert['HasMoreResults'], },
                { "name": 'NumHits',            "content": alert['NumHits'], }
            ]
        })
    else:
        alert.update({"fields": []})
    return alert


def parsevROps(payload, alert):
    """
    Parse vROps JSON from alert webhook.
    Returns a dict.
    """
    if (not 'alertId' in payload):
        return alert
    alert.update({
        "hookName": "vRealize Operations Manager",
        "AlertName": payload['alertName']       if ('alertName' in payload and payload['alertName'] != "") else "<None>",
        "alertId": payload['alertId']           if ('alertId' in payload) else "",
        "info": payload['info']                 if ('info' in payload and payload['info'] is not None) else "",
        "criticality": payload['criticality']   if ('criticality' in payload) else "",
        "status": payload['status']             if ('status' in payload) else "",
        "type": payload['type']                 if ('type' in payload) else "",
        "subType": payload['subType']           if ('subType' in payload) else "",
        "Risk": payload['Risk']                 if ('Risk' in payload) else "<None>",
        "Efficiency": payload['Efficiency']     if ('Efficiency' in payload) else "<None>",
        "Health": payload['Health']             if ('Health' in payload) else "<None>",
        "resourceName": payload['resourceName'] if ('resourceName' in payload) else "",
        "resourceId": payload['resourceId']     if ('resourceId' in payload) else "",
        "adapterKind": payload['adapterKind']   if ('adapterKind' in payload) else "",
        "startDate": payload['startDate']       if ('startDate' in payload) else "",
        "updateDate": payload['updateDate']     if ('updateDate' in payload) else "",
        "icon": "http://blogs.vmware.com/management/files/2016/09/vrops-256.png",
        "Messages":"",
        "url":"",
        "editurl":"",
    })
    if (alert['status'] == "ACTIVE"):
        if (alert['criticality'] == "ALERT_CRITICALITY_LEVEL_CRITICAL" or
            alert['criticality'] == "ALERT_CRITICALITY_LEVEL_IMMEDIATE"):
                color = "red"
        elif (alert['criticality'] == "ALERT_CRITICALITY_LEVEL_WARNING"):
            color = "yellow"
        else:
            color = "gray"
    elif (alert['status'] != "ACTIVE" and alert['status'] != ""):
        if (alert['criticality'] == "ALERT_CRITICALITY_LEVEL_CRITICAL" or
            alert['criticality'] == "ALERT_CRITICALITY_LEVEL_IMMEDIATE" or
            alert['criticality'] == "ALERT_CRITICALITY_LEVEL_WARNING"):
                color = "green"
        else:
            color = "gray"
    else:
        color = "red"
    alert.update({
        "color": color,
        "fields": [
            { "name": 'Health',         "content": str(alert['Health']), },
            { "name": 'Risk',           "content": str(alert['Risk']), },
            { "name": 'Efficiency',     "content": str(alert['Efficiency']), },
            { "name": 'Resouce Name',   "content": alert['resourceName'], },
            { "name": 'Adapter Kind',   "content": alert['adapterKind'], },
            { "name": 'Type',           "content": alert['type'], },
            { "name": 'Sub Type',       "content": alert['subType'], },
        ]
    })
    if (alert['adapterKind'] == 'sample-adapter-type'): # If a test alert
        alert.update({
            "moreinfo": "Hello from the webhook shim! This is a test webhook alert.\n\n" + \
                    ("Alert Name: ") + alert['AlertName'] + \
                    ("\nAlert Info: ") + alert['info'] + \
                    ("\nAlert Details: ") + str(alert['fields']),
        })
    else:
        alert.update({
            "moreinfo": ("Alert Name: ") + alert['AlertName'] + \
                    ("\nAlert Info: ") + alert['info'] + \
                    ("\nAlert Details: ") + str(alert['fields']),
        })
    return alert


def callapi(url, method='post', payload=None, headers=None, auth=None, check=True):
    """
    Simple wrapper around `requests.post`, with excessive logging.
    Returns a Flask-friendly tuple on success or failure.
    Logs and re-raises any exceptions.
    """
    if not headers:
        headers = {'Content-type': 'application/json'}
    try:
        logging.info("URL=%s" % url)
        logging.info("Auth=%s" % str(auth))
        logging.info("Headers=%s" % headers)
        logging.info("Body=%s" % payload)
        logging.info("Check=%s" % check)
        if (auth is not None):
            r = requests.request(method, url, auth=auth, headers=headers, data=payload, verify=bool(strtobool(str(check))))
        else:
            r = requests.request(method, url, headers=headers, data=payload, verify=check)
        if r.status_code >= 200 and r.status_code < 300:
            if (payload is None):
                return r.text
            else:
                return ("OK", r.status_code, None)
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise
    return ("%s" % r.text, r.status_code, None)


@app.route("/")
def _introduction():
    """This help text."""
    ret = _minimal_markdown(Markup("<p>%s</p>") % __doc__)
    ret += Markup("<dl>")

    for f in sorted(app.view_functions):
        if f != 'static':
            ret += Markup("<dt><b>%s()</b></dt>\n") % f
            for r in app.url_map.iter_rules():
                if r.endpoint == f:
                    ret += Markup(" <dd><code>%s</code></dd>\n") % str(r)
            ret += Markup(" <dd>%s</dd>\n") % _minimal_markdown(Markup.escape(str(app.view_functions[f].__doc__)))
    ret += Markup("</dl>")
    return ret


@app.route("/endpoint/test", methods=['POST'])
@app.route("/endpoint/test/<ALERTID>", methods=['POST'])
def test(ALERTID=None):
    """Log the auth header, request, and parsed moreinfo field. Respond with success. Don't send the payload anywhere."""
    try:
        logging.info(request.headers['Authorization'])
    except KeyError:
        pass
    if request.get_data():
        logging.info(request.get_data())
        a = parse(request)
        try:
            logging.info(a['moreinfo'])
        except KeyError:
            pass
    return "OK"


# Import individual shims
import loginsightwebhookdemo.bigpanda
import loginsightwebhookdemo.bugzilla
import loginsightwebhookdemo.groove
import loginsightwebhookdemo.hipchat
import loginsightwebhookdemo.jenkins
import loginsightwebhookdemo.jira
import loginsightwebhookdemo.kafkatopic
import loginsightwebhookdemo.opsgenie
import loginsightwebhookdemo.pagerduty
import loginsightwebhookdemo.pivotaltracker
import loginsightwebhookdemo.pushbullet
import loginsightwebhookdemo.servicenow
import loginsightwebhookdemo.slack
import loginsightwebhookdemo.socialcast
#import loginsightwebhookdemo.template
import loginsightwebhookdemo.travisci
import loginsightwebhookdemo.vrealizeorchestrator
import loginsightwebhookdemo.zendesk
import loginsightwebhookdemo.moogsoft
import loginsightwebhookdemo.msteams
