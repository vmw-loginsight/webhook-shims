#!/usr/bin/env python

"""
This is a demo shim that accepts incoming webhooks, implemented using Flask.

Run this directly on your development machine or under any WSGI webserver.
The following functions parse the webhook payload, translate and send it to other services.
"""

from loginsightwebhookdemo import app
import logging
import sys


# Define if you want to leverage SSL
SSLCERT = ''
SSLKEY = ''

def main(PORT):
    # Configure logging - overwrite on every start
    logging.basicConfig(filename='li_webhook_shim.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    # stdout
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    logging.info("Please navigate to the below URL for the available routes")

    if (SSLCERT and SSLKEY):
        context = (SSLCERT, SSLKEY)
        app.run(host='0.0.0.0', port=PORT, ssl_context=context, threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    PORT = 5001
    if (len(sys.argv) == 2):
        PORT = sys.argv[1]
    main(PORT)
