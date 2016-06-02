#!/usr/bin/env python

import json
from flask import Flask
from flask import request
import requests
app = Flask(__name__)
import logging
import sys

__author__ = "Alan Castonguay and Steve Flanders"
__copyright__ = "Copyright 2016"
__credits__ = ["Alan Castonguay", "Steve Flanders"]
__license__ = "Apache v2"
__version__ = "1.0"
__maintainer__ = "Alan Castonguay and Steve Flanders"
__email__ = "li-cord@vmware.com"
__status__ = "Beta"

#######################################
# VARIABLES CHANGEME!!!
#######################################

# Port to use when running the shim
PORT=5001

# Socialcast
SOCIALCASTURL=''

# Slack
SLACKURL=''

# Pushbullet
PUSHBULLETURL='https://api.pushbullet.com/v2/pushes'
# This is an access token that you can obtain from https://www.pushbullet.com/#settings/account
# Please protect this access token since an unauthorized user who has access to this will be able to perform actions on your behalf
PUSHBULLETTOKEN = ''
#######################################
# DO NOT CHANGE ANYTHHING BELOW HERE!!!
#######################################

# PagerDuty
PAGERDUTYURL="https://events.pagerduty.com/generic/2010-04-15/create_event.json" # Do not change

# Configure logging

# file - override on every start
logging.basicConfig(filename='li_webhook_shim.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# stdout
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

def parse(request):
    """ Parse JSON from alert webhook, return python dict or log exception """
    try:
        payload = request.get_json()
        # Need to support user alers and system notifications
        # Given different formats, some keys need to be checked
        alert = {
            "AlertName": payload['AlertName'],
            "info": payload['Info'] if 'Info' in payload else "",
            "Messages": payload['messages'],
            "url": payload['Url'] if 'Url' in payload else "",
            "editurl": payload['EditUrl'] if 'EditUrl' in payload else "",
            "HasMoreResults": payload['HasMoreResults'] if 'HasMoreResults' in payload else "",
            # may be less than length of messages, if there's more events
            "NumHits": payload['NumHits'] if 'NumHits' in payload else ""
        }
    except:
        logging.info("Body=%s" % request.get_data())
        logging.exception("Unexpected payload, is it in proper JSON format?")
        raise
    logging.info("Parsed=%s" % alert)
    return alert

def sendevent(url, payload, headers=None):
    """ Send payload in JSON to remote destination """
    if not headers:
        headers = {'Content-type': 'application/json'}
    try:
        logging.info("URL=%s" % url)
        logging.info("Headers=%s" % headers)
        logging.info("Body=%s" % payload)
        r = requests.post(url, headers=headers, data=payload)
        if r.status_code >= 200 and r.status_code < 300:
            return ("OK", r.status_code, None)
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise
    return ("Failed to POST event, error_code=%d" % r.status_code, r.status_code, None)

@app.route("/")
def root():
    return ("""<p>This is a demo shim for a VMware vRealize Log Insight 3.3 or newer webhook.<br/>
<b>IMPORTANT:</b> It is <b>NOT SUPPORTED</b> to run this shim on the Log Insight virtual appliance!!<br/><br/>
This shim features translations for:
<ul>
<li><b>Socialcast</b> (NOTE: payload must be under 1MB or webhook will fail)
<ul>
<li>/endpoint/socialcast -- Requires specifying a SOCIALCASTURL and sends up to 10 events</li>
<li>/endpoint/socialcast/<NUMRESULTS> -- Requires specifying a SOCIALCASTURL and passing the NUMRESULTS to be forwarded</li>
</ul>
<li><b>Slack</b> (/endpoint/slack) 
<ul>
<li>/endpoint/slack -- Requires specifying a SLACKURL and sends up to 10 events</li>
<li>/endpoint/slack/<NUMRESULTS> -- Requires specifying a SLACKURL and passing the NUMRESULTS to be forwarded</li>
</ul>
<li><b>PagerDuty</b> (NOTE: SERVICEKEY can be email address or integration key for service)
<ul>
<li>/endpoint/pagerduty/<SERVICEKEY> -- Requires passing a SERVICEKEY in the URL</li>
</ul>
<li><b>Pushbullet</b> (NOTE: PUSHBULLETTOKEN needs to be set on the shim)
<ul>
<li>/endpoint/pushbullet -- Sends a 'link' notification on all devices on pushbullet</li>
</ul>
<li><b>Test</b>
<ul>
<li>/endpoint/test -- Does not require anything and just dumps the body of the POST event</li>
</ul>
</ul><br/>
<b>IMPORTANT:</b> This code is current in <b>%s</b> status. Known issues:
<ul>
<li>This shim is very trusting; does not guarantee the notification source identity or require any shared secret</li>
<li>This shim does not convert HTML encoding so results may not appear on the destination in the desired output</li>
<li>This shim does not retry to send an event, it is fire and forget</li>
<li>No tests to ensure this shim respects the APIs it is calling</li>
<li>This shim has only partial exception handling and logging</li>
</ul><br/>
Please send feedback to: <a href=mailto:%s>%s</a></p>
""" % (__status__, __email__, __email__), 200, None)

@app.route("/endpoint/test", methods=['POST'])
def test():
    logging.info(request.get_data())
    return "OK"

@app.route("/endpoint/pushbullet", methods=['POST'])
def pushbullet():
    if not PUSHBULLETURL: return ("PUSHBULLET parameter must be set, please edit the shim!", 500, None)
    if not PUSHBULLETTOKEN: return ("PUSHBULLETTOKEN parameter must be set, please edit the shim!", 500, None)
    
    a = parse(request)
    
    payload = {
        "body" : a['info'],
        "title" : a['AlertName'],
        "type" : "link",
        "url" : a['url']
    }

    headers = {'Content-type': 'application/json', 'Access-Token' : PUSHBULLETTOKEN}
    
    return sendevent(PUSHBULLETURL, json.dumps(payload), headers)    

@app.route("/endpoint/socialcast", methods=['POST'])
@app.route("/endpoint/socialcast/<int:NUMRESULTS>", methods=['POST'])
def socialcast(NUMRESULTS=10):
    if not SOCIALCASTURL: return ("SOCIALCASTURL parameter must be set, please edit the shim!", 500, None)

    # Socialcast cares about the order of the information in the body
    # json.dumps() does not preserve the order so just use raw get_data()
    return sendevent(SOCIALCASTURL, request.get_data())

@app.route("/endpoint/slack", methods=['POST'])
@app.route("/endpoint/slack/<int:NUMRESULTS>", methods=['POST'])
def slack(NUMRESULTS=10):
    if not SLACKURL: return ("SLACKURL parameter must be set, please edit the shim!", 500, None)

    a = parse(request)

    slack_attachments = []
    try:
        for message in a['Messages'][:NUMRESULTS]:
            slack_attachments.append({
                "title": a['AlertName'],
                "title_link": a['url'],
                "color": "warning",
                "fallback": a['info'],
                "text": message.get('text', 'empty'),
                "fields": [{"title":f['name'], "value":f['content'], "short": True if len(f['content'])<20 else False} for f in message['fields'] if not f['name'].startswith('__') ],
                "pretext": a['info'] + ("\n\nYou can edit this alert by clicking: %s" % a['editurl'] if a['editurl'] else "")
            })
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise
    payload={
        "username": a['AlertName'],
        "icon_url": "http://blogs.vmware.com/management/files/2015/04/li-logo.png",
        "pretext": a['info'],
        "attachments": slack_attachments,
    }
    return sendevent(SLACKURL, json.dumps(payload))

@app.route("/endpoint/pagerduty", methods=['POST'])
@app.route("/endpoint/pagerduty/<SERVICEKEY>", methods=['POST'])
def pagerduty(SERVICEKEY=None):
    if not SERVICEKEY: return ("SERVICEKEY must be set in the URL (e.g. /endpoint/pagerduty/<SERVICEKEY>", 500, None)

    # Retrieve fields in notification
    a = parse(request)

    payload={
        "service_key": SERVICEKEY,
        "event_type": "trigger",
        "description": a['AlertName'],
        "details": {
            "notes": a['info'],
            "events": str(a['Messages']),
        },
        "contexts":[
            {
                "type": "link",
                "href": a['url'],
                "text": "View search results in Log Insight"
            },{
                "type": "link",
                "href": a['editurl'],
                "text": "View alert definition in Log Insight"
            }
        ]
    }
    return sendevent(PAGERDUTYURL, json.dumps(payload))

if __name__ == "__main__":
    logging.info("Please navigate to the below URL for the available options in this shim")
    app.run(host='0.0.0.0', port=PORT)
