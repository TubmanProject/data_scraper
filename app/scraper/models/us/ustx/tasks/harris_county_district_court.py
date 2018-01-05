"""Celery tasks for scraping data."""

import datetime
import requests

from app.scraper.models.us.ustx import HarrisCountyDistrictCourtScraper
from app.extensions import celery
from celery import chain
from dateutil.parser import parse


class ScrapeTaskBaseClass(celery.Task):
    """Scrape Task Base Class."""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Error Handler."""
        # log the failure
        # use print(), as anything written to standard out/-err will be redirected to the logging system
        print('Task ID: {0} Error Type: {1} Error Message: {2} Error Traceback: {3}'.format(task_id,
                                                                                            exc.__class__.__name__,
                                                                                            str(exc),
                                                                                            einfo.traceback))


@celery.task(base=ScrapeTaskBaseClass)
def parse_disposition_data_by_date_task(isoformat_date):
    """Celery task to parse the downloaded disposition data file."""
    # convert isoformat_date back to datetime_obj
    datetime_obj = parse(isoformat_date)

    try:
        res = HarrisCountyDistrictCourtScraper().parse_disposition_data_by_date(datetime_obj)
        if res:
            date = datetime_obj.strftime('%Y-%m-%d')
            return date
    except EnvironmentError as err:
        # error reading the disposition data file or attribute names data file
        raise
    except Exception as err:
        # other error
        raise


@celery.task(base=ScrapeTaskBaseClass)
def download_disposition_report_by_date_task(isoformat_date):
    """Celery task to download the disposition data file."""
    # convert isoformat_date back to datetime_obj
    datetime_obj = parse(isoformat_date)

    try:
        res = HarrisCountyDistrictCourtScraper().download_disposition_report_by_date(datetime_obj)
        if res:
            date = datetime_obj.strftime('%Y-%m-%d')
            return date
    except requests.exceptions.HTTPError as err:
        # error requesting harris county website
        raise
    except requests.exceptions.RequestException as err:
        # error requesting harris county website
        raise
    except OSError as err:
        # file not found or error creating directory
        raise
    except Exception as err:
        # other error
        raise


@celery.task(base=ScrapeTaskBaseClass)
def delete_disposition_report_by_date_task(isoformat_date):
    """Celery task to delete the downloaded disposition data file."""
    # convert isoformat_date back to datetime_obj
    datetime_obj = parse(isoformat_date)

    try:
        res = HarrisCountyDistrictCourtScraper().delete_disposition_report_by_date(datetime_obj)
        if res:
            date = datetime_obj.strftime('%Y-%m-%d')
            return date
    except OSError as err:
        # unable to delete
        raise
    except Exception as err:
        # other error
        raise


@celery.task(base=ScrapeTaskBaseClass)
def parse_filing_data_by_date_task(isoformat_date):
    """Celery task to parse the downloaded disposition data file."""
    # convert isoformat_date back to datetime_obj
    datetime_obj = parse(isoformat_date)

    try:
        res = HarrisCountyDistrictCourtScraper().parse_filing_data_by_date(datetime_obj)
        if res:
            date = datetime_obj.strftime('%Y-%m-%d')
            return date
    except EnvironmentError as err:
        # error reading the disposition data file or attribute names data file
        raise
    except Exception as err:
        # other error
        raise


@celery.task(base=ScrapeTaskBaseClass)
def download_filing_report_by_date_task(isoformat_date):
    """Celery task to download the filing data file."""
    # convert isoformat_date back to datetime_obj
    datetime_obj = parse(isoformat_date)

    try:
        res = HarrisCountyDistrictCourtScraper().download_filing_report_by_date(datetime_obj)
        if res:
            date = datetime_obj.strftime('%Y-%m-%d')
            return date
    except requests.exceptions.HTTPError as err:
        # error requesting harris county website
        raise
    except requests.exceptions.RequestException as err:
        # error requesting harris county website
        raise
    except OSError as err:
        # file not found or error creating directory
        raise
    except Exception as err:
        # other error
        raise


@celery.task(base=ScrapeTaskBaseClass)
def delete_filing_report_by_date_task(isoformat_date):
    """Celery task to delete the downloaded filing data file."""
    # convert isoformat_date back to datetime_obj
    datetime_obj = parse(isoformat_date)

    try:
        res = HarrisCountyDistrictCourtScraper().delete_filing_report_by_date(datetime_obj)
        if res:
            date = datetime_obj.strftime('%Y-%m-%d')
            return date
    except OSError as err:
        # unable to delete
        raise
    except Exception as err:
        # other error
        raise


def scrape_disposition_today_task():
    """Scrape today's disposition report."""
    today = datetime.datetime.today()

    task = chain(download_disposition_report_by_date_task.si(today),
                 parse_disposition_data_by_date_task.si(today),
                 delete_disposition_report_by_date_task.si(today)).apply_async()

    data = {
        "task_id": task.id,
        "date": today.strftime('%Y-%m-%d'),
        "msg": "Asynchronous task to scrape disposition report for today started with a task id of {}.".format(task.id)
    }
    return data


def scrape_filing_today_task():
    """Scrape today's filing report."""
    today = datetime.datetime.today()

    task = chain(download_filing_report_by_date_task.si(today),
                 parse_filing_data_by_date_task.si(today),
                 delete_filing_report_by_date_task.si(today)).apply_async()

    data = {
        "task_id": task.id,
        "date": today.strftime('%Y-%m-%d'),
        "msg": "Asynchronous task to scrape filing report for today started with a task id of {}.".format(task.id)
    }
    return data
