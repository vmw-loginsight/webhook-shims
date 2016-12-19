#!/usr/bin/env python


import json


payloadLI_MQ = json.dumps({
    "AlertType": 1,
    "AlertName": "Hello World",
    "SearchPeriod": 300000,
    "HitCount": 0.0,
    "HitOperator": 2,
    "messages": [
        {
            "text": "hello world 1",
            "timestamp": 1451940578545,
            "fields": [{
                "name": "Field_1",
                "content": "Content 1"
            }, {
                "name": "Field_2",
                "content": "Content 2"
            }]
        }, {
            "text": "hello world 2",
            "timestamp": 1451940561008,
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

payloadLI_AQ = json.dumps({
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
    "HasMoreResults": True,
    "Url": "https://10.11.12.13/s/8pgzq6",
    "EditUrl": "https://10.11.12.13/s/56monr",
    "Info": "This is an alert for all the Hello World messages",
    "NumHits": 2
})

payload = payloadLI_AQ

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

payloadLI_sys = json.dumps({
    "AlertName": "Hello World",
    "messages": [
        {
            "text": "hello world 1",
            "timestamp": 1451940578545,
            "fields": []
        }
    ],
})

payloadvROps60 = json.dumps({
    "startDate": 1369757346267,
    "criticality": "ALERT_CRITICALITY_LEVEL_WARNING",
    "resourceId": "sample-object-uuid",
    "alertId": "sample-alert-uuid",
    "status": "INACTIVE",
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
