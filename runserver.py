#!/usr/bin/env python

"""
This is a demo shim that accepts alert webhooks from VMware vRealize Log Insight 3.3 or newer, implemented using Flask.

Run this directly on your development machine or under any WSGI webserver, within the Log Insight virtual appliance.
The following functions parse the Alert webhook payload from Log Insight, translate and send it to other services.
"""

from loginsightwebhookdemo import app
import logging
import sys


if __name__ == "__main__":
    # Configure logging

    # file - overwrite on every start
    logging.basicConfig(filename='li_webhook_shim.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    # stdout
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    logging.info("Please navigate to the below URL for the available routes")

    app.run(host='0.0.0.0', port=5001)
