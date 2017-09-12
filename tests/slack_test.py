#!/usr/bin/env python


import pytest

import loginsightwebhookdemo.slack

import conftest


NUMRESULTS = '1'
T = 'T3BCFGGDU'
B = 'B3BL90K4N'
X = 'Q8BojtVn1Pvjg510aCEOKNrd'


@pytest.mark.parametrize("url,post,data,expected,method", [
    # No URL
    (None,
        '/endpoint/slack',
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (None,
        '/endpoint/slack/',
        conftest.payload,
        '404 NOT FOUND', 'POST'),
    (None,
        '/endpoint/slack/alertid/' + NUMRESULTS,
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'PUT'),
    (None,
        '/endpoint/slack/' + T,
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (None,
        '/endpoint/slack/' + T + '/' + B,
        conftest.payload,
        '404 NOT FOUND', 'POST'),
    (None,
        '/endpoint/slack/' + T + '/' + B + '/' + X,
        conftest.payload,
        '200 OK', 'POST'),
    (None,
        '/endpoint/slack/' + T + '/' + B + '/' + X + '/alertid',
        conftest.payloadvROps60,
        '200 OK', 'PUT'),
    (None,
        '/endpoint/slack/' + T + '/' + B + '/' + X + '/alertid' + NUMRESULTS,
        conftest.payloadvROps62,
        '200 OK', 'PUT'),
    # All params
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack',
        conftest.payload,
        '200 OK', 'POST'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X + '/alertid',
        '/endpoint/slack',
        conftest.payloadvROps60,
        '200 OK', 'POST'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X + '/alertid',
        '/endpoint/slack',
        conftest.payloadvROps62,
        '200 OK', 'POST'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack',
        conftest.payloadLI_test,
        '200 OK', 'POST'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack/' + NUMRESULTS,
        conftest.payload,
        '200 OK', 'POST'),
    # Wrong URL
    ('https://vmw-loginsight.slack.com',
        '/endpoint/slack',
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'POST'),
    ('https://hooks.slack.com/services/a/b/c',
        '/endpoint/slack',
        conftest.payload,
        '404 NOT FOUND', 'POST'),
])
def test_slack(url, post, data, expected, method):
    if url is not None:
        loginsightwebhookdemo.slack.SLACKURL = url
    if method == 'PUT':
        rsp = conftest.client.put(post, data=data, content_type="application/json")
    else:
        rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected
