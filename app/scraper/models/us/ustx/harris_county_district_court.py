"""Scraper models."""

from app.scraper.models.us.ustx.constants import HCDC_CRIMINAL_DISPOSITION_PATH
from app.scraper.models.us.ustx.constants import HCDC_CRIMINAL_FILING_PATH
from app.scraper.models.us.ustx.constants import HCDC_DATA_PATH
from app.extensions import db
from dateutil.parser import parse

import bs4
import csv
import datetime
import errno
import json
import os
import pytz
import requests


class HarrisCountyDistrictCourtScraper(object):
    """Scraper class.

    Download, parse, and delete criminal data from public datasets.
    """

    time_zone = pytz.timezone(os.getenv('TIMEZONE', 'America/Chicago'))

    def __init__(self):
        """__init__ method.

        Method undefined
        """
        pass

    def __repr__(self):
        """__repr__ method.

        Print a string representation of the Python object to be parsed by the
        Python interpreter.
        """
        pass

    @staticmethod
    def download_disposition_report_by_date(datetime_obj, cb=None):
        """Download the daily disposition file.

        File downloaded from
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
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # capture all input tags
        input_tags = soup.find_all('input')

        # initialize form_data object
        form_data = {}

        for input_tag in input_tags:
            if input_tag.get('name') == 'hiddenDownloadFile':
                # set the hiddenDownloadFile to today's file
                form_data[input_tag.get('name')] = 'Criminal\\{} CrimDisposDaily_withHeadings.txt'.format(date)

            else:
                form_data[input_tag.get('name')] = input_tag.get('value')

        # post request - simulate the function DownloadDoc(filePath)
        # on http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx
        try:
            r = requests.post('http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx', data=form_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.RequestException:
            raise

        filename = '{}_criminal_disposition.txt'.format(date)

        # check the response for a dataset file
        # responses with attachements include the Content-Disposition header
        # and the header Content-Type: text/plain
        if 'Content-Disposition' not in r.headers:
            # raise a file not found exception
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

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
        if cb:
            res = cb(datetime_obj)
            return res
        else:
            return True

    @staticmethod
    def download_filing_report_by_date(datetime_obj, cb=None):
        """Download the daily filing file.

        File downloaded from
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
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # capture all input tags
        input_tags = soup.find_all('input')

        # initialize form_data object
        form_data = {}

        for input_tag in input_tags:
            if input_tag.get('name') == 'hiddenDownloadFile':
                # set the hiddenDownloadFile to today's file
                form_data[input_tag.get('name')] = 'Criminal\\{} CrimFilingsDaily_withHeadings.txt'.format(date)

            else:
                form_data[input_tag.get('name')] = input_tag.get('value')

        # post request - simulate the function DownloadDoc(filePath)
        # on http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx
        try:
            r = requests.post('http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx', data=form_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.RequestException:
            raise

        filename = '{}_criminal_filing.txt'.format(date)

        # check the response for a dataset file
        # responses with attachements include the Content-Disposition header
        # and the header Content-Type: text/plain
        if 'Content-Disposition' not in r.headers:
            # raise a file not found exception
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

        # create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(os.path.join(HCDC_CRIMINAL_FILING_PATH, filename))):
            try:
                os.makedirs(os.path.dirname(os.path.join(HCDC_CRIMINAL_FILING_PATH, filename)))
            except OSError:
                raise

        # save the requested file to disk
        with open(os.path.join(HCDC_CRIMINAL_FILING_PATH, filename), 'wb') as f:
            f.write(r.content)

        # file downloaded and saved
        if cb:
            res = cb(datetime_obj)
            return res
        else:
            return True

    @classmethod
    def parse_disposition_data_by_date(cls, datetime_obj):
        """Parse the downloaded disposition data file by date."""
        date = datetime_obj.strftime('%Y-%m-%d')
        filename = '{}_criminal_disposition.txt'.format(date)
        filepath = os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename)

        # initialize a dictionary of the txt file
        disposition_data = []

        # open attribute names data file
        try:
            with open(os.path.join(HCDC_DATA_PATH, 'hcdc_criminal_disposition_attribute_names.json'), 'r') as f:
                disposition_attributes = tuple(json.load(f).values())
        except EnvironmentError:
            raise

        # read the disposition_data file
        try:
            # http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
            with open(filepath, 'r', encoding='latin-1', errors='backslashreplace', newline='') as f:
                reader = csv.DictReader(f, fieldnames=disposition_attributes, delimiter='\t')
                for row in reader:
                    disposition_data.append(row)
        except EnvironmentError:
            raise

        # loop through each disposition entry and clean up data before saving
        for record in disposition_data[1:]:
            # initialize the criminal disposition record
            disposition_record = {}
            # save record creation dates
            disposition_record['created_on'] = datetime.datetime.utcnow()
            disposition_record['last_modified'] = datetime.datetime.utcnow()
            # iterate across the dictionary
            for key, val in record.items():
                # convert dates to datetime objects
                if 'date' in key:
                    try:
                        # localized datetime
                        local_datetime = cls.time_zone.localize(parse(val.rstrip()))
                        disposition_record[key] = local_datetime
                    except ValueError:
                        # save an unrealistic date
                        disposition_record[key] = datetime.datetime.max
                elif 'bond_amount' in key:
                    # only bond amount is an integer
                    disposition_record[key] = int(val.rstrip())
                else:
                    # everything else is a string
                    disposition_record[key] = val.rstrip()

            # add the disposition to the database
            try:
                db['dispositions'].insert_one(disposition_record)
            except Exception:
                raise

        return True

    @classmethod
    def parse_filing_data_by_date(cls, datetime_obj):
        """Parse the downloaded filing data file by date."""
        date = datetime_obj.strftime('%Y-%m-%d')
        filename = '{}_criminal_filing.txt'.format(date)
        filepath = os.path.join(HCDC_CRIMINAL_FILING_PATH, filename)

        # initialize a dictionary of the txt file
        filing_data = []

        # open attribute names data file
        try:
            with open(os.path.join(HCDC_DATA_PATH, 'hcdc_criminal_filing_attribute_names.json'), 'r') as f:
                filing_attributes = tuple(json.load(f).values())
        except EnvironmentError:
            raise

        # read the filing data file
        try:
            # http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
            with open(filepath, 'r', encoding='latin-1', errors='backslashreplace', newline='') as f:
                reader = csv.DictReader(f, fieldnames=filing_attributes, delimiter='\t')
                for row in reader:
                    filing_data.append(row)
        except EnvironmentError:
            raise

        # loop through each disposition entry and clean up data before saving
        for record in filing_data[1:]:
            # initialize the criminal disposition record
            filing_record = {}
            # save record creation dates
            filing_record['created_on'] = datetime.datetime.utcnow()
            filing_record['last_modified'] = datetime.datetime.utcnow()
            # iterate across the dictionary
            for key, val in record.items():
                # convert dates to datetime objects
                if 'date' in key:
                    try:
                        # localized datetime
                        local_datetime = cls.time_zone.localize(parse(val.rstrip()))
                        filing_record[key] = local_datetime
                    except ValueError:
                        # save an unrealistic date
                        filing_record[key] = datetime.datetime.max
                elif 'bond_amount' in key:
                    # only bond amount is an integer
                    filing_record[key] = int(val.rstrip())
                else:
                    # everything else is a string
                    filing_record[key] = val.rstrip()

            # add the filing to the database
            try:
                db['filings'].insert_one(filing_record)
            except Exception:
                raise

        return True

    @staticmethod
    def delete_disposition_report_by_date(datetime_obj):
        """Delete a disposition file from the disk by date."""
        date = datetime_obj.strftime('%Y-%m-%d')

        filename = '{}_criminal_disposition.txt'.format(date)

        try:
            os.remove(os.path.join(HCDC_CRIMINAL_DISPOSITION_PATH, filename))
        except OSError:
            raise

        return True

    @staticmethod
    def delete_filing_report_by_date(datetime_obj):
        """Delete a filing file from the disk by date."""
        date = datetime_obj.strftime('%Y-%m-%d')

        filename = '{}_criminal_filing.txt'.format(date)

        try:
            os.remove(os.path.join(HCDC_CRIMINAL_FILING_PATH, filename))
        except OSError:
            raise

        return True
