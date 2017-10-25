import os

FLASK_PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# hcdc data
HCDC_DATA_PATH = os.path.join(FLASK_PROJECT_ROOT, 'data')

# temporary hcdc data download path
HCDC_CRIMINAL_DISPOSITION_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_disposition')
HCDC_CRIMINAL_FILING_PATH = os.path.join(FLASK_PROJECT_ROOT, 'tmp/criminal_filing')