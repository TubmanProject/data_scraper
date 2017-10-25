from ..extensions import BaseDB, db
from ..config import HCDC_CRIMINAL_DISPOSITION_PATH, HCDC_CRIMINAL_FILING_PATH, HCDC_DATA_PATH

import os
import datetime
import json
import datetime
import requests
import bs4

class Dispositions(BaseDB):
    
    # tablename
    __tablename__ = 'dispositions'
    
    # table columns
    rundate                                 = db.Column(db.DateTime, nullable=False)
    court_division_indicator_code           = db.Column(db.Integer, db.ForeignKey('court_division_indicator.code'), nullable=False)
    case_number                             = db.Column(db.Integer, nullable=False)
    filing_date                             = db.Column(db.DateTime, nullable=True)
    instrument_type_code                    = db.Column(db.VARCHAR(3), db.ForeignKey('instrument_type.code'), nullable=False)
    case_disposition_code                   = db.Column(db.VARCHAR(4), db.ForeignKey('case_disposition.code'), nullable=False)
    court                                   = db.Column(db.Integer, nullable=False)
    case_status_code                        = db.Column(db.VARCHAR(1), db.ForeignKey('case_status.code'), nullable=False)
    defendant_status_code                   = db.Column(db.VARCHAR(1), db.ForeignKey('defendant_status.code'), nullable=False)
    bond_amount                             = db.Column(db.Integer, nullable=True)
    current_offense_code                    = db.Column(db.Integer, nullable=False)
    current_offense_definition              = db.Column(db.VARCHAR(255), nullable=True)
    current_offense_level_degree_code       = db.Column(db.VARCHAR(2), db.ForeignKey('current_offense_level_degree.code'), nullable=False)
    next_appearance_date                    = db.Column(db.DateTime, nullable=True)
    docket_calendar_name_code               = db.Column(db.VARCHAR(3), db.ForeignKey('docket_calendar_name.code'), nullable=True)
    calendar_reason_code                    = db.Column(db.VARCHAR(4), db.ForeignKey('calendar_reason.code'), nullable=True)
    defendant_name                          = db.Column(db.VARCHAR(255), nullable=True)
    defendant_spn                           = db.Column(db.Integer, nullable=False)
    defendant_race_code                     = db.Column(db.VARCHAR(1), db.ForeignKey('defendant_race.code'), nullable=True)
    defendant_sex                           = db.Column(db.VARCHAR(1), nullable=True)
    defendant_date_of_birth                 = db.Column(db.DateTime, nullable=True)
    defendant_street_number                 = db.Column(db.VARCHAR(10), nullable=True)
    defendant_street_name                   = db.Column(db.VARCHAR(255), nullable=True)
    defendant_city                          = db.Column(db.VARCHAR(255), nullable=True)
    defendant_state                         = db.Column(db.VARCHAR(255), nullable=True)
    defendant_zip_code                      = db.Column(db.VARCHAR(10), nullable=True)
    attorney_name                           = db.Column(db.VARCHAR(255), nullable=True)
    attorney_spn                            = db.Column(db.Integer, nullable=True)
    attorney_connection_code                = db.Column(db.VARCHAR(3), nullable=True)
    attorney_connection_definition          = db.Column(db.VARCHAR(255), nullable=True)
    disposition_date                        = db.Column(db.DateTime, nullable=True)
    disposition                             = db.Column(db.VARCHAR(255), nullable=True)
    sentence                                = db.Column(db.VARCHAR(255), nullable=True)
    complainant_name                        = db.Column(db.VARCHAR(255), nullable=True)
    complainant_agency                      = db.Column(db.VARCHAR(255), nullable=True)
    offense_report_number                   = db.Column(db.VARCHAR(255), nullable=True)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
    @classmethod
    def seed_db(cls):
        """
        Download past disposition reports from the HCDC Public Dataset website, parse them, and add to the database.
        Use the not_found counter to determine when there are no more past dataset remaining.
        The assumption is that when 14 days have passed and there are no dataset files available for download the end has been reach.
        14 days was chosen assuming that during the holiday break there may be several days where no reports have been published but not more than 14 days.
        """
        
        # initialize
        not_found = 0
        found = True
        date = datetime.datetime.today()
        
        # while 14 consecutive days of not being able to download a dataset
        while not_found <= 14:
            try:
                download_disposition_report_by_date(date)
            except:
                found = False
                not_found += 1  
            
            if found:
                # TODO: fix this
                # wait for the file to be downloaded
                filename = '%s_criminal_disposition.txt'%(date.strftime('%Y-%m-%d'))
                file_path = os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)
                while not os.path.exists(file_path):
                    time.sleep(1)
                
                not_found = 0
                try:
                    parse_disposition_data_by_date(date)
                except:
                    pass
            
            # reset and decrement date
            found = True
            date = date - datetime.timedelta(days=1)     
    
    @classmethod
    def parse_disposition_data_by_date(cls, datetime_obj):
        """
        Parse the downloaded disposition data file by date
        """
        date = datetime_obj.strftime('%Y-%m-%d')
        filename = '%s_criminal_disposition.txt'%(date)
        filepath = os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)
        
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
            with open(os.path.join(HCDC_DATA_PATH, 'hcdc_criminal_disposition_attribute_names.json'), 'r') as f:
                disposition_attributes = json.load(f)
        except EnvironmentError:
            raise
        
        # loop through each row of the disposition data
        for i, disposition_row in enumerate(disposition_data, start=1):
            
            # header is the first line of the array
            header = txt_array[0]
            
            # create a new criminal disposition
            disposition = cls()
            
            # map the header values to the disposition row values 
            for j, header_attr in enumerate(header):
                
                # setattr api: setattr(object, name, value)
                setattr(disposition, disposition_attributes[header_attr], disposition_row[j])
        
            # add the disposition to the database session
            db.session.add(disposition)
        
        # save database session to the database
        db.session.commit()
        
        return True
    
    @staticmethod
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
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.RequestException:
            raise  
        
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
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.RequestException:
            raise
        
        filename = '%s_criminal_disposition.txt'%(date)
        
        # create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))):
            try:
                os.makedirs(os.path.dirname(os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)))
            except OSError: 
               raise
        
        # save the requested file to disk        
        with open(os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename), 'wb') as f:
            f.write(r.content)
        
        # file downloaded and saved
        return True
    
    @staticmethod
    def delete_disposition_report_by_date(datetime_obj):
        """
        Delete a disposition file from the disk by date
        """
        
        date = datetime_obj.strftime('%Y-%m-%d')
        
        filename = '%s_criminal_disposition.txt'%(date)
        
        try:
            os.remove(os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))
        except OSError:
            raise
        
        return True
    