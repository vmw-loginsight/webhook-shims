#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.groove

import conftest


client = loginsightwebhookdemo.app.test_client()


def test_groove_nourl():
    TOKEN = 'abc123'
    FROM = 'A'
    TO = 'B'

    rsp = client.post('/endpoint/groove', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/groove/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/groove/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/groove/' + TOKEN + '/' + FROM, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/groove/' + TOKEN + '/' + FROM + '/' + TO, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_groove_allparams():
    TOKEN = 'abc123'
    FROM = 'A'
    TO = 'B'
    loginsightwebhookdemo.groove.GROOVEURL = 'http://localhost'
    loginsightwebhookdemo.groove.GROOVEFROM = 'C'
    loginsightwebhookdemo.groove.GROOVETO = 'D'

    rsp = client.post('/endpoint/groove', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/groove/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/groove/' + TOKEN + '/' + FROM + '/' + TO, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
