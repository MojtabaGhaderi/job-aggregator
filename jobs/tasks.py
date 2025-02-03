from celery import shared_task
from .scrape import scrape_jobs

@shared_task
def daily_scrape():
    scrape_jobs()