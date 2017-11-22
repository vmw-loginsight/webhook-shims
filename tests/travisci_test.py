#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.travisci

import conftest

client = loginsightwebhookdemo.app.test_client()

TOKEN = 'abc123'
REPO = 'repo1'
BRANCH = 'branch1'


def test_travisci_noparams():
    rsp = client.post('/endpoint/travisci', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/travisci/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/travisci/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/travisci/' + TOKEN + '/' + REPO, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/travisci/' + TOKEN + '/' + REPO + '/' + BRANCH, data=conftest.payload, content_type="application/json")
    assert rsp.status == '403 FORBIDDEN'


def test_travisci_allparams():
    loginsightwebhookdemo.travisci.TRAVISCITOKEN = 'def456'
    loginsightwebhookdemo.travisci.TRAVISCIREPO = 'repo2'
    loginsightwebhookdemo.travisci.TRAVISCIBRANCH = 'branch2'

    rsp = client.post('/endpoint/travisci', data=conftest.payload, content_type="application/json")
    assert rsp.status == '403 FORBIDDEN'
    rsp = client.post('/endpoint/travisci/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '403 FORBIDDEN'
    rsp = client.post('/endpoint/travisci/' + TOKEN + '/' + REPO, data=conftest.payload, content_type="application/json")
    assert rsp.status == '403 FORBIDDEN'
    rsp = client.post('/endpoint/travisci/' + TOKEN + '/' + REPO + '/' + BRANCH, data=conftest.payload, content_type="application/json")
    assert rsp.status == '403 FORBIDDEN'
