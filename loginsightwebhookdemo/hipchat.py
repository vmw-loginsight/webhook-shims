#!/usr/bin/env python

"""
HipChat API makes it difficult to get feature parity with Slack shim.
Opted for a single message and leveraged the HTML driven activity option.
This may need to be revisited in the future.
"""

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"
__version__ = "1.0"


# HipChat incoming webhook URL. For more information see https://www.hipchat.com/docs/apiv2/method/send_room_notification
HIPCHATURL = ''


#@app.route("/endpoint/hipchat/<int:NUMRESULTS>", methods=['POST'])
#@app.route("/endpoint/hipchat/<TEAM>/<ROOMNUM>/<AUTHTOKEN>/<int:NUMRESULTS>", methods=['POST'])
#@app.route("/endpoint/hipchat/<TEAM>/<ROOMNUM>/<AUTHTOKEN>/<int:NUMRESULTS>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/hipchat", methods=['POST'])
@app.route("/endpoint/hipchat/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/hipchat/<int:NUMRESULTS>/<ALERTID>", methods=['PUT'])
@app.route("/endpoint/hipchat/<TEAM>/<ROOMNUM>/<AUTHTOKEN>", methods=['POST'])
@app.route("/endpoint/hipchat/<TEAM>/<ROOMNUM>/<AUTHTOKEN>/<ALERTID>", methods=['PUT'])
def hipchat(NUMRESULTS=1, ALERTID=None, TEAM=None, ROOMNUM=None, AUTHTOKEN=None):
    """
    Consume messages, and send them to HipChat as an Attachment object.
    If `TEAM/ROOMNUM/AUTHOKEN` is not passed, requires `HIPCHATURL` defined in the form `https://TEAM.hipchat.com/v2/room/0000000/notification?auth_token=XXXXXXXXXXXXXXXXXXXXXXXXXXX`
    For more information, see https://www.hipchat.com/docs/apiv2/method/send_room_notification
    """
    if (AUTHTOKEN is not None):
        URL = 'https://' + TEAM + '.hipchat.com/v2/room/' + ROOMNUM + '/notification?auth_token=' + AUTHTOKEN
    if not HIPCHATURL:
        return ("HIPCHATURL parameter must be set, please edit the shim!", 500, None)
    else:
        URL = HIPCHATURL

    a = parse(request)

    hipchat_attachments = []
    attachment_prefix = {
        "style": "application",
        "format": "medium",
        "id": "1",
    }
    try:
        attachment = {
            "icon": { "url": a['icon'] },
        }
        # Log Insight
        if ('Messages' in a):
            for message in a['Messages'][:NUMRESULTS]:
                attachment.update(attachment_prefix)
                attachment.update({
                    "title": a['AlertName'],
                })
                if (a['url'] != ""):
                    attachment.update({
                        "url": a['url'],
                        "activity": {
                            "html": a['moreinfo'],
                        }
                    })
                elif (message['text'] is not None):
                    attachment.update({
                        "activity": {
                            "html": message['text'],
                        }
                    })
                if (message['fields'] is not None):
                    message['fields'] = message['fields'] + a['fields']
                    attachment.update({
                        "attributes": [{  # start of dict comprehension
                            "label": f['name'],
                            "value": { "label": f['content'] }
                        } for f in message['fields'] if not f['name'].startswith('__')],
                    })
                hipchat_attachments.append(attachment)
                attachment = {} # only attach the icon to the first card
        # Additional information (non-product specific)
        elif (a['fields'] is not None):
            attachment.update(attachment_prefix)
            attachment.update({
                "title": a['AlertName'],
                "activity": {
                    "html": a['moreinfo'],
                },
                "attributes": [{  # start of dict comprehension
                    "label": f['name'],
                    "value": { "label": f['content'] }
                } for f in a['fields']],
            })
            hipchat_attachments.append(attachment)
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise
    if not hipchat_attachments: # If a test alert
        attachment.update(attachment_prefix)
        attachment.update({
            "title": "This is a test webhook alert",
            "attributes": [
                {  # start of dict comprehension
                    "label": "Test",
                    "value": { "label": "It works!" }
                }
            ],
            "icon": { "url": "http://blogs.vmware.com/management/files/2015/04/li-logo.png" },
        })
        hipchat_attachments.append(attachment)

    payload = {
        "from": a['hookName'],
        "color": a['color'] if ('color' in a and a['color'] is not None) else "gray",
        "message_format": "text",
        "message": a['moreinfo'],
        "notify": 'true',
        "card": hipchat_attachments.pop(0),
    }
    return callapi(URL, 'post', json.dumps(payload))
