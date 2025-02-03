from django.test import TestCase
from django.test import Client
from jobs.models import JobListing
from unittest.mock import patch
from jobs.scrape import scrape_jobs
from jobs.tasks import daily_scrape



class JobListingModelTest(TestCase):
    def test_job_listing_creation(self):
        """
        Test that a JobListing instance can be created with valid data.
        """
        job = JobListing.objects.create(title="Python Developer", company="Example Corp", link="http://example.com")
        self.assertEqual(job.title, "Python Developer")
        self.assertEqual(job.company, "Example Corp")
        self.assertEqual(job.link, "http://example.com")



class JobListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        JobListing.objects.create(title="Python Developer", company="Example Corp", link="http://example.com")

    def test_job_list_view(self):
        """
        Test that the job_list view returns a 200 status code and has job listings in it.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")

    def test_search_functionality(self):
        """
        Test that the search bar filters jobs by title or company name.
        """
        response = self.client.get('/?q=Python')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")

        response = self.client.get('/?q=Example')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example Corp")


class ScrapeTest(TestCase):
    @patch('jobs.scrape.requests.get')
    def test_scrape_jobs(self, mock_get):
        """
        Test that the scrape_jobs function correctly parses HTML and saves job listings.
        """
        # Mock the linkdinn response
        mock_response = mock_get.return_value
        mock_response.text = '''
            <html>
                <div class="base-card">
                    <h3>Python Developer</h3>
                    <h4>Example Corp</h4>
                    <a href="http://example.com"></a>
                </div>
            </html>
        '''

        # call the scrape_jobs function
        scrape_jobs()

        self.assertEqual(JobListing.objects.count(), 1)
        job = JobListing.objects.first()
        self.assertEqual(job.title, "Python Developer")
        self.assertEqual(job.company, "Example Corp")
        self.assertEqual(job.link, "http://example.com")

class CeleryTaskTest(TestCase):
    @patch('jobs.tasks.scrape_jobs')
    def test_daily_scrape_task(self, mock_scrape_jobs):
        """
        Test that the daily_scrape task calls the scrape_jobs function.
        """
        daily_scrape.delay()  # Trigger the task
        mock_scrape_jobs.assert_called_once()