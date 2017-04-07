#!/usr/bin/env python


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Alan Castonguay and Steve Flanders"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"
__version__ = "2.1"


# Slack incoming webhook URL. For more information see https://api.slack.com/incoming-webhooks
SLACKURL = ''


def slack_fields(color, message):
    return {
        "color": color,
        "fallback": message.get('text', '') if 'text' in message else "Alert details",
        "text": message.get('text', '') if 'text' in message else "Alert details",
        "fields": [
            {  # start of dict comprehension
                "title": f['name'],
                "value": f['content'],
                "short": True if len(f['content']) < 20 else False
            } for f in message['fields'] if not f['name'].startswith('__')
        ]
    }


@app.route("/endpoint/slack", methods=['POST'])
@app.route("/endpoint/slack/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/slack/<ALERTID>/<int:NUMRESULTS>", methods=['POST','PUT'])
@app.route("/endpoint/slack/<T>/<B>/<X>", methods=['POST'])
@app.route("/endpoint/slack/<T>/<B>/<X>/<ALERTID>", methods=['POST','PUT'])
@app.route("/endpoint/slack/<T>/<B>/<X>/<ALERTID>/<int:NUMRESULTS>", methods=['POST','PUT'])
def slack(NUMRESULTS=10, ALERTID=None, T=None, B=None, X=None):
    """
    Consume messages, and send them to Slack as an Attachment object.
    Sends up to `NUMRESULTS` (default 10) events onward.
    If `T/B/X` is not passed, requires `SLACKURL` defined in the form `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
    For more information, see https://api.slack.com/incoming-webhooks
    """
    # Prefer URL parameters to SLACKURL
    if X is not None:
        URL = 'https://hooks.slack.com/services/' + T + '/' + B + '/' + X
    elif not SLACKURL or not 'https://hooks.slack.com/services' in SLACKURL:
        return ("SLACKURL parameter must be set properly, please edit the shim!", 500, None)
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
    payload = {
        "icon_url": a['icon'],
    }
    try:
        if ('AlertName' in a):
            slack_attachments.append({ "pretext": a['moreinfo'], })
            if ('Messages' in a):
                for message in a['Messages'][:NUMRESULTS]:
                    slack_attachments.append(slack_fields(color, message))
            if a['fields']:
                slack_attachments.append(slack_fields(color, a))
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise

    payload.update({
        "username": a['hookName'],
        "attachments": slack_attachments
    })
    return callapi(URL, 'post', json.dumps(payload))
