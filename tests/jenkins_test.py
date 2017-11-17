#!/usr/bin/env python


import loginsightwebhookdemo
import loginsightwebhookdemo.jenkins

import conftest


client = loginsightwebhookdemo.app.test_client()

NUMRESULTS = '1'
T = 'T3BCFGGDU'
B = 'B3BL90K4N'
X = 'Q8BojtVn1Pvjg510aCEOKNrd'

# Parameters
JENKINSURL = ''
# Only required if not passed
JOBNAME = 'job1'
TOKEN = 'abc123'


def test_jenkins_nourl():
    rsp = client.post('/endpoint/jenkins', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/jenkins/', data=conftest.payload, content_type="application/json")
    assert rsp.status == '404 NOT FOUND'
    rsp = client.post('/endpoint/jenkins/' + JOBNAME, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/jenkins/' + JOBNAME + '/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'


def test_jenkins_allparams():
    loginsightwebhookdemo.jenkins.JENKINSURL = 'https://jenkins.vmwloginsight.com'
    loginsightwebhookdemo.jenkins.JOBNAME = 'job2'
    loginsightwebhookdemo.jenkins.TOKEN = 'def456'

    rsp = client.post('/endpoint/jenkins', data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
    rsp = client.post('/endpoint/jenkins/' + JOBNAME + '/' + TOKEN, data=conftest.payload, content_type="application/json")
    assert rsp.status == '500 INTERNAL SERVER ERROR'
