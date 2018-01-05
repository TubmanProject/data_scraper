"""Configuration for app."""

import os
import json
import logging

from configparser import ConfigParser

aws_config = ConfigParser()
aws_config.read(os.getenv('AWS_SHARED_CREDENTIALS_FILE'))

server_name = "{}.{}".format(os.getenv('SUBDOMAIN'), os.getenv('DOMAIN'))

# read the configuration files
with open(os.path.join(os.getenv('APP_SECRETS_PATH'), server_name, 'secrets.json'), 'r') as api_config:
    api_settings = json.load(api_config)

with open(os.path.join(os.getenv('MONGODB_SECRETS_PATH'), 'secrets.json'), 'r') as mongodb_config:
    mongodb_settings = json.load(mongodb_config)

with open(os.path.join(os.getenv('RABBITMQ_SECRETS_PATH'), 'secrets.json'), 'r') as rabbitmq_config:
    rabbitmq_settings = json.load(rabbitmq_config)

with open(os.path.join(os.getenv('REDIS_SECRETS_PATH'), 'secrets.json'), 'r') as redis_config:
    redis_settings = json.load(redis_config)

with open(os.path.join(os.getenv('REDIS_HAPROXY_SECRETS_PATH'), 'secrets.json'), 'r') as redis_haproxy_config:
    redis_haproxy = json.load(redis_haproxy_config)

with open(os.path.join(os.getenv('RABBITMQ_HAPROXY_SECRETS_PATH'), 'secrets.json'), 'r') as rabbitmq_haproxy_config:
    rabbitmq_haproxy = json.load(rabbitmq_haproxy_config)


