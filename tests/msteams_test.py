#!/usr/bin/env python


import pytest

import loginsightwebhookdemo.slack

import conftest


NUMRESULTS = '1'
# A public URL for testing Teams is not available
URL = 'https://mock.test'


@pytest.mark.parametrize("url,post,data,expected,method", [
    # No URL
    (None,
        '/endpoint/msteams',
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (None,
        '/endpoint/msteams/',
        conftest.payload,
        '404 NOT FOUND', 'POST'),
    # All params
    (URL,
        '/endpoint/msteams',
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (URL,
        '/endpoint/msteams',
        conftest.payloadvROps60,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (URL,
        '/endpoint/msteams',
        conftest.payloadvROps62,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (URL,
        '/endpoint/msteams',
        conftest.payloadLI_test,
        '500 INTERNAL SERVER ERROR', 'POST'),
    (URL,
        '/endpoint/msteams/' + NUMRESULTS,
        conftest.payload,
        '500 INTERNAL SERVER ERROR', 'POST'),
])
def test_msteams(url, post, data, expected, method):
    if url is not None:
        loginsightwebhookdemo.msteams.TEAMSURL = url
    if method == 'PUT':
        rsp = conftest.client.put(post, data=data, content_type="application/json")
    else:
        rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected
