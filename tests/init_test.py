import requests

import loginsightwebhookdemo


client = loginsightwebhookdemo.app.test_client()
# client2 = loginsightwebhookdemo.app.test_client(5002)

payloadLI_MQ = {
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
}

payloadLI_AQ = {
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
}

payloadLI_test = {
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
}

payloadLI_sys = {
    "AlertName": "Hello World",
    "messages": [
        {
            "text": "hello world 1",
            "timestamp": 1451940578545,
            "fields": []
        }
    ],
}

payloadvROps60 = {
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
}

payloadvROps62 = {
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
}


def test_parse():
    try:
        loginsightwebhookdemo.parse({"abc": "123"})
    except AttributeError:
        assert True
    else:
        assert False


def test_parse_LI_MQ():
    alert = loginsightwebhookdemo.parseLI(payloadLI_MQ, {})
    assert alert['hookName'] == 'Log Insight'
    assert alert['color'] == 'red'
    assert alert['AlertName'] == 'Hello World'
    assert alert['info'] == 'This is an alert for all the Hello World messages'
    # assert alert['Messages'] == '[{"text": "hello world 1","timestamp": 1451940578545,"fields": [{"name": "Field_1","content": "Content 1"}, { "name": "Field_2","content": "Content 2"}]'
    assert alert['url'] == 'https://10.11.12.13/s/8pgzq6'
    assert alert['editurl'] == 'https://10.11.12.13/s/56monr'
    assert alert['HasMoreResults'] == 'False'
    assert alert['NumHits'] == '2'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2015/04/li-logo.png'
    assert alert['moreinfo'] == 'Hello World\n\nThis is an alert for all the Hello World messages\n\n\
You can view this alert by clicking: https://10.11.12.13/s/8pgzq6\n\
You can edit this alert by clicking: https://10.11.12.13/s/56monr'


def test_parse_vROps60_test():
    alert = loginsightwebhookdemo.parsevROps(payloadvROps60, {})
    assert alert['hookName'] == 'vRealize Operations Manager'
    assert alert['color'] == 'green'
    assert alert['AlertName'] == '<None>'
    assert alert['info'] == 'sample-info'
    assert alert['criticality'] == 'ALERT_CRITICALITY_LEVEL_WARNING'
    assert alert['status'] == 'INACTIVE'
    assert alert['type'] == 'ALERT_TYPE_APPLICATION_PROBLEM'
    assert alert['subType'] == 'ALERT_SUBTYPE_AVAILABILITY_PROBLEM'
    assert alert['Risk'] == ''
    assert alert['Efficiency'] == ''
    assert alert['Health'] == ''
    assert alert['resourceName'] == 'sample-object-name'
    assert alert['adapterKind'] == 'sample-adapter-type'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2016/09/vrops-256.png'
    assert alert['moreinfo'] == alert['AlertName'] + ("\n\n") + alert['info']


def test_parseLI_MQ():
    alert = loginsightwebhookdemo.parseLI(payloadLI_MQ, {})
    assert alert['hookName'] == 'Log Insight'
    assert alert['color'] == 'red'
    assert alert['AlertName'] == 'Hello World'
    assert alert['info'] == 'This is an alert for all the Hello World messages'
    # assert alert['Messages'] == '[{"text": "hello world 1","timestamp": 1451940578545,"fields": [{"name": "Field_1","content": "Content 1"}, { "name": "Field_2","content": "Content 2"}]'
    assert alert['url'] == 'https://10.11.12.13/s/8pgzq6'
    assert alert['editurl'] == 'https://10.11.12.13/s/56monr'
    assert alert['HasMoreResults'] == 'False'
    assert alert['NumHits'] == '2'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2015/04/li-logo.png'
    assert alert['moreinfo'] == 'Hello World\n\nThis is an alert for all the Hello World messages\n\n\
You can view this alert by clicking: https://10.11.12.13/s/8pgzq6\n\
You can edit this alert by clicking: https://10.11.12.13/s/56monr'


def test_parseLI_AQ():
    alert = loginsightwebhookdemo.parseLI(payloadLI_AQ, {})
    assert alert['hookName'] == 'Log Insight'
    assert alert['color'] == 'red'
    assert alert['AlertName'] == 'Hello World'
    assert alert['info'] == 'This is an alert for all the Hello World messages'
    # assert alert['Messages'] == '[{"text": "hello world 1","timestamp": 1451940578545,"fields": [{"name": "Field_1","content": "Content 1"}, { "name": "Field_2","content": "Content 2"}]'
    assert alert['url'] == 'https://10.11.12.13/s/8pgzq6'
    assert alert['editurl'] == 'https://10.11.12.13/s/56monr'
    assert alert['HasMoreResults'] == 'False'
    assert alert['NumHits'] == '2'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2015/04/li-logo.png'
    assert alert['moreinfo'] == 'Hello World\n\nThis is an alert for all the Hello World messages\n\n\
You can view this alert by clicking: https://10.11.12.13/s/8pgzq6\n\
You can edit this alert by clicking: https://10.11.12.13/s/56monr'


def test_parseLI_sys():
    alert = loginsightwebhookdemo.parseLI(payloadLI_sys, {})
    assert alert['hookName'] == 'Log Insight'
    assert alert['color'] == 'red'
    assert alert['AlertName'] == 'Hello World'
    assert alert['info'] == 'hello world 1'
    # assert alert['Messages'] == '[{"text": "hello world 1","timestamp": 1451940578545,"fields": [{"name": "Field_1","content": "Content 1"}, { "name": "Field_2","content": "Content 2"}]'
    assert alert['url'] == ''
    assert alert['editurl'] == ''
    assert alert['HasMoreResults'] == False
    assert alert['NumHits'] == False
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2015/04/li-logo.png'
    assert alert['moreinfo'] == 'Hello World\n\nhello world 1'


def test_parseLI_test():
    alert = loginsightwebhookdemo.parseLI(payloadLI_test, {})
    assert alert['hookName'] == 'Log Insight'
    assert alert['color'] == 'red'
    assert alert['AlertName'] == 'Hello World'
    assert alert['info'] == 'hello world 1'
    assert alert['Messages'] == []
    '{"text": "hello world 1","timestamp": 1451940578545,"fields": [{"name": "Field_1","content": "Content 1"}, { "name": "Field_2","content": "Content 2"}]'
    assert alert['url'] == ''
    assert alert['editurl'] == ''
    'https://10.11.12.13/s/56monr'
    assert alert['HasMoreResults'] == 'False'
    assert alert['NumHits'] == '0'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2015/04/li-logo.png'
    assert alert['moreinfo'] == 'Hello World\n\nhello world 1'


def test_parsevROps_LI():
    alert = loginsightwebhookdemo.parsevROps(payloadLI_sys, {})
    assert alert == {}


def test_parsevROps60_test():
    alert = loginsightwebhookdemo.parsevROps(payloadvROps60, {})
    assert alert['hookName'] == 'vRealize Operations Manager'
    assert alert['color'] == 'green'
    assert alert['AlertName'] == '<None>'
    assert alert['info'] == 'sample-info'
    assert alert['criticality'] == 'ALERT_CRITICALITY_LEVEL_WARNING'
    assert alert['status'] == 'INACTIVE'
    assert alert['type'] == 'ALERT_TYPE_APPLICATION_PROBLEM'
    assert alert['subType'] == 'ALERT_SUBTYPE_AVAILABILITY_PROBLEM'
    assert alert['Risk'] == ''
    assert alert['Efficiency'] == ''
    assert alert['Health'] == ''
    assert alert['resourceName'] == 'sample-object-name'
    assert alert['adapterKind'] == 'sample-adapter-type'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2016/09/vrops-256.png'
    assert alert['moreinfo'] == alert['AlertName'] + ("\n\n") + alert['info']


def test_parsevROps62_test():
    alert = loginsightwebhookdemo.parsevROps(payloadvROps62, {})
    assert alert['hookName'] == 'vRealize Operations Manager'
    assert alert['color'] == 'yellow'
    assert alert['AlertName'] == 'Invalid IP Address for connected Leaf Switch'
    assert alert['info'] == 'sample-info'
    assert alert['criticality'] == 'ALERT_CRITICALITY_LEVEL_WARNING'
    assert alert['status'] == 'ACTIVE'
    assert alert['type'] == 'ALERT_TYPE_APPLICATION_PROBLEM'
    assert alert['subType'] == 'ALERT_SUBTYPE_AVAILABILITY_PROBLEM'
    assert alert['Risk'] == 4.0
    assert alert['Efficiency'] == 1.0
    assert alert['Health'] == 1.0
    assert alert['resourceName'] == 'sample-object-name'
    assert alert['adapterKind'] == 'sample-adapter-type'
    assert alert['icon'] == 'http://blogs.vmware.com/management/files/2016/09/vrops-256.png'
    assert alert['moreinfo'] == alert['AlertName'] + ("\n\n") + alert['info']


def test_parseLI_vrops():
    assert loginsightwebhookdemo.parseLI('{}', 'Hello world') == 'Hello world'


def test_parseLI_other():
    if loginsightwebhookdemo.parseLI('{}', None) is None:
        pass


def test_callapi():
    try:
        loginsightwebhookdemo.callapi()
    except TypeError:
        assert True
    else:
        assert False
    try:
        loginsightwebhookdemo.callapi('abc123')
    except (requests.exceptions.MissingSchema):
        assert True
    else:
        assert False
    try:
        loginsightwebhookdemo.callapi('http://abc123')
    except (requests.exceptions.ConnectionError):
        assert True
    else:
        assert False
    assert 'google.j' in loginsightwebhookdemo.callapi('http://www.google.com', 'get')
    assert 'google.j' in loginsightwebhookdemo.callapi('http://www.google.com', 'get', None, {"Cache-control": "no-cache"}, ('user', 'pass'), False)
    if any('400' in code for code in loginsightwebhookdemo.callapi('http://www.google.com', 'get', 'test')):
        assert True
    else:
        assert False


def test_homepage():
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    # assert '<title>Todo</title>' in html
    assert '<p>\n<h1>Demo webhook shims for Log Insight and vRealize Operations Manager</h1>' in html


def test_unknown_url():
    rsp = client.get('/test')
    assert rsp.status == '404 NOT FOUND'


def test_wrong_method():
    rsp = client.get('/endpoint/test')
    assert rsp.status == '405 METHOD NOT ALLOWED'


def test_test():
    rsp = client.post('/endpoint/test')
    assert rsp.status == '200 OK'
    rsp = client.put('/endpoint/test/alertid')
    assert rsp.status == '200 OK'