class DefaultConfig(object):
    """Default configuration."""

    #################################
    # Built-in configuration values #
    #################################
    DEBUG = False
    TESTING = False
    # PROPAGATE_EXECEPTIONS = ''
    # PRESERVE_CONTEXT_ON_EXCEPTION = ''
    SECRET_KEY = api_settings['SECRET_KEY']
    SESSION_COOKIE_NAME = 'session'
    # SESSION_COOKIE_DOMAIN = ''
    # SESSION_COOKIE_PATH = ''
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    # PERMANENT_SESSION_LIFETIME = ''
    # SESSION_REFRESH_EACH_REQUEST = True
    # USE_X_SENDFILE = ''
    # LOGGER_NAME = ''
    # LOGGER_HANDLER_POLICY = 'always'
    SERVER_NAME = api_settings['SERVER_NAME']
    # APPLICATION_ROOT = os.path.abspath(os.path.dirname(__file__))
    # MAX_CONTENT_LENGTH = ''
    # SEND_FILE_MAX_AGE_DEFAULT = 43200
    # TRAP_HTTP_EXCEPTIONS = ''
    # TRAP_BAD_REQUEST_ERRORS = ''
    # PREFERRED_URL_SCHEME = 'http'
    # JSON_AS_ASCII = ''
    # JSON_SORT_KEYS = ''
    # JSONIFY_PRETTYPRINT_REGULAR = True
    # JSONIFY_MIMETYPE = ''
    # TEMPLATES_AUTO_RELOAD = None
    # EXPLAIN_TEMPLATE_LOADING = False

    ########################
    # Sentry Configuration #
    ########################
    # SENTRY_DSN = ''

    #########################
    # MongoDB Configuration #
    #########################
    MONGO_HOST = mongodb_settings['HOST'] or 'localhost'
    MONGO_PORT = mongodb_settings['PORT'] or 27017
    MONGO_PEM_KEYFILE = mongodb_settings['PEMKeyFile']
    MONGO_USER = [i for i in mongodb_settings['USERS'] if i['username'] == api_settings['HOSTNAME']][0]
    MONGO_USERNAME = MONGO_USER['username']
    MONGO_PASSWORD = MONGO_USER['password']
    MONGO_DBNAME = MONGO_USER['database']
    MONGO_ROLES = MONGO_USER['roles']

    #######################
    # Redis Configuration #
    #######################
    REDIS_HOST = redis_settings['MASTER']['HOST']
    REDIS_PORT = redis_settings['MASTER']['PORT']
    # REDIS_DB = 0
    REDIS_CELERY_DB = 1
    REDIS_PASSWORD = redis_settings['MASTER']['PASSWORD']
    # REDIS_SOCKET_TIMEOUT = None
    # REDIS_SOCKET_CONNECT_TIMEOUT = None
    # REDIS_SOCKET_KEEPALIVE = None
    # REDIS_SOCKET_KEEPALIVE_OPTIONS = None
    # REDIS_CONNECTION_POOL = None
    # REDIS_UNIX_SOCKET_PATH = None
    # REDIS_ENCODING = 'utf-8'
    # REDIS_ENCODING_ERRORS = 'strict'
    # REDIS_CHARSET = None
    # REDIS_ERRORS = None
    # REDIS_DECODE_RESPONSES = False
    # REDIS_RETRY_ON_TIMEOUT = False
    # REDIS_SSL = False
    # REDIS_SSL_KEYFILE = redis_settings['SSL']['KEYFILE']
    # REDIS_SSL_CERTFILE = redis_settings['SSL']['CERTFILE']
    # REDIS_SSL_CERT_REQS = None
    # REDIS_SSL_CA_CERTS = None
    # REDIS_MAX_CONNECTIONS = None

    ##########################
    # RabbitMQ Configuration #
    ##########################
    RABBITMQ_USERNAME = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    RABBITMQ_HOST = 'localhost'
    RABBITMQ_PORT = rabbitmq_haproxy['RABBITMQ_HAPROXY']['PORT']  # port 5772 if using haproxy
    RABBITMQ_VHOST = api_settings['HOSTNAME']
    RABBITMQ_BROKER_URLS = rabbitmq_settings[RABBITMQ_VHOST]['broker_urls']

    ########################
    # Celery Configuration #
    ########################
    # accept_content = ['json']
    # enable_utc = True
    # timezone = 'UTC'
    # task_annotations = None
    # task_compression = None
    # task_protocol = 2
    # task_serializer = 'json'
    # task_publish_retry = True
    # task_publish_retry_policy
    # task_always_eager = False
    # task_eager_propagates = False
    # task_ignore_result = False
    # task_store_errors_even_if_ignored = False
    # task_track_started = False
    # task_time_limit = 0
    # task_soft_time_limit = 0
    # task_acks_late = False
    # task_reject_on_worker_lost = False
    # task_default_rate_limit = 0
    # result_backend = 'file:///var/celery/results'
    # redis_max_connections = 0
    # redis_socket_connection_timeout = None
    # redis_socket_timeout = 5.0
    # result_serializer = 'json'
    # result_compression = None
    # result_expires = 24 * 60 * 60
    # result_cache_max = -1
    # task_queues = None
    # task_routes = None
    # task_queue_ha_policy = None
    # task_queue_max_priority = None
    # worker_direct = False
    # task_create_missing_queues = True
    # task_default_queue = 'celery'
    # task_default_exchange = 'celery'
    # task_default_exchange_type = 'direct'
    # task_default_routing_key = 'celery'
    # task_default_delivery_mode = 'persistent'
    # broker_url = 'amqp://'
    # broker_read_url = 'amqp://'
    # broker_write_url = 'amqp://'
    # broker_failover_strategy = 'round-robin'
    # broker_heartbeat = 120.0
    # broker_heartbeat_checkrate = 2.0
    # broker_use_ssl = False
    # broker_pool_limit = 10
    # broker_connection_timeout = 4.0
    # broker_connection_retry = True
    # broker_connection_max_retries = 100
    # broker_login_method = 'AMQPLAIN'
    # broker_transport_options = {}
    # imports = []
    # include = []
    # worker_concurrency = 2
    # worker_prefetch_multiplier = 4
    # worker_lost_wait = 10.0
    # worker_max_tasks_per_child = 0
    # worker_max_memory_per_child = 0
    # worker_disabled_rate_limits = False
    # worker_state_db = None
    # worker_timer_precision = 1.0
    # worker_enabled_remote_control = True
    # worker_send_task_events = False
    # task_send_sent_event = False
    # event_queue_ttl = 5.0
    # event_queue_expires = 60.0
    # event_queue_prefix = 'celeryev'
    # event_serializer = 'json'
    # control_queue_ttl = 300.0
    # control_queue_expires = 10.0
    # worker_hijack_root_logger = True
    # worker_log_color = ''
    # worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
    # worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s"
    # worker_redirect_stdouts = True
    # worker_redirect_stdouts_level = 'WARNING'
    # security_key = None
    # security_certificate = None
    # security_cert_store = None
    # worker_pool = 'prefork'
    # worker_pool_restarts = False
    # worker_autoscaler = "celery.worker.autoscale:Autoscaler"
    # worker_consumer = "celery.worker.consumer:Consumer"
    # worker_timer = "kombu.async.hub.timer:Timer"
    # beat_schedule - {}
    # beat_scheduler = "celery.beat:PersistentScheduler"
    # beat_schedule_filename = "celerybeat-schedule"
    # beat_sync_every = 0
    # beat_max_loop_interval = 0

    ############################
    # Flask-Mail Configuration #
    ############################
    # MAIL_SERVER = 'localhost'
    # MAIL_PORT = 25
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_DEBUG = DEBUG
    # MAIL_USERNAME = None
    # MAIL_PASSWORD = None
    # MAIL_DEFAULT_SENDER = 'admin@example.com'
    # MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = TESTING
    # MAIL_ASCII_ATTACHMENTS = False

    ###############################
    # Flask-Uploads Configuration #
    ###############################
    # UPLOADED_FILES_DEST = ''
    # UPLOADED_FILES_URL = ''
    # UPLOADED_FILES_ALLOW = ''
    # UPLOADED_FILES_DENY = ''
    UPLOADS_DEFAULT_DEST = '/var/uploads'
    UPLOADS_DEFAULT_URL = 'http://{}/assets'.format(SERVER_NAME)

    #########################
    # Logging Configuration #
    #########################
    LOG_FOLDER = os.path.join('/var/log/', api_settings['SERVER_NAME'])
    LOG_FILE = 'tubmanproject_api.log'
    LOG_LEVEL = logging.WARNING

    ###################
    # AWS credentials #
    ###################
    AWS_ACCESS_KEY_ID = aws_config.get('default', 'aws_access_key_id')
    AWS_SECRET_ACCESS_KEY = aws_config.get('default', 'aws_secret_access_key')
    AWS_DEFAULT_REGION = aws_config.get('default', 'region')

    #######################
    # Other Configuration #
    #######################
    # default app name to use when no app_name is passed to create_app()
    APP_NAME = 'tubmanproject_api'

    # domain name
    DOMAIN_NAME = api_settings['DOMAIN_NAME']

    # project paths
    FLASK_PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    FLASK_STATIC_PATH = os.path.join(FLASK_PROJECT_ROOT, 'static')
    TEMPLATE_FOLDER = os.path.join(FLASK_PROJECT_ROOT, 'templates')
    STATIC_FOLDER = os.path.join(FLASK_PROJECT_ROOT, 'static')

    # hcdc data
    HCDC_DATA_PATH = os.path.join(FLASK_PROJECT_ROOT, 'data')

    # temporary hcdc data download path
    HCDC_CRIMINAL_DISPOSITION_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_disposition')
    HCDC_CRIMINAL_FILING_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_filing')

    # array of admin email addresses for logging emails
    # ADMINS = []

    # SSL/TLS certificates and keys
    SSL_CERTFILE = api_settings['SSL_CERTFILE']
    SSL_KEYFILE = api_settings['SSL_KEYFILE']

    @classmethod
    def __getitem__(cls, x):
        """Return the attribute."""
        return getattr(cls, x)


