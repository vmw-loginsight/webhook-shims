#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.socialcast

import conftest


client = loginsightwebhookdemo.app.test_client()

NUMRESULTS = '1'
TEAM = 'team1'
I = 'i'
X = 'x'


def test_socialcast_nourl():
    rsp = client.post('/endpoint/socialcast', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/socialcast/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/socialcast/' + NUMRESULTS, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/socialcast/' + TEAM, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/socialcast/' + TEAM + '/' + I, data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/socialcast/' + TEAM + '/' + I + '/' + X, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/socialcast/' + TEAM + '/' + I + '/' + X + '/' + NUMRESULTS, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_socialcast_allparams():
    loginsightwebhookdemo.socialcast.SOCIALCASTURL = 'https://' + TEAM + '.socialcast.com/api/webhooks/' + I + '/' + X

    rsp = client.post('/endpoint/socialcast', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/socialcast', data=conftest.payloadvROps60, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/socialcast', data=conftest.payloadLI_test, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/socialcast/' + NUMRESULTS, data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'


def test_socialcast_wrongx():
    X = 'y'
    loginsightwebhookdemo.socialcast.SOCIALCASTURL = 'https://' + TEAM + '.socialcast.com/api/webhooks/' + I + '/' + X

    rsp = client.post('/endpoint/socialcast', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
