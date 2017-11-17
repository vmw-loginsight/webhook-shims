#!/usr/bin/env python


import json
import uuid

import loginsightwebhookdemo
import loginsightwebhookdemo.pivotaltracker


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

TOKEN = '688555f2e3ca466d7586953749332828'
PROJECT = '1938421'


# Need to generate a unique, random bug ID to test
def generate_alertname():
    bugid = str(uuid.uuid4())
    payload = payload_base
    payload.update({"AlertName": bugid})
    return json.dumps(payload)


def test_pivotaltracker_noparams():
    payload = generate_alertname()

    rsp = client.post('/endpoint/pivotaltracker', data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/pivotaltracker/', data=payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/pivotaltracker/' + TOKEN, data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/pivotaltracker/' + TOKEN + '/' + PROJECT, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


def test_pivotaltracker_wrongtoken():
    loginsightwebhookdemo.pivotaltracker.PIVOTALTRACKERTOKEN = 'wrongtoken'
    loginsightwebhookdemo.pivotaltracker.PIVOTALTRACKERPROJECT = 'project1'
    payload = generate_alertname()

    rsp = client.post('/endpoint/pivotaltracker', data=payload, content_type="application/json")
    assert rsp.status == '403 FORBIDDEN'


payload = generate_alertname()


def test_pivotaltracker_allparams_allurl():
    loginsightwebhookdemo.pivotaltracker.PIVOTALTRACKERTOKEN = 'wrongtoken'
    loginsightwebhookdemo.pivotaltracker.PIVOTALTRACKERPROJECT = 'project1'

    rsp = client.post('/endpoint/pivotaltracker/' + TOKEN + '/' + PROJECT, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


# Try to post with the same AlertName
def test_pivotaltracker_update():
    rsp = client.post('/endpoint/pivotaltracker/' + TOKEN + '/' + PROJECT, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'
