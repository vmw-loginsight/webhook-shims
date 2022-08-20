#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Morteza Saeed Mohammadi"
__license__ = "Apache v2"
__verion__ = "1.0"


# melipayamak parameters
APIURL = '' #required Rest API
APIUSER = '' # required if not passed in URL
APIPASS = '' # required if SMSTOKEN or TOKEN is not specified
SMSNUMBER ='' # required from number
SMSTOKEN = '' # required if APIPASS is not specifed or TOKEN is not passed in URL
STAFFNUMBER = '' # the phone number's for sending mass SMS delimiter by , (comma)


@app.route("/endpoint/melipayamak", methods=['POST'])
@app.route("/endpoint/melipayamak/<NUMBER>/<TOKEN>", methods=['POST'])
@app.route("/endpoint/melipayamak/<MASS_SMS>/<TOKEN>", methods=['POST'])
def melipayamak(NUMBER=None, MASS_SMS=None, TOKEN=None):

    bauth = request.authorization
    if bauth is not None:
        global APIUSER
        global APIPASS
        APIUSER = bauth.username
        APIPASS = bauth.password

    a = parse(request)

    if (not APIURL or (not APIPASS and not SMSTOKEN and not TOKEN)):
        return ("melipayamak* parameters must be set, please edit the shim!", 500, None)

    # Prefer tokens over passwords
    if (SMSTOKEN != TOKEN):
        return("token is invalid")

    if (MASS_SMS == "mass_sms"):
        if (not STAFFNUMBER):
            return("melipayamak* staff numbers must be set, please edit the shim!", 500, None)
        NUMBER = STAFFNUMBER

    TEXT =  a['resourceName'] +' - '+ a['AlertName']
    payload = {'username': APIUSER, 'password': APIPASS, 'to': NUMBER, 'from': SMSNUMBER, 'text': TEXT }

    return callapi(APIURL, 'post', json.dumps(payload))
