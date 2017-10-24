from flask import Blueprint
import os
import json
import datetime
import requests
import bs4

from ..response import Response
from ..config import HCDC_CRIMINAL_DISPOSITION_PATH, HCDC_CRIMINAL_FILING_PATH, HCDC_DATA_PATH
from ..dispositions import Dispositions

scraper = Blueprint('scraper', __name__, url_prefix='/api/scraper')

@scraper.route('/disposition/today', methods=['POST'])
def scrape_disposition_today():
    
    today = datetime.datetime.today()
    
    # download today's disposition report
    try:
        download_disposition_report_by_date(today)
    except Exception as err:
        if err.__class__.__name__ == 'HTTPError':
            return Response.make_error_resp(msg=err.response.reason, type=err.__class__.__name__, code=err.response.status_code)
        else:
            return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=500) 
    
    # TODO: fix this
    # wait for the file to be downloaded
    filename = '%s_criminal_disposition.txt'%(today.strftime('%Y-%m-%d'))
    file_path = op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)
    while not os.path.exists(file_path):
        time.sleep(1)
    
    # parse the downloaded disposition report
    try: 
       parsed = parse_disposition_data_by_date(today)
    except Exception as err:
       return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=500) 
    
    if parsed:
        return Response.make_success_resp(msg="Disposition report for today has been saved to the database.")
    else: 
        return Response.make_error_resp(msg="Error: Unknown error parsing the disposition data file", type="Error", code=500)

# =============================================================================
def download_todays_disposition():
    """
    Download the daily disposition file from 
    http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx
    and save it to disk
    """
    
    # request the Harris County District Clerk public dataset page
    try:
        response = requests.get('http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx')
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise
        # return Response.make_error_resp(msg=err.args[0], type=err.__class__.__name__, code=response.status_code)
    except requests.exceptions.RequestException as err:
        raise
        # return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=response.status_code)  
    
    # create a BeautifulSoup object with the content of the response
    soup = bs4.BeautifulSoup(response.text)
    
    # capture the form (name and id attributes hardcoded, they were found by looking at the page source)
    submit_form = soup.find_all('form', id='aspnetForm', name='aspnetForm')
    
    # capture all input tags
    input_tags = soup.find_all('input')
    
    # initialize form_data object
    form_data = {}
    
    for input_tag in input_tags:
        if input_tag.get('name') == 'hiddenDownloadFile':
            # set the hiddenDownloadFile to today's file
            form_data[input_tag.get('name')] = 'Criminal\\%s CrimDisposDaily_withHeadings.txt'%(datetime.datetime.today().strftime('%Y-%m-%d'))
            
        else:
            form_data[input_tag.get('name')] = input_tag.get('value')
    
    # post request - simulate the function DownloadDoc(filePath) on http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx
    try:
        r = requests.post('http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx', data=form_data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise
        # return Response.make_error_resp(msg=err.args[0], type=err.__class__.__name__, code=r.status_code)
    except requests.exceptions.RequestException as err:
        raise
        # return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=r.status_code) 
    
    filename = '%s_criminal_disposition.txt'%(datetime.datetime.today().strftime('%Y-%m-%d'))
    
    # create the directory if it doesn't exist
    if not os.path.exists(os.path.dirname(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))):
        try:
            os.makedirs(os.path.dirname(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)))
        except Exception as err: 
           raise
           # return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=None) 
    
    # save the requested file to disk        
    with open(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename), 'wb') as f:
        f.write(r.content)
    
    # file downloaded and saved
    return True

def delete_todays_disposition():
    """
    Delete the downloaded daily disposition file from the disk
    """
    filename = '%s_criminal_disposition.txt'%(datetime.datetime.today().strftime('%Y-%m-%d'))
    
    try:
        os.remove(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))
    except OSError:
        raise
    
    return True

def download_disposition_report_by_date(datetime_obj):
    """
    Download the daily disposition file from 
    http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx
    by date passed as a parameter and save it to disk
    """
    date = datetime_obj.strftime('%Y-%m-%d')
    
    # request the Harris County District Clerk public dataset page
    try:
        response = requests.get('http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx')
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise
        # return Response.make_error_resp(msg=err.args[0], type=err.__class__.__name__, code=response.status_code)
    except requests.exceptions.RequestException as err:
        raise
        # return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=response.status_code)  
    
    # create a BeautifulSoup object with the content of the response
    soup = bs4.BeautifulSoup(response.text)
    
    # capture the form (name and id attributes hardcoded, they were found by looking at the page source)
    submit_form = soup.find_all('form', id='aspnetForm', name='aspnetForm')
    
    # capture all input tags
    input_tags = soup.find_all('input')
    
    # initialize form_data object
    form_data = {}
    
    for input_tag in input_tags:
        if input_tag.get('name') == 'hiddenDownloadFile':
            # set the hiddenDownloadFile to today's file
            form_data[input_tag.get('name')] = 'Criminal\\%s CrimDisposDaily_withHeadings.txt'%(date)
            
        else:
            form_data[input_tag.get('name')] = input_tag.get('value')
    
    # post request - simulate the function DownloadDoc(filePath) on http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx
    try:
        r = requests.post('http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx', data=form_data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise
        # return Response.make_error_resp(msg=err.args[0], type=err.__class__.__name__, code=r.status_code)
    except requests.exceptions.RequestException as err:
        raise
        # return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=r.status_code) 
    
    filename = '%s_criminal_disposition.txt'%(date)
    
    # create the directory if it doesn't exist
    if not os.path.exists(os.path.dirname(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))):
        try:
            os.makedirs(os.path.dirname(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)))
        except Exception as err: 
           raise
           # return Response.make_error_resp(msg=str(err), type=err.__class__.__name__, code=None) 
    
    # save the requested file to disk        
    with open(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename), 'wb') as f:
        f.write(r.content)
    
    # file downloaded and saved
    return True

def delete_disposition_report_by_date(datetime_obj):
    """
    Delete a disposition file from the disk by date
    """
    
    date = datetime_obj.strftime('%Y-%m-%d')
    
    filename = '%s_criminal_disposition.txt'%(date)
    
    try:
        os.remove(op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))
    except OSError:
        raise
    
    return True

def parse_disposition_data_by_date(datetime_obj):
    """
    Parse the downloaded disposition data file by date
    """
    date = datetime_obj.strftime('%Y-%m-%d')
    filename = '%s_criminal_disposition.txt'%(date)
    filepath = op.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)
    
    # initialize a dictionary of the txt file
    disposition_data = []
    
    # read the disposition_data file
    try:   
        with open(filepath, 'r') as f:
            for line in f:
                file_line = line.split('\t')
                disposition_data.append(file_line)
    except EnvironmentError:
        raise
    
    # open attribute names data file
    try: 
        with open(op.path.join(HCDC_DATA_PATH, 'hcdc_criminal_disposition_attribute_names.json'), 'r') as f:
            disposition_attributes = json.load(f)
    except EnvironmentError:
        raise
    
    # loop through each row of the disposition data
    for i, disposition_row in enumerate(disposition_data, start=1):
        
        # header is the first line of the array
        header = txt_array[0]
        
        # create a new criminal disposition
        disposition = Disposition()
        
        # map the header values to the disposition row values 
        for j, header_attr in enumerate(header):
            
            # setattr api: setattr(object, name, value)
            setattr(disposition, disposition_attributes[header_attr], disposition_row[j])
    
        # add the disposition to the database session
        db.session.add(disposition)
    
    # save database session to the database
    db.session.commit()
    
    return True