#!/usr/bin/env python


import pytest

import loginsightwebhookdemo.vrealizeorchestrator

import conftest


URL = 'mock.test'
WORKFLOWID = 'abc123'
USER = 'admin'
PASSWORD = 'changeme'
TOKEN = 'token'
HOK = 'hok'

WRONGWORKFLOWID = '!@#$'


@pytest.mark.parametrize("url,user,password,token,hok,post,data,expected", [
    (None, None, None, None, None, '/endpoint/vro', conftest.payload, '404 NOT FOUND'),
    (None, None, None, None, None, '/endpoint/vro/', conftest.payload, '404 NOT FOUND'),
    (None, None, None, None, None, '/endpoint/vro/' + WORKFLOWID, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (None, None, None, None, None, '/endpoint/vro/' + WORKFLOWID, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, None, None, None, None, '/endpoint/vro/' + WORKFLOWID, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, None, None, '/endpoint/vro/' + WORKFLOWID, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, TOKEN, None, '/endpoint/vro/' + WORKFLOWID, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, TOKEN, HOK, '/endpoint/vro/' + WORKFLOWID, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, TOKEN, HOK, '/endpoint/vro/' + WORKFLOWID + '/oauth/' + TOKEN, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, TOKEN, HOK, '/endpoint/vro/' + WORKFLOWID + '/sso/' + HOK, conftest.payload, '500 INTERNAL SERVER ERROR'),
])
def test_vro_nourl(url, user, password, token, hok, post, data, expected):
    if user:
        loginsightwebhookdemo.vrealizeorchestrator.VROUSER = user
    if password:
        loginsightwebhookdemo.vrealizeorchestrator.VROUSER = password
    if token:
        loginsightwebhookdemo.vrealizeorchestrator.VROTOKEN = token
    if hok:
        loginsightwebhookdemo.vrealizeorchestrator.VROHOK = hok

    rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected
