#!/usr/bin/env python


import json
import uuid

import loginsightwebhookdemo
import loginsightwebhookdemo.bugzilla


client = loginsightwebhookdemo.app.test_client()

# Cannot add AlertName as must be unique for testing
payload_base = {
    "messages": [
        {
            "text": "hello world 1",
            "timestamp": 1451940578545,
            "fields": []
        }
    ]
}

URL = 'https://landfill.bugzilla.org/bugzilla-5.0-branch/'
TOKEN = 'BR8zMD8ywOJSAgRnjylr4G3pa7Zx5zKE6U3xYl76'
PRODUCT = 'MyOwnBadSelf'
COMPONENT = 'Comp1'
VERSION = 'unspecified'


# Need to generate a unique, random bug ID to test
def generate_alertname():
    bugid = str(uuid.uuid4())
    payload = payload_base
    payload.update({"AlertName": bugid})
    return json.dumps(payload)


def test_bugzilla_noparams():
    loginsightwebhookdemo.bugzilla.BUGZILLAURL = ''
    loginsightwebhookdemo.bugzilla.BUGZILLAUSER = ''
    loginsightwebhookdemo.bugzilla.BUGZILLAPASS = ''
    loginsightwebhookdemo.bugzilla.BUGZILLAPRODUCT = ''
    loginsightwebhookdemo.bugzilla.BUGZILLACOMPONENT = ''
    loginsightwebhookdemo.bugzilla.BUGZILLAVERSION = ''
    loginsightwebhookdemo.bugzilla.VERIFY = ''
    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla', data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/bugzilla/', data=payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/bugzilla/' + TOKEN, data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/bugzilla/' + TOKEN + '/' + PRODUCT, data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/bugzilla/' + TOKEN + '/' + PRODUCT + '/' + COMPONENT, data=payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/bugzilla/' + TOKEN + '/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_bugzilla_wrongpass():
    loginsightwebhookdemo.bugzilla.BUGZILLAURL = 'https://landfill.bugzilla.org/bugzilla-5.0-branch/'
    loginsightwebhookdemo.bugzilla.BUGZILLAUSER = 'loginsight-marketplace@vmware.com'
    loginsightwebhookdemo.bugzilla.BUGZILLAPASS = 'wrongpass'
    loginsightwebhookdemo.bugzilla.BUGZILLAPRODUCT = 'MyOwnBadSelf'
    loginsightwebhookdemo.bugzilla.BUGZILLACOMPONENT = 'comp2'
    loginsightwebhookdemo.bugzilla.BUGZILLAVERSION = 'unspecified'
    loginsightwebhookdemo.bugzilla.VERIFY = True
    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla/' + TOKEN, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'

    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla/' + TOKEN + '/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'

    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla/-/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '401 UNAUTHORIZED'


def test_bugzilla_nopass():
    loginsightwebhookdemo.bugzilla.BUGZILLAPASS = ''
    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla/' + TOKEN, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'
    rsp = client.post('/endpoint/bugzilla', data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/bugzilla/-/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_bugzilla_wrongtoken():
    loginsightwebhookdemo.bugzilla.BUGZILLAPASS = 'L0g1ns1ght!'
    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla/wrongtoken', data=payload, content_type="application/json")
    assert rsp.status == '400 BAD REQUEST'
    rsp = client.post('/endpoint/bugzilla/wrongtoken/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '400 BAD REQUEST'


def test_bugzilla_allparams_allurl():
    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla/-/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    # This does not confirm that VERSION is used instead of loginsightwebhookdemo.bugzilla.VERSION
    # Handled in test_bugzilla_e2e
    assert rsp.status == '200 OK'


def test_bugzilla_notoken():
    payload = generate_alertname()

    rsp = client.post('/endpoint/bugzilla', data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


# Generate a payload that can be re-used for the rest of the tests
payload = generate_alertname()


def test_bugzilla_noverify():
    loginsightwebhookdemo.bugzilla.VERIFY = False

    rsp = client.post('/endpoint/bugzilla/' + TOKEN + '/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


# Try to post with the same AlertName to ensure that update works as well
def test_bugzilla_update():
    rsp = client.post('/endpoint/bugzilla/' + TOKEN + '/' + PRODUCT + '/' + COMPONENT + '/' + VERSION, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


# GET last bug and confirm output contains AlertName, Info, Url, and EditUrl
# Ensure that VERSION is used instead of loginsightwebhookdemo.bugzilla.VERSION
def test_bugzilla_e2e():
    url = URL + '/rest/bug?api_key=' + TOKEN + '&product=' + PRODUCT + '&component=' + COMPONENT + '&summary=' + json.loads(payload)['AlertName']
    id = json.loads(loginsightwebhookdemo.callapi(url, 'get'))['bugs'][0]['id']
    url = URL + '/rest/bug/' + str(id) + '/comment?api_key=' + TOKEN + '&product=' + PRODUCT + '&component=' + COMPONENT + '&summary=' + json.loads(payload)['AlertName']
    assert json.loads(loginsightwebhookdemo.callapi(url, 'get'))['bugs'][str(id)]['comments'][1]['text'] == json.loads(payload)['AlertName'] + '\n\nhello world 1'
