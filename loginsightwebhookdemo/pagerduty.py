#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, sendevent
from flask import request
import logging


__author__ = "Steve Flanders"
__license__ = "Apache v2"


# PagerDuty post url defined by https://v2.developer.pagerduty.com/v2/docs/trigger-events - don't change
PAGERDUTYURL = 'https://events.pagerduty.com/generic/2010-04-15/create_event.json'


@app.route("/endpoint/pagerduty/<SERVICEKEY>", methods=['POST'])
def pagerduty(SERVICEKEY=None):
    """
    Create a new incident for the Pagerduty service identified by `SERVICEKEY` in the URL.
    Uses the https://v2.developer.pagerduty.com/v2/docs/trigger-events API directly.
    """
    if not SERVICEKEY:
        return ("SERVICEKEY must be set in the URL (e.g. /endpoint/pagerduty/<SERVICEKEY>", 500, None)

    # Retrieve fields in notification
    a = parse(request)

    payload = {
        "service_key": SERVICEKEY,
        "event_type": "trigger",
        "description": a['AlertName'],
        "details": {
            "notes": a['info'],
            "events": str(a['Messages']),
        },
        "contexts": [
            {
                "type": "link",
                "href": a['url'],
                "text": "View search results"
            }, {
                "type": "link",
                "href": a['editurl'],
                "text": "View alert definition"
            },
        ]
    }
    return sendevent(PAGERDUTYURL, json.dumps(payload))
