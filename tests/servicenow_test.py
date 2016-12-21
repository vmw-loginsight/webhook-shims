#!/usr/bin/env python


import json
import pytest

import loginsightwebhookdemo.servicenow

import conftest


# IMPORTANT: The service now account leveraged below
# hibernates after 6 hours of inactivity and is reclaimed
# if not used at least once every 10 days. A new URL can
# be generated as needed using the provided credentials.
# More information here: https://community.servicenow.com/community/develop/blog/2016/05/26/hibernation-and-developer-instances
#
# You can tell that hibernation/reclaimation has happened
# when the third test fails with '200 OK'.
#
# Given this, tox is configured to ignore testing SNOW.
# Please run pytest manually whenever changing the SNOW shim.
URL = 'https://dev18597.service-now.com'
USER = 'admin'
PASSWORD = 'L0g1ns1ght!'

BADPASSWORD = 'changeme'


@pytest.mark.parametrize("url,user,password,post,data,expected", [
    (None, None, None, '/endpoint/servicenow', conftest.payload, '500 INTERNAL SERVER ERROR'),
    (None, None, None, '/endpoint/servicenow/', conftest.payload, '404 NOT FOUND'),
    (URL, USER, BADPASSWORD, '/endpoint/servicenow', conftest.payload, '401 UNAUTHORIZED'),
    (URL, USER, PASSWORD, '/endpoint/servicenow', conftest.payload, '201 CREATED'),
    (URL, USER, PASSWORD, '/endpoint/servicenow', conftest.payloadvROps60, '201 CREATED'),
    (URL, USER, PASSWORD, '/endpoint/servicenow', conftest.payloadLI_test, '200 OK'),
])
def test_servicenow(url, user, password, post, data, expected):
    if url is not None:
        loginsightwebhookdemo.servicenow.SERVICENOWURL = url
    if user is not None:
        loginsightwebhookdemo.servicenow.SERVICENOWUSER = user
    if password is not None:
        loginsightwebhookdemo.servicenow.SERVICENOWPASS = password
    rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected


def test_servicenow_e2e():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    url = URL + '/incident.do?JSONv2&sysparm_query=active=true^short_description=Hello World'
    sys_id = json.loads(loginsightwebhookdemo.callapi(url, 'get', None, headers, (USER, PASSWORD)))['records'][0]['sys_id']
    url = URL + '/incident.do?JSONv2&sysparm_query=active=true^short_description=<None>'
    sys_id2 = json.loads(loginsightwebhookdemo.callapi(url, 'get', None, headers, (USER, PASSWORD)))['records'][0]['sys_id']
    ids = [sys_id, sys_id2]

    url = URL + '/sys_journal_field.do?JSONv2&sysparm_query=element_id=' + sys_id
    records = json.loads(loginsightwebhookdemo.callapi(url, 'get', None, headers, (USER, PASSWORD)))
    assert 'You can view this alert by clicking' in json.dumps(records)
    assert 'hello world 1' in json.dumps(records)

    payload = {"incident_state": "7"}
    for incident_id in ids:
        url = URL + '/api/now/table/incident/' + incident_id
        loginsightwebhookdemo.callapi(url, 'put', json.dumps(payload), headers, (USER, PASSWORD))
    url = URL + '/incident.do?JSONv2&sysparm_query=sys_id=' + sys_id
    result = json.loads(loginsightwebhookdemo.callapi(url, 'get', None, headers, (USER, PASSWORD)))['records'][0]['active']
    assert result == 'false'
