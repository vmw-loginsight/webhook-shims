#!/usr/bin/env python

"""
#Demo

This is a demo shim that accepts alert webhooks from VMware vRealize Log Insight 3.3 or newer, implemented using Flask.
You can invoke `runserver.py` directly on your development machine or run the Flask app under any WSGI webserver.
Don't run it within the Log Insight virtual appliance, though.

As a demonstration, these shims are optimized for readabiility.
There is minimal error handling and no attempt to retransmit.
HTTP errors are passed back to Log Insight.

Please send feedback to https://github.com/vmw-loginsight/webhook-shims/issues or mailto:li-cord@vmware.com - pull requests welcome.

The following functions parse the Alert webhook payload from Log Insight, translate and send it to other services.
"""

from flask import Flask, Markup, request, json
import requests
import logging
import re

app = Flask(__name__)

__author__ = "Alan Castonguay and Steve Flanders"
__copyright__ = "Copyright 2016"
__credits__ = ["Alan Castonguay", "Steve Flanders"]
__license__ = "Apache v2"
__version__ = "2.0"
__maintainer__ = "Alan Castonguay and Steve Flanders"
__email__ = "li-cord@vmware.com"
__status__ = "Beta"


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
    Parse JSON from alert webhook.
    Returns a dict or logs an exception.
    """
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
            "HasMoreResults": payload['HasMoreResults'] if 'HasMoreResults' in payload else False,
            # may be less than length of messages, if there's more events
            "NumHits": payload['NumHits'] if 'NumHits' in payload else 0
        }
    except:
        logging.info("Body=%s" % request.get_data())
        logging.exception("Unexpected payload, is it in proper JSON format?")
        raise
    logging.info("Parsed=%s" % alert)
    return alert


def sendevent(url, payload, headers=None):
    """
    Simple wrapper around `requests.post`, with excessive logging.
    Returns a Flask-friendly tuple on success or failure.
    Logs and re-raises any exceptions.
    """
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
        raise  # re-raise all exceptions
    return ("Failed to POST event, error_code=%d" % r.status_code, r.status_code, None)


@app.route("/")
def introduction():
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
def test():
    """Log the request and respond with success. Don't send the payload anywhere."""
    logging.info(request.get_data())
    return "OK"


# Import individual shims
import loginsightwebhookdemo.pagerduty
import loginsightwebhookdemo.pushbullet
import loginsightwebhookdemo.slack
import loginsightwebhookdemo.socialcast
import loginsightwebhookdemo.vrealizeorchestrator
