FROM python:2
ADD webhook-shims /
RUN pip install -r ./requirements.txt
CMD ["python", "./runserver.py"]
