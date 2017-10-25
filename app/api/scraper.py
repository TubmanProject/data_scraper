from flask import Blueprint
import os
import json
import datetime
import requests
import bs4

from ..response import Response
from ..constants import HCDC_CRIMINAL_DISPOSITION_PATH, HCDC_CRIMINAL_FILING_PATH, HCDC_DATA_PATH
from ..dispositions import Dispositions

scraper = Blueprint('scraper', __name__, url_prefix='/api/scraper')

@scraper.route('/disposition/today', methods=['POST'])
def scrape_disposition_today():
    
    today = datetime.datetime.today()
    
    # download today's disposition report
    try:
        Dispositions.download_disposition_report_by_date(today)
    except Exception as err:
        if err.__class__.__name__ == 'HTTPError':
            return Response.make_error_resp(msg=err.response.reason, type=err.__class__.__name__, code=err.response.status_code)
        else:
            return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=500) 
    
    # TODO: fix this
    # wait for the file to be downloaded
    filename = '%s_criminal_disposition.txt'%(today.strftime('%Y-%m-%d'))
    file_path = os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)
    while not os.path.exists(file_path):
        time.sleep(1)
    
    # parse the downloaded disposition report
    try: 
       parsed = Dispositions.parse_disposition_data_by_date(today)
    except Exception as err:
        return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=500) 
    finally:
        if parsed:
            return Response.make_success_resp(msg="Disposition report for today has been saved to the database.")
        else: 
            return Response.make_error_resp(msg="Error: Unknown error parsing the disposition data file", type="Error", code=500)

@scraper.route('/disposition/seed_db', methods=['POST'])
def seed_disposition_db():
     """
     This endpoint doesn't work.
     The HCDC public dataset website doesn't seem to archive disposition data
     """
     try:
        num_found = Dispositions.seed_db()
     except Exception as err:
        if err.__class__.__name__ == 'HTTPError':
            return Response.make_error_resp(msg=err.response.reason, type=err.__class__.__name__, code=err.response.status_code)
        else:
            return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=500)
     finally:    
         if num_found:
            return Response.make_success_resp(msg="%s disposition reports have been added to the database."%(num_found))
         else: 
            return Response.make_error_resp(msg="Error: Unknown error seeding the disposition database.", type="Error", code=500) 