"""Constants."""

import os
from app.constants import FLASK_PROJECT_ROOT

# hcdc data
HCDC_DATA_PATH = os.path.join(FLASK_PROJECT_ROOT, 'scraper', 'models', 'us', 'ustx', 'data')

# temporary hcdc data download path
HCDC_CRIMINAL_DISPOSITION_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_disposition')
HCDC_CRIMINAL_FILING_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_filing')
