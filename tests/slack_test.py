#!/usr/bin/env python


import json

import loginsightwebhookdemo
import loginsightwebhookdemo.slack


client = loginsightwebhookdemo.app.test_client()

# Cannot add AlertName as must be unique for testing
payload = json.dumps({
    "AlertType": 2,
    "AlertName": "Hello World",
    "SearchPeriod": 300000,
    "HitCount": 2.0,
    "HitOperator": 2,
    "messages": [
        {
            "fields": [{
                "name": "Field_1",
                "content": "Content 1"
            }, {
                "name": "Field_2",
                "content": "Content 2"
            }]
        }, {
            "fields": [{
                "name": "Field_1",
                "content": "Content 1_2"
            }, {
                "name": "Field_2",
                "content": "Content 2_2"
            }]
        }
    ],
    "HasMoreResults": False,
    "Url": "https://10.11.12.13/s/8pgzq6",
    "EditUrl": "https://10.11.12.13/s/56monr",
    "Info": "This is an alert for all the Hello World messages",
    "NumHits": 2
})

payloadvROps62 = json.dumps({
    "startDate": 1369757346267,
    "criticality": "ALERT_CRITICALITY_LEVEL_WARNING",
    "Risk": 4.0,
    "resourceId": "sample-object-uuid",
    "alertId": "sample-alert-uuid",
    "status": "ACTIVE",
    "subType": "ALERT_SUBTYPE_AVAILABILITY_PROBLEM",
    "cancelDate": 1369757346267,
    "resourceKind": "sample-object-type",
    "alertName": "Invalid IP Address for connected Leaf Switch",
    "attributeKeyID": 5325,
    "Efficiency": 1.0,
    "adapterKind": "sample-adapter-type",
    "Health": 1.0,
    "type": "ALERT_TYPE_APPLICATION_PROBLEM",
    "resourceName": "sample-object-name",
    "updateDate": 1369757346267,
    "info": "sample-info"
})

payloadvROps60 = json.dumps({
    "startDate": 1369757346267,
    "criticality": "ALERT_CRITICALITY_LEVEL_WARNING",
    "resourceId": "sample-object-uuid",
    "alertId": "sample-alert-uuid",
    "status": "ACTIVE",
    "subType": "ALERT_SUBTYPE_AVAILABILITY_PROBLEM",
    "cancelDate": 1369757346267,
    "resourceKind": "sample-object-type",
    "attributeKeyID": 5325,
    "adapterKind": "sample-adapter-type",
    "type": "ALERT_TYPE_APPLICATION_PROBLEM",
    "resourceName": "sample-object-name",
    "updateDate": 1369757346267,
    "info": "sample-info"
})

payloadLI_test = json.dumps({
    "AlertType": 1,
    "AlertName": "Hello World",
    "SearchPeriod": 300000,
    "HitCount": 0.0,
    "HitOperator": 2,
    "messages": [],
    "HasMoreResults": False,
    "Url": None,
    "EditUrl": None,
    "Info": "hello world 1",
    "Recommendation": None,
    "NumHits": 0
})

NUMRESULTS = '1'
T = 'T3BCFGGDU'
B = 'B3BL90K4N'
X = 'Q8BojtVn1Pvjg510aCEOKNrd'


def test_slack_nourl():
    rsp = client.post('/endpoint/slack', data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/slack/', data=payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/slack/' + NUMRESULTS, data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/slack/' + T, data=payload, content_type="application/json")
    assert rsp.status == '405 METHOD NOT ALLOWED'
    rsp = client.post('/endpoint/slack/' + T + '/' + B, data=payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/slack/' + T + '/' + B + '/' + X, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


def test_slack_nox():
    loginsightwebhookdemo.slack.SLACKURL = 'https://hooks.slack.com/services/' + T + '/' + B + '/' + X

    rsp = client.post('/endpoint/slack', data=payload, content_type="application/json")
    assert rsp.status == '200 OK'
    rsp = client.post('/endpoint/slack', data=payloadvROps60, content_type="application/json")
    assert rsp.status == '200 OK'
    rsp = client.post('/endpoint/slack', data=payloadLI_test, content_type="application/json")
    assert rsp.status == '200 OK'
    rsp = client.post('/endpoint/slack/' + NUMRESULTS, data=payload, content_type="application/json")
    assert rsp.status == '200 OK'


def test_slack_wrongurl():
    loginsightwebhookdemo.slack.SLACKURL = 'https://vmw-loginsight.slack.com'

    rsp = client.post('/endpoint/slack', data=payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'

    loginsightwebhookdemo.slack.SLACKURL = 'https://hooks.slack.com/services/a/b/c'

    rsp = client.post('/endpoint/slack', data=payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
