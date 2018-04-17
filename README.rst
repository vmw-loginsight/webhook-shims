.. image:: https://api.travis-ci.org/vmw-loginsight/webhook-shims.svg?branch=master
    :target: https://travis-ci.org/vmw-loginsight/webhook-shims
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/vmw-loginsight/webhook-shims/badge.svg?branch=master
    :target: https://coveralls.io/github/vmw-loginsight/webhook-shims?branch=master

Translation Shims for Log Insight and/or vRealize Operations Manager Webhooks
=============================================================================

Translate webhooks from Log Insight 3.3+ and vRealize Operations Manager
6.0+ (recommended 6.2+) to other services. Get alerts in your team
chatroom, open an incident ticket or kick off a remediation workflow.

Log Insight and vRealize Operations Manager send alert notifications as
HTTP POST with a JSON body. However, most third-party solutions expect
incoming webhooks to be in a proprietary format. If the receiving system
lacks native support for the webhook format, a shim between them can
translate the webhook format as needed. This repository provides several
example shims design to work with Python 2.7+.

Installation
------------

Three installation methods exist. Please select the one you are most comfortable with.

`Docker`_
~~~~~~

::

    docker run -it -p 5001:5001 vmware/webhook-shims

`Photon OS 1.0`_
~~~~~~~~~~~~

::

    tdnf install wget -y
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    pip install virtualenv
    tdnf install git -y
    virtualenv loginsightwebhookdemo
    cd loginsightwebhookdemo
    source bin/activate
    git clone https://github.com/vmw-loginsight/webhook-shims.git
    cd webhook-shims/
    pip install -r requirements.txt

`Photon OS 2.0`_
~~~~~~~~~~~~

::

    tdnf install wget python2 python-xml -y
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    pip install virtualenv
    tdnf install git -y
    virtualenv loginsightwebhookdemo
    cd loginsightwebhookdemo
    source bin/activate
    git clone https://github.com/vmw-loginsight/webhook-shims.git
    cd webhook-shims/
    pip install -r requirements.txt
    iptables -A INPUT -p tcp --dport 5001 -j ACCEPT

Manual
~~~~~~

::

    virtualenv loginsightwebhookdemo
    cd loginsightwebhookdemo
    source bin/activate
    git clone https://github.com/vmw-loginsight/webhook-shims.git
    cd webhook-shims/
    pip install -r requirements.txt

Modify and run the shim:

-  Some services require credentials or URLs. Edit individual services
   under ``loginsightwebhookdemo/`` to modify constants as needed.
   (Note: For basic auth, ~/.netrc will take prescendence.)
-  Run ``python runserver.py [port]`` - the Flask webserver starts and
   reports listening - default http://0.0.0.0:5001/
-  Open your browser pointed to the Flask webserver for a list of
   available URLs.

Documentation
-------------

Documentation for this shim can be found under the Installation section
above. Once the shim is running, documentation for all endpoint can be
found at the root path. With the shim running, you need to configure
sources to point to the shim. Configuration information for Log Insight
and vRealize Operations Manager are listed below.

Log Insight webhook configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two places in LI where webhooks can be configured:

1. `System notification: under the General page in the Administration
   section`_
2. `User alerts: while creating a new user alert or by editing an
   existing user alert`_

vRealize Operations Manager webhook configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`REST plugin: under Administration > Outbound Settings`_

Developing and Contributing
---------------------------

We’d love to get contributions from you! Once you are up and running,
take a look at the `Contribution Document`_ to see how to get your
changes merged in.

Licensing
---------

Provided under Apache License 2.0.
For more information, see the `LICENSE`_ file.

Support
-------

Please report problems via `GitHub issues`_.

.. _`Docker`: https://hub.docker.com/r/vmware/webhook-shims/
.. _`Photon OS`: https://vmware.github.io/photon/
.. _`System notification: under the General page in the Administration section`: http://pubs.vmware.com/log-insight-40/topic/com.vmware.log-insight.administration.doc/GUID-506AE354-3F68-43A6-8C28-70F6FA1D3D9F.html
.. _`User alerts: while creating a new user alert or by editing an existing user alert`: http://pubs.vmware.com/log-insight-40/topic/com.vmware.log-insight.user.doc/GUID-95177CE4-C79C-42E3-A095-450B0F93A5DA.html
.. _`REST plugin: under Administration > Outbound Settings`: http://pubs.vmware.com/vrealizeoperationsmanager-64/topic/com.vmware.vcom.core.doc/GUID-2A26A734-CD91-43E0-BF42-B079D5B0F5D4.html
.. _Contribution Document: https://github.com/vmw-loginsight/webhook-shims/blob/master/CONTRIBUTING.md
.. _LICENSE: https://github.com/vmw-loginsight/webhook-shims/blob/master/LICENSE
.. _`GitHub Issues`: https://github.com/vmw-loginsight/webhook-shims/issues
