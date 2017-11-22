#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.zendesk

import conftest

client = loginsightwebhookdemo.app.test_client()

EMAIL = 'test@example.com'
TOKEN = 'token1'


def test_zendesk_noparams():
    rsp = client.post('/endpoint/zendesk', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/zendesk/' + EMAIL, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk/' + EMAIL + '/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_zendesk_justurl():
    loginsightwebhookdemo.zendesk.ZENDESKURL = 'https://zendesk.vmwloginsight.com'

    rsp = client.post('/endpoint/zendesk', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk/' + EMAIL + '/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_zendesk_notoken():
    loginsightwebhookdemo.zendesk.ZENDESKURL = 'https://zendesk.vmwloginsight.com'
    loginsightwebhookdemo.zendesk.ZENDESKUSER = 'test'
    loginsightwebhookdemo.zendesk.ZENDESKPASS = 'changeme'

    rsp = client.post('/endpoint/zendesk', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk', data=conftest.payloadvROps60, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk', data=conftest.payloadLI_test, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk/' + EMAIL + '/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_zendesk_allparams():
    loginsightwebhookdemo.zendesk.ZENDESKURL = 'https://zendesk.vmwloginsight.com'
    loginsightwebhookdemo.zendesk.ZENDESKUSER = 'test'
    loginsightwebhookdemo.zendesk.ZENDESKPASS = 'changeme'
    loginsightwebhookdemo.zendesk.ZENDESKTOKEN = 'token'

    rsp = client.post('/endpoint/zendesk', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk', data=conftest.payloadvROps60, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk', data=conftest.payloadLI_test, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/zendesk/' + EMAIL + '/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
