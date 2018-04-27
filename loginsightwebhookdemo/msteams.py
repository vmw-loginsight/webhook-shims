#!/usr/bin/env python

"""
Create an incoming webhook for MS Teams: http://aka.ms/o365-connectors
Set TEAMSURL using the webhook URL that Teams provides.
"""


from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Doug Taliaferro"
__license__ = "Apache v2"
__verion__ = "1.0"


# Teams incoming webhook URL
TEAMSURL = ''


def teams_fields(message):
    return {
        "text": message.get('text', '') if 'text' in message else "Alert details",
        "facts": [
            {  # start of dict comprehension
                "name": f['name'],
                "value": f['content']
            } for f in message['fields'] if not f['name'].startswith('__')
        ]
    }


# Route without <ALERTID> are for LI, with are for vROps
@app.route("/endpoint/msteams", methods=['POST'])
@app.route("/endpoint/msteams/<ALERTID>", methods=['POST', 'PUT'])
@app.route("/endpoint/msteams/<ALERTID><int:NUMRESULTS>", methods=['POST', 'PUT'])
def msteams(NUMRESULTS=10, ALERTID=None):
    """
    Posts a message to a Microsoft Teams channel. Set TEAMSURL to the incoming
    webhook URL provided by Teams. To create a Teams webhook see:
    http://aka.ms/o365-connectors
    """

    if not TEAMSURL:
        return ("The TEAMSURL parameter must be set, please edit the shim!", 500, None)

    a = parse(request)

    teams_attachments = [
        {
            "activityImage": a['icon'],
            "activityTitle": a['AlertName'] if 'AlertName' in a else "Alert details",
            "activitySubtitle": "[Link to Alert](" + a['url'] + ")" if a['url'] else "",
        }
    ]

    try:
        if ('AlertName' in a):
            if ('Messages' in a):
                for message in a['Messages'][:NUMRESULTS]:
                    teams_attachments.append(teams_fields(message))
            if (a['fields'] is not None):
                teams_attachments.append(teams_fields(a))
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise

    if (a['color'] == 'red'):
        color = 'CC0000'
    elif (a['color'] == 'yellow'):
        color = 'FFCC00'
    elif (a['color'] == 'green'):
        color = '009000'
    else:
        color = '0075FF'

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color,
        "summary": "Message from " + a['hookName'],
        "sections": teams_attachments
    }

    # Defaults to Content-type: application/json
    # If changed you must specify the content-type manually
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if not headers:
        headers = None

    return callapi(TEAMSURL, 'post', json.dumps(payload), headers)
