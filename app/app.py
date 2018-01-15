"""App Module."""

import click
import os
import redis

from flask import Flask
from logging import Formatter
from logging import FileHandler
from werkzeug.exceptions import (NotFound,
                                 BadRequest,
                                 Unauthorized,
                                 Forbidden,
                                 BadGateway,
                                 MethodNotAllowed)

from app import config as Config
from app.api import (dispositions,
                     filings,
                     fields)
from app.scraper.models.us.ustx.tasks import (scrape_hcdc_disposition_today_task,
                                              scrape_hcdc_filing_today_task,
                                              scrape_hcdc_disposition_by_date_task,
                                              scrape_hcdc_filing_by_date_task)
from app.scraper.models.us.ustx.constants import HCDC_DATA_PATH
from app.scraper.models.us.ustx.fields import initialize_fields as init_hcdc_fields
from .dispositions import Dispositions
from .extensions import pymongo_client
from .filings import Filings
from .frontend import frontend
from .response import Response

# only import the create_app() function when from app import * is called
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    frontend,
    dispositions,
    filings,
    fields
]


def create_app(config=None, app_name=None, blueprints=None):
    """Application factory to create the Flask app.

    Instantiate and configure the Flask application object.
    """
    if app_name is None:
        # load the default app_name from the config file
        app_name = config.APP_NAME
    if blueprints is None:
        # load blueprints from the list of blueprints defined in this module
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name,
                template_folder=config.TEMPLATE_FOLDER)
    app.url_map.strict_slashes = False

    # configure the app
    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app, blueprints)
    configure_hooks(app)
    configure_commands(app)
    configure_logging(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    """Configure the application with differentiation between dev, staging, and production."""
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
    """Initialize Flask extension libaries.

    Extensions extend the functionality of Flask
    """
    #######################
    # Notes on init_app() #
    #######################
    # init_app() is used to support the factory pattern for creating apps.
    # Some extensions require the app object but are instantiated in
    # extensions.py without the app object.
    # init_app() initializes the app (sets up configuration) for the extension

    ###########
    # MongoDB #
    ###########
    # configured in the 'app.extensions module'

    ##########
    # Celery #
    ##########
    # configured in 'app.extensions module' because Flask is not compatiable with lower-case config attributes

    ##############
    # Flask-Mail #
    ##############
    # Delaying initialization of the Mail instance until configuration time
    # requires the use of Flask's "current_app" context global to access the app's
    # configuration values
    # mail.init_app(app)

    #########
    # Redis #
    #########
    app.redis = redis.StrictRedis(host=app.config['REDIS_HOST'],
                                  port=app.config['REDIS_PORT'],
                                  password=app.config['REDIS_PASSWORD'])


def configure_blueprints(app, blueprints):
    """Register a collection of blueprints.

    A blueprint is a set of operations that can be registered on an application
    Blueprints are defined in each package's __init__.py
    """
    # Register a blueprint on an application at a URL prefix and/or subdomain
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_hooks(app):
    """Configure hooks."""
    pass


def configure_commands(app):
    """Configure commands."""
    @app.cli.command('initdb')
    def init_db_command():
        """Initialize the database command."""
        pymongo_client.drop_database(app.config['MONGO_DBNAME'])
        init_hcdc_fields(HCDC_DATA_PATH)
        Dispositions.setup_schema()
        Filings.setup_schema()
        Dispositions.create_denormalized_view()
        Filings.create_denormalized_view()
        click.echo('Initialized the database.')

    @app.cli.command('scrape')
    @click.option('--type',
                  help='Type of report to scrape. "disposition" or "filing"',
                  type=click.Choice(['disposition', 'filing']))
    @click.option('--date',
                  help='Date of the report to scrape.',
                  default='today')
    def scrape_report(type=None, date='today'):
        """Scrape a report."""
        if type:
            if date == 'today':
                if type == 'disposition':
                    res = scrape_hcdc_disposition_today_task()
                    click.echo(res)

                if type == 'filing':
                    res = scrape_hcdc_filing_today_task()
                    click.echo(res)
            else:
                if type == 'disposition':
                    res = scrape_hcdc_disposition_by_date_task(date)
                    click.echo(res)

                if type == 'filing':
                    res = scrape_hcdc_filing_by_date_task(date)
                    click.echo(res)
        else:
            if date == 'today':
                res = scrape_hcdc_disposition_today_task()
                click.echo(res)
                res = scrape_hcdc_filing_today_task()
                click.echo(res)
            else:
                res = scrape_hcdc_disposition_by_date_task(date)
                click.echo(res)
                res = scrape_hcdc_filing_by_date_task(date)
                click.echo(res)


def configure_logging(app):
    """Configure logging of data."""
    # When running locally use STDOUT for logging
    if app.debug or app.testing:
        print('App running locally.')
        print('Logging configured to use STDOUT for logging.')
        return

    # set log level
    app.logger.setLevel(app.config['LOG_LEVEL'])

    #############################
    # Error logging with Sentry #
    #############################

    ###########################
    # Configure error e-mails #
    ###########################

    ###################################
    # Configure error logging to file #
    ###################################
    file_handler = FileHandler(filename=os.path.join(app.config['LOG_FOLDER'],
                               app.config['LOG_FILE']),
                               mode='a',
                               encoding=None,
                               delay=False)

    # set formatting of the log file
    # format string makes use of knowledge of the LogRecord attributes
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    # log warning level
    file_handler.setLevel(app.config['LOG_LEVEL'])

    # add the error handler to the Flask application object
    app.logger.addHandler(file_handler)
    # Start logger
    app.logger.info('Logging configuration complete.')


def configure_error_handlers(app):
    """Configure the registration of error handlers for exceptions."""
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

    # Raise if the requested method is not allowed.
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        return Response.make_error_resp(error.description, code=error.code)
