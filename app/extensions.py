"""Extensions module - Set up external libraries."""

import os
import pika
import ssl

from app.config import get_config
from celery import Celery
from flask_mail import Mail
from pymongo import MongoClient

application_mode = os.getenv('APPLICATION_MODE', 'DEVELOPMENT')
Config = get_config(MODE=application_mode)
config = Config()

##############
# Flask-Mail #
##############
# email are managed through a Mail instance
mail = Mail()

###########
# PyMongo #
###########
# create a PyMongo client
# Flask-PyMongo doesn't support SSL/TLS therefore configure the client here
pymongo_client = MongoClient(
    config['MONGO_HOST'],
    port=config['MONGO_PORT'],
    username=config['MONGO_USERNAME'],
    password=config['MONGO_PASSWORD'],
    authSource=config['MONGO_DBNAME'],
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
    ssl_certfile=config['SSL_CERTFILE'],
    ssl_keyfile=config['SSL_KEYFILE'],
    connect=False)
db = pymongo_client[config['MONGO_DBNAME']]

##########
# celery #
##########
# celery instance is created as a global variable but configuration is halted until creation of the Flask app
celery = Celery(__name__,
                backend=config['result_backend'],
                broker=config['broker_url'])
celery.config_from_object(Config)
###################
# Pika (RabbitMQ) #
###################


class PikaConnection(object):
    """Class - Set up pika connection."""

    def __init__(self, rabbitmq_username, rabbitmq_password, rabbitmq_host, rabbitmq_port, rabbitmq_vhost):
        """Initialize the PikaConnection class."""
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_vhost = rabbitmq_vhost

    def blocking_connection(self):
        """Set up a pika blocking connection."""
        pika_credentials = pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        pika_connection_parameters = pika.ConnectionParameters(
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            virtual_host=self.rabbitmq_vhost,
            credentials=pika_credentials)

        return pika.BlockingConnection(parameters=pika_connection_parameters)
