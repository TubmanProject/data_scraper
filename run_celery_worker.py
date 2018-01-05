"""Run Celery Worker Module."""

import os

from app import create_app
from app.config import get_config
from app.extensions import celery

application_mode = os.getenv('APPLICATION_MODE', 'DEVELOPMENT')
Config = get_config(MODE=application_mode)

# an instance of the app is being created for use with celery
app = create_app(config=Config)

# no request is active but you need to reference the current_app for celery configuration
# therefore bind the application to the current context
with app.app_context():
    celery.start()
