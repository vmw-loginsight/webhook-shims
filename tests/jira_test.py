#!/usr/bin/env python


import pytest

import loginsightwebhookdemo
import loginsightwebhookdemo.jira

import conftest

client = loginsightwebhookdemo.app.test_client()

URL = 'https://jira.vmwloginsight.com'
USER = 'test'
PASSWORD = 'changeme'
PROJECT = 'proj1'


@pytest.mark.parametrize("url,user,password,post,data,expected", [
    (None, None, None, '/endpoint/jira', conftest.payload, '404 NOT FOUND'),
    (None, None, None, '/endpoint/jira/' + PROJECT, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, '/endpoint/jira/' + PROJECT, conftest.payload, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, '/endpoint/jira/' + PROJECT, conftest.payloadvROps60, '500 INTERNAL SERVER ERROR'),
    (URL, USER, PASSWORD, '/endpoint/jira/' + PROJECT, conftest.payloadLI_test, '500 INTERNAL SERVER ERROR'),
])
def test_jira(url, user, password, post, data, expected):
    if url is not None:
        loginsightwebhookdemo.jira.JIRAURL = url
    if user is not None:
        loginsightwebhookdemo.jira.JIRAUSER = user
    if password is not None:
        loginsightwebhookdemo.jira.JIRAPASS = password
    rsp = client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected
