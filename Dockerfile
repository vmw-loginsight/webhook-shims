FROM photon:latest
MAINTAINER John Dias "diasj@vmware.com"
ENV PATH /usr/bin:$PATH
RUN tdnf install wget -y \
  && wget https://bootstrap.pypa.io/get-pip.py \
  && python get-pip.py \
  && tdnf install git -y \
  && git clone https://github.com/vmw-loginsight/webhook-shims.git
WORKDIR /webhook-shims
RUN /usr/bin/pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["runserver.py"]
