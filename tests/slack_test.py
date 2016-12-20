#!/usr/bin/env python


import pytest

import loginsightwebhookdemo
import loginsightwebhookdemo.slack

import conftest


client = loginsightwebhookdemo.app.test_client()

NUMRESULTS = '1'
T = 'T3BCFGGDU'
B = 'B3BL90K4N'
X = 'Q8BojtVn1Pvjg510aCEOKNrd'


@pytest.mark.parametrize("url,post,data,expected", [
    # No URL
    (None,
        '/endpoint/slack',
        conftest.payload,
        '500 INTERNAL SERVER ERROR'),
    (None,
        '/endpoint/slack/',
        conftest.payload,
        '404 NOT FOUND'),
    (None,
        '/endpoint/slack/' + NUMRESULTS,
        conftest.payload,
        '500 INTERNAL SERVER ERROR'),
    (None,
        '/endpoint/slack/' + T,
        conftest.payload,
        '405 METHOD NOT ALLOWED'),
    (None,
        '/endpoint/slack/' + T + '/' + B,
        conftest.payload,
        '404 NOT FOUND'),
    (None,
        '/endpoint/slack/' + T + '/' + B + '/' + X,
        conftest.payload,
        '200 OK'),
    (None,
        '/endpoint/slack/' + T + '/' + B + '/' + X + '/' + NUMRESULTS,
        conftest.payload,
        '200 OK'),
    # All params
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack',
        conftest.payload,
        '200 OK'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack',
        conftest.payloadvROps60,
        '200 OK'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack',
        conftest.payloadLI_test,
        '200 OK'),
    ('https://hooks.slack.com/services/' + T + '/' + B + '/' + X,
        '/endpoint/slack/' + NUMRESULTS,
        conftest.payload,
        '200 OK'),
    # Wrong URL
    ('https://vmw-loginsight.slack.com',
        '/endpoint/slack',
        conftest.payload,
        '500 INTERNAL SERVER ERROR'),
    ('https://hooks.slack.com/services/a/b/c',
        '/endpoint/slack',
        conftest.payload,
        '404 NOT FOUND'),
])
def test_slack(url, post, data, expected):
    if url is not None:
        loginsightwebhookdemo.slack.SLACKURL = url
    rsp = client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected
