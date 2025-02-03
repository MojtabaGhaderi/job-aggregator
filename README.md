# Job Aggregator Web App

## Overview
A Django-based web application that scrapes the latest 10 job postings for "Python Developer" from LinkedIn, displays them on a webpage, and allows filtering by title or company name.

## Installation
1. Clone the repository: `git clone <repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up Redis: Ensure Redis is installed and running.
6. Apply migrations: `python manage.py migrate`

## Running the Application
1. Start the development server: `python manage.py runserver`
2. Start Celery worker: `celery -A job_aggregator worker --loglevel=info`
3. Start Celery Beat: `celery -A job_aggregator beat --loglevel=info`

## Features
- Scrapes job listings daily at midnight.
- Displays job listings on a webpage.
- Provides a search bar to filter jobs by title or company name.

## Dependencies
- Django
- Celery
- Redis
- BeautifulSoup
- Requests

## Testing
Run tests using: `python manage.py test`
