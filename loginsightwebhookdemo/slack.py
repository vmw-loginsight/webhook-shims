#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Alan Castonguay and Steve Flanders"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"
__version__ = "2.0"


# Slack incoming webhook URL. For more information see https://api.slack.com/incoming-webhooks
SLACKURL = ''


@app.route("/endpoint/slack", methods=['POST'])
@app.route("/endpoint/slack/<int:NUMRESULTS>", methods=['POST'])
@app.route("/endpoint/slack/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/slack/<int:NUMRESULTS>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/slack/<T>/<B>/<X>", methods=['POST'])
@app.route("/endpoint/slack/<T>/<B>/<X>/<int:NUMRESULTS>", methods=['POST'])
@app.route("/endpoint/slack/<T>/<B>/<X>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/slack/<T>/<B>/<X>/<int:NUMRESULTS>/<ALERTID>", methods=['PUT'])
def slack(NUMRESULTS=10, ALERTID=None, T=None, B=None, X=None):
    """
    Consume messages, and send them to Slack as an Attachment object.
    Sends up to `NUMRESULTS` (default 10) events onward.
    If `T/B/X` is not passed, requires `SLACKURL` defined in the form `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
    For more information, see https://api.slack.com/incoming-webhooks
    """
    if (X is not None):
        URL = 'https://hooks.slack.com/services/' + T + '/' + B + '/' + X
    if not SLACKURL:
        return ("SLACKURL parameter must be set, please edit the shim!", 500, None)
    else:
        URL = SLACKURL

    a = parse(request)

    slack_attachments = []
    if (a['color'] == 'red'):
        color = 'danger'
    elif (a['color'] == 'yellow'):
        color = 'warning'
    else:
        color = 'info'
    try:
        payload = {
            "icon_url": a['icon'],
        }
        if ('AlertName' in a):
            attachment = { "pretext": a['moreinfo'], }
            if ('Messages' in a):
                for message in a['Messages'][:NUMRESULTS]:
                    attachment.update({
                        "color": color,
                        "fallback": message.get('text', ''),
                        "text": message.get('text', ''),
                        "fields": [
                            {  # start of dict comprehension
                                "title": f['name'],
                                "value": f['content'],
                                "short": True if len(f['content']) < 20 else False
                            } for f in message['fields'] if not f['name'].startswith('__')
                        ],
                    })
                    slack_attachments.append(attachment)
                    attachment = {}
            if a['fields']:
                attachment.update({
                    "color": color,
                    "fallback": 'Alert details',
                    "text": 'Alert details',
                    "fields": [
                        {  # start of dict comprehension
                            "title": f['name'],
                            "value": f['content']
                        } for f in a['fields']
                    ],
                })
        else:
            if a['fields']:
                slack_attachments.append({
                    "color": color,
                    "fallback": 'Alert details',
                    "text": 'Alert details',
                    "fields": [
                        {  # start of dict comprehension
                            "title": f['name'],
                            "value": f['content']
                        } for f in a['fields']
                    ],
                })
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise
    if not slack_attachments: # If a test alert
        slack_attachments.append({
            "text": "This is a test webhook alert",
            "color": "info",
            "fallback": "This is a test webhook alert",
            "fields": [
                {
                    "title": "Test",
                    "value": "It works!"
                }
            ],
            "pretext": "Hello from Log Insight!"
        })

    payload.update({
        "username": a['hookName'],
        "attachments": slack_attachments
    })
    return callapi(URL, 'post', json.dumps(payload))
