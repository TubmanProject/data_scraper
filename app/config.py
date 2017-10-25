import os

class DefaultConfig(object):
    #################################
    # Built-in configuration values #
    #################################
    DEBUG = False
    TESTING = False
    # PROPAGATE_EXECEPTIONS = ''
    # PRESERVE_CONTEXT_ON_EXCEPTION = ''
    # SECRET_KEY = ''
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
    # SERVER_NAME = ''
    # APPLICATION_ROOT = ''
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
    
    ############################
    # SQLAlchemy Configuration #
    ############################    
    # SQLALCHEMY_DATABASE_URI = #'mysql://user:pass@host/db_name'
    # SQLALCHEMY_BINDS = ''
    # SQLALCHEMY_ECHO = <bool>
    # SQLALCHEMY_RECORD_QUERIES = <bool>
    # SQLALCHEMY_NATIVE_UNICODE = <bool>
    # SQLALCHEMY_POOL_SIZE = 5
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # SQLALCHEMY_POOL_RECYCLE = 2 * 60 * 60
    # SQLALCHEMY_MAX_OVERFLOW = 10
    # SQLALCHEMY_TRACK_MODIFICATIONS = <bool>
    
    ########################
    # Sentry Configuration #
    ########################
    #SENTRY_DSN = ''
    
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
    # UPLOADS_DEFAULT_DEST = '/var/uploads'
    # UPLOADS_DEFAULT_URL = 'http://%s/assets'%(SERVER_NAME)
    
    #########################
    # Logging Configuration #
    #########################
    # LOG_FOLDER = ''
    # LOG_FILE = "hcdc_criminal_scraper.log"
    
    ###################
    # AWS credentials #
    ###################
    # AWS_ACCESS_KEY_ID = ''
    # AWS_SECRET_ACCESS_KEY = ''
    # AWS_DEFAULT_REGION = ''
    
    #######################
    # Other Configuration #
    #######################
    # default app name to use when no app_name is passed to create_app()
    APP_NAME = 'hcdc_criminal_scraper'
    
    # domain name
    DOMAIN_NAME = ''
    
    # project paths
    FLASK_PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    FLASK_STATIC_PATH = os.path.join(FLASK_PROJECT_ROOT, 'static')
    
    # hcdc data
    HCDC_DATA_PATH = os.path.join(FLASK_PROJECT_ROOT, 'data')
    
    # temporary hcdc data download path
    HCDC_CRIMINAL_DISPOSITION_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_disposition')
    HCDC_CRIMINAL_FILING_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_filing')
    
    # array of admin email addresses for logging emails
    # ADMINS = []

class ProductionConfig(DefaultConfig):
    pass

class StagingConfig(DefaultConfig):
    pass

class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = True
    EXPLAIN_TEMPLATE_LOADING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DefaultConfig.HCDC_DATA_PATH, 'sqlite', 'development.db')
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_RECORD_QUERIES = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig(DefaultConfig):
    pass

def get_config(MODE=None):
    """
    Return the configuration mode based on the APPLICATION_MODE env variable 
    """
    return {
        'DEVELOPMENT' : DevelopmentConfig,
        'STAGING' : StagingConfig,
        'PRODUCTION' : ProductionConfig,
        'TESTING' : TestConfig
    }.get(MODE, DevelopmentConfig)
