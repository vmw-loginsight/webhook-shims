FROM photon:latest
MAINTAINER John Dias "diasj@vmware.com"
RUN tdnf install python2 python-xml -y \
  && curl -s https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py \
  && /usr/bin/python /tmp/get-pip.py \
  && tdnf install git -y \
  && git clone https://github.com/vmw-loginsight/webhook-shims.git ~/webhook-shims
WORKDIR /root/webhook-shims
RUN /usr/bin/pip install -r requirements.txt
#ENTRYPOINT ["python"]
CMD ["/root/webhook-shims/runserver.py"]
