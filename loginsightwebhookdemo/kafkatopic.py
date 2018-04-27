#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging
from kafka import KafkaProducer
from kafka.common import KafkaTimeoutError


__author__ = "Pontus Rydin"
__license__ = "Apache v2"
__email__ = "li-cord@vmware.com"
__version__ = "1.0"

KAFKA_BOOSTRAP_SERVERS='192.168.1.13:9092'
KAFKA_USER=None
KAFKA_PASSWORD=None
KAFKA_SASL_MECHANISM=None # Change to 'SASL_PLAINTEXT' for basic plaintext authentication

PRODUCER = None

@app.route("/endpoint/kafka/<TOPIC>", methods=['POST'])

def kafka(TOPIC=None):
    # Lazy init of the Kafka producer
    #
    global PRODUCER
    if PRODUCER is None:
        PRODUCER = KafkaProducer(
            bootstrap_servers=KAFKA_BOOSTRAP_SERVERS,
            sasl_mechanism=KAFKA_SASL_MECHANISM,
            sasl_plain_username=KAFKA_USER,
            sasl_plain_password=KAFKA_PASSWORD)
    try:
        future = PRODUCER.send(TOPIC, request.get_data())
        future.get(timeout=60)
        return "OK", 200, None
    except KafkaTimeoutError:
        return "Internal Server Error", 500, None


