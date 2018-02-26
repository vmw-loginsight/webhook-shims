#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.bigpanda

import conftest


client = loginsightwebhookdemo.app.test_client()

TOKEN = 'a-b-c-d'
APPKEY = 'abc123'


def test_bigpanda_nourl():
    loginsightwebhookdemo.bigpanda.bigpandaURL = ''

    rsp = client.post('/endpoint/bigpanda', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/bigpanda/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/bigpanda/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/bigpanda/' + TOKEN + '/' + APPKEY, data=conftest.payload, content_type="application/json")
    assert rsp.status == '401 UNAUTHORIZED'


def test_bigpanda_allparams():
    loginsightwebhookdemo.bigpanda.bigpandaURL = 'https://api.bigpanda.io/data/v2/alerts'

    rsp = client.post('/endpoint/bigpanda/' + TOKEN + '/' + APPKEY, data=conftest.payload, content_type="application/json")
    assert rsp.status == '401 UNAUTHORIZED'
    rsp = client.post('/endpoint/bigpanda/' + TOKEN + '/' + APPKEY, data=conftest.payloadvROps60, content_type="application/json")
    assert rsp.status == '401 UNAUTHORIZED'
    rsp = client.post('/endpoint/bigpanda/' + TOKEN + '/' + APPKEY, data=conftest.payloadLI_test, content_type="application/json")
    assert rsp.status == '401 UNAUTHORIZED'
