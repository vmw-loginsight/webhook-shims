#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.opsgenie

import conftest


client = loginsightwebhookdemo.app.test_client()

APIKEY = 'abc123'
TEAM = 'team1'


def test_opsgenie_nourl():
    loginsightwebhookdemo.opsgenie.OPSGENIEURL = ''

    rsp = client.post('/endpoint/opsgenie', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/opsgenie/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/opsgenie/' + APIKEY, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_opsgenie_allparams():
    loginsightwebhookdemo.opsgenie.OPSGENIEURL = 'https://api.opsgenie.com/v2/alerts'

    rsp = client.post('/endpoint/opsgenie/' + APIKEY, data=conftest.payload, content_type="application/json")
    assert rsp.status == '422 UNPROCESSABLE ENTITY'
    rsp = client.post('/endpoint/opsgenie/' + APIKEY, data=conftest.payloadvROps60, content_type="application/json")
    assert rsp.status == '422 UNPROCESSABLE ENTITY'
    rsp = client.post('/endpoint/opsgenie/' + APIKEY, data=conftest.payloadLI_test, content_type="application/json")
    assert rsp.status == '422 UNPROCESSABLE ENTITY'
