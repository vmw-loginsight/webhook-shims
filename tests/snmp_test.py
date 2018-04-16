import pytest
import conftest
import loginsightwebhookdemo.snmp

loginsightwebhookdemo.snmp.VROPSURL = None


@pytest.mark.parametrize("url,post,data,expected,method", [
    (None,
     '/endpoint/snmp',
     conftest.payloadvROps62,
     '200 OK', 'POST'),
    (None,
     '/endpoint/snmp',
     conftest.payloadLI_AQ,
     '200 OK', 'POST'),
    (None,
     '/endpoint/snmp',
     conftest.payloadLI_MQ,
     '200 OK', 'POST'),
    (None,
     '/endpoint/snmp',
     conftest.payloadLI_sys,
     '200 OK', 'POST'),
    (None,
     '/endpoint/snmp',
     conftest.payloadvROps60,
     '200 OK', 'POST')])
def test_snmp(url, post, data, expected, method):
    if url is not None:
        loginsightwebhookdemo.slack.SLACKURL = url
    if method == 'PUT':
        rsp = conftest.client.put(post, data=data, content_type="application/json")
    else:
        rsp = conftest.client.post(post, data=data, content_type="application/json")
    assert rsp.status == expected
