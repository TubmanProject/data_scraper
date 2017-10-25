import os

from flask import Flask

from . import config as Config
from .api import scraper
from .constants import HCDC_CRIMINAL_DISPOSITION_PATH, HCDC_CRIMINAL_FILING_PATH, HCDC_DATA_PATH
from .extensions import db, mail
from .response import Response
from .hcdc_fields import CourtDivisionIndicator, InstrumentType, CaseDisposition, CaseStatus, DefendantStatus, CurrentOffenseLevelDegree, DocketCalendarName, CalendarReason, DefendantRace
from .dispositions import Dispositions

# only import the create_app() function when from app import * is called
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    scraper
]

def create_app(config=None, app_name=None, blueprints=None):
    """
    Application factory to create the Flask app.
    Instantiate and configure the Flask application object.
    """
    
    if app_name is None:
        # load the default app_name from the config file
        app_name = config.APP_NAME
    if blueprints is None:
        # load blueprints from the list of blueprints defined in this module
        blueprints = DEFAULT_BLUEPRINTS
    
    app = Flask(app_name)
    
    # configure the app
    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app, blueprints)
    configure_hooks(app)
    # configure_logging(app)
    configure_error_handlers(app)
    
    return app

def configure_app(app, config=None):
    """
    Configure the application with differentiation between dev, staging, and production
    """
    # load the default configuration from a module
    app.config.from_object(Config.DefaultConfig)
    
    # override the default config with the configuration passed at app creation
    if config:
        app.config.from_object(config)
        
    # override the config with the configuration set in file referenced by environment variable
    if 'APPNAME_CONFIG' in os.environ:
        app.config.from_envvar('APPNAME_CONFIG')
    
    # override the config when APPLICATION_MODE env var is set
    application_mode = os.getenv('APPLICATION_MODE', 'DEVELOPMENT')
    app.config.from_object(Config.get_config(application_mode)) 

def configure_extensions(app):
    """
    Initialize Flask extensions
    Extensions extend the functionality of Flask
    """
    #######################
    # Notes on init_app() #
    #######################
    # init_app() is used to support the factory pattern for creating apps.
    # Some extensions require the app object but are instantiated in 
    # extensions.py without the app object.
    # init_app() initializes the app (sets up configuration) for the extension
    
    ##############
    # SQLAlchemy #
    ##############
    # "db" object is created globally in extenstions.py in order to be imported into modules
    # database configuration is handled in configure_app()
    
    # "db" object is not bound to the app object without setting up an application context
    # for methods that are passed the app object, like db.create_all(bind='__all__', app=None) 
    # which would not have an app object the app_context() is required to bind the "db" object to the app
    # init_app() initialize an application for the use with this database setup
    db.init_app(app)
    
    # add a custom CLI command for initializing the database
    with app.app_context():
        def init_db():
            db.drop_all()
            db.create_all()
            CourtDivisionIndicator.seed_db(HCDC_DATA_PATH)
            InstrumentType.seed_db(HCDC_DATA_PATH)
            CaseDisposition.seed_db(HCDC_DATA_PATH)
            CaseStatus.seed_db(HCDC_DATA_PATH)
            DefendantStatus.seed_db(HCDC_DATA_PATH)
            CurrentOffenseLevelDegree.seed_db(HCDC_DATA_PATH)
            DocketCalendarName.seed_db(HCDC_DATA_PATH)
            CalendarReason.seed_db(HCDC_DATA_PATH)
            DefendantRace.seed_db(HCDC_DATA_PATH)
            #Dispositions.seed_db()
    
    @app.cli.command('initdb')
    def initdb_command():
        """Initializes the database"""
        init_db()
        print 'Initialized the database.'
    
    
    ##############
    # Flask-Mail #
    ##############
    # Delaying initialization of the Mail instance until configuration time
    # requires the use of Flask's "current_app" context global to access the app's
    # configuration values
    # mail.init_app(app)

def configure_blueprints(app, blueprints):
    """
    Register a collection of blueprints.
    A blueprint is a set of operations that can be registered on an application
    Blueprints are defined in each package's __init__.py
    """
    
    # Register a blueprint on an application at a URL prefix and/or subdomain
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def configure_hooks(app):
    pass

def configure_logging(app):
    """
    Configure logging of data
    """
    
    # When running locally use STDOUT for logging
    if app.debug or app.testing:
        return
    
    # import the python logging library
    import logging
    from logging import Formatter, getLogger
    
    #-- TODO: use getLogger() to iterate over each library with logging and attach handlers
    
    #############################
    # Error logging with Sentry #
    #############################
    
    ## TODO
    
    ###########################
    # Configure error e-mails #
    ###########################
    
    ## TODO
    
    ###################################
    # Configure error logging to file #
    ###################################
    from logging.handlers import FileHandler
    file_handler = FileHandler(filename=os.path.join(app.config['LOG_FOLDER'], app.config['LOG_FILE']), 
                               mode='a', 
                               encoding=None, 
                               delay=False)
    
    # set formatting of the log file
    # format string makes use of knowledge of the LogRecord attributes
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    
    # log warning and more severe messages to file
    file_handler.setLevel(logging.WARNING)
    
    # add the error handler to the Flask application object
    app.logger.addHandler(file_handler)
    
def configure_error_handlers(app):
    """
    Configure the registration of error handlers for exceptions
    """
    
    from werkzeug.exceptions import HTTPException, NotFound, BadRequest, Unauthorized, Forbidden, BadGateway
    
    # Raise if the browser sends something to the application the application or server cannot handle
    @app.errorhandler(BadGateway)
    def handle_bad_gateway(error):
        return Response.make_exception_resp(BadRequest, code=error.code)
    
    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return Response.make_error_resp(error.description, code=error.code)
        
    # Raise if a resource does not exist and never existed.
    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return Response.make_error_resp(error.description, code=error.code)
    
    # Raise if the user is not authorized. Also used if you want to use HTTP basic auth
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(error):
        return Response.make_error_resp(error.description, code=error.code)
        
    # Raise if the user doesn't have the permission for the requested resource but was authenticated.    
    @app.errorhandler(Forbidden)
    def handle_forbidden(error):
        return Response.make_error_resp(error.description, code=error.code)