class ProductionConfig(DefaultConfig):
    """Production configuration."""

    LOG_LEVEL = logging.ERROR
    result_backend = 'redis://:{}@{}:{}/{}'.format(
        redis_settings['MASTER']['PASSWORD'],
        redis_settings['MASTER']['HOST'],
        redis_settings['MASTER']['PORT'],
        DefaultConfig.REDIS_CELERY_DB)
    task_queue_ha_policy = 'all'
    RABBITMQ_VHOST = DefaultConfig.RABBITMQ_VHOST  # '/app'
    RABBITMQ_USERNAME = rabbitmq_settings[RABBITMQ_VHOST]['username']
    RABBITMQ_PASSWORD = rabbitmq_settings[RABBITMQ_VHOST]['password']
    # haproxy is setup to handle rabbitmq cluster
    broker_url = 'amqp://{}:{}@{}:{}/{}'.format(
        RABBITMQ_USERNAME,
        RABBITMQ_PASSWORD,
        DefaultConfig.RABBITMQ_HOST,
        DefaultConfig.RABBITMQ_PORT,
        RABBITMQ_VHOST)


class StagingConfig(DefaultConfig):
    """Staging configuration."""

    pass


class DevelopmentConfig(DefaultConfig):
    """Development configuration."""

    LOG_LEVEL = logging.INFO
    DEBUG = True
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = True
    EXPLAIN_TEMPLATE_LOADING = True
    task_track_started = True
    result_backend = 'redis://:{}@{}:{}/{}'.format(
        redis_settings['MASTER']['PASSWORD'],
        redis_settings['MASTER']['HOST'],
        redis_settings['MASTER']['PORT'],
        DefaultConfig.REDIS_CELERY_DB)
    task_queue_ha_policy = 'all'
    RABBITMQ_VHOST = DefaultConfig.RABBITMQ_VHOST  # '/app'
    RABBITMQ_USERNAME = rabbitmq_settings[RABBITMQ_VHOST]['username']
    RABBITMQ_PASSWORD = rabbitmq_settings[RABBITMQ_VHOST]['password']
    # haproxy is setup to handle rabbitmq cluster
    broker_url = 'amqp://{}:{}@{}:{}/{}'.format(
        RABBITMQ_USERNAME,
        RABBITMQ_PASSWORD,
        DefaultConfig.RABBITMQ_HOST,
        DefaultConfig.RABBITMQ_PORT,
        RABBITMQ_VHOST)
    task_send_sent_event = True


