#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.pushbullet

import conftest

client = loginsightwebhookdemo.app.test_client()

TOKEN = 'token'


def test_pushbullet_noparams():
    loginsightwebhookdemo.pushbullet.PUSHBULLETURL = ''

    rsp = client.post('/endpoint/pushbullet', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/pushbullet/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/pushbullet/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_pushbullet_justurl():
    rsp = client.post('/endpoint/pushbullet', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/pushbullet/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_pushbullet_allparams():
    loginsightwebhookdemo.pushbullet.PUSHBULLETTOKEN = 'token2'

    rsp = client.post('/endpoint/pushbullet', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/pushbullet/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
