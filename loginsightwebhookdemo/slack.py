#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, sendevent
from flask import request, json
import logging


__author__ = "Alan Castonguay"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"


# Slack incoming webhook URL. For more information see https://api.slack.com/incoming-webhooks
SLACKURL = ''


@app.route("/endpoint/slack", methods=['POST'])
@app.route("/endpoint/slack/<int:NUMRESULTS>", methods=['POST'])
def slack(NUMRESULTS=10):
    """
    Consume messages, and send them to Slack as an Attachment object.
    Sends up to `NUMRESULTS` (default 10) events onward.
    Requires `SLACKURL` defined in the form `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
    For more information, see https://api.slack.com/incoming-webhooks
    """
    if not SLACKURL:
        return ("SLACKURL parameter must be set, please edit the shim!", 500, None)

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
                "fields": [
                    {  # start of dict comprehension
                        "title": f['name'],
                        "value": f['content'],
                        "short": True if len(f['content']) < 20 else False
                    } for f in message['fields'] if not f['name'].startswith('__')
                ],
                "pretext": a['info'] + ("\n\nYou can edit this alert by clicking: %s" % a['editurl'] if a['editurl'] else "")
            })
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise
    payload = {
        "username": a['AlertName'],
        "icon_url": "http://blogs.vmware.com/management/files/2015/04/li-logo.png",
        "pretext": a['info'],
        "attachments": slack_attachments,
    }
    return sendevent(SLACKURL, json.dumps(payload))