class TestConfig(DefaultConfig):
    """Test configuration."""

    LOG_LEVEL = logging.INFO
    TESTING = True
    task_track_started = True
    result_backend = 'redis://:{}@{}:{}/{}'.format(
        redis_settings['MASTER']['PASSWORD'],
        redis_settings['MASTER']['HOST'],
        redis_settings['MASTER']['PORT'],
        DefaultConfig.REDIS_CELERY_DB)
    task_queue_ha_policy = 'all'
    RABBITMQ_VHOST = DefaultConfig.RABBITMQ_VHOST  # '/app'
    RABBITMQ_USERNAME = rabbitmq_settings[RABBITMQ_VHOST]['username']
    RABBITMQ_PASSWORD = rabbitmq_settings[RABBITMQ_VHOST]['password']
    # haproxy is setup to handle rabbitmq cluster
    broker_url = 'amqp://{}:{}@{}:{}/{}'.format(
        RABBITMQ_USERNAME,
        RABBITMQ_PASSWORD,
        DefaultConfig.RABBITMQ_HOST,
        DefaultConfig.RABBITMQ_PORT,
        RABBITMQ_VHOST)
    task_send_sent_event = True


def get_config(MODE=None):
    """Return the configuration mode based on the APPLICATION_MODE env variable."""
    return {
            'DEVELOPMENT': DevelopmentConfig,
            'STAGING': StagingConfig,
            'PRODUCTION': ProductionConfig,
            'TESTING': TestConfig
    }.get(MODE, DevelopmentConfig)
