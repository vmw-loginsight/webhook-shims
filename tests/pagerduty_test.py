#!/usr/bin/env python


import pytest

import loginsightwebhookdemo.pagerduty

import conftest


APIKEY = 'abc123'


@pytest.mark.parametrize("post,data,expected", [
    ('/endpoint/pagerduty/', conftest.payload, '404 NOT FOUND'),
    ('/endpoint/pagerduty/' + APIKEY, conftest.payload, '500 INTERNAL SERVER ERROR'),
])
def test_pgaerduty_nourl(post, data, expected):
    loginsightwebhookdemo.pagerduty.PAGERDUTYURL = ''

    rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected


@pytest.mark.parametrize("post,data,expected", [
    ('/endpoint/pagerduty/' + APIKEY, conftest.payload, '400 BAD REQUEST'),
    ('/endpoint/pagerduty/' + APIKEY, conftest.payloadvROps60, '400 BAD REQUEST'),
    ('/endpoint/pagerduty/' + APIKEY, conftest.payloadLI_test, '400 BAD REQUEST'),
])
def test_pgaerduty_allparams(post, data, expected):
    loginsightwebhookdemo.pagerduty.PAGERDUTYURL = 'https://events.pagerduty.com/generic/2010-04-15/create_event.json'

    rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected


# Will not work by default since PD does not offer a free account for testing API
# Change APIKEY2 to something valid if you want to test
# APIKEY2 = 'df5369ca51b241cfbe8aeb91d656b3e4'
# @pytest.mark.parametrize("post,data,expected", [
#     ('/endpoint/pagerduty/' + APIKEY2, conftest.payload, '200 OK'),
#     ('/endpoint/pagerduty/' + APIKEY2, conftest.payloadvROps60, '200 OK'),
#     ('/endpoint/pagerduty/' + APIKEY2, conftest.payloadLI_test, '200 OK'),
# ])
# def test_pgaerduty_allparams_real(post, data, expected):
#     loginsightwebhookdemo.pagerduty.PAGERDUTYURL = 'https://events.pagerduty.com/generic/2010-04-15/create_event.json'
#
#     rsp = conftest.client.post(post, data=data, content_type="application/json")
#     assert rsp.status == expected
