"""Celery tasks for scraping data."""

from app.scraper.models.us.ustx.tasks import scrape_hcdc_disposition_today_task, scrape_hcdc_filing_today_task


def scrape_task():
    """Bundle task for scraping data."""
    scrape_hcdc_disposition_today_task()
    scrape_hcdc_filing_today_task()
