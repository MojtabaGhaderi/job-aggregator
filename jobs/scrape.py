    import requests
    from bs4 import BeautifulSoup
    from jobs.models import JobListing

    def scrape_jobs():
        url = 'https://www.linkedin.com/jobs/search/?keywords=Python%20Developer'
        headers = {'User-Agent': 'Mozilla/5.0'} # Set a user agent to mimic a browser request
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')  # parse
        jobs = soup.find_all('div', class_='base-card')  # find the jobs

        for job in jobs[:10]:  # cause we want latest 10 jobs
            try:
                title = job.find('h3').text.strip()
                company = job.find('h4').text.strip()
                link = job.find('a')['href']

                # now save or update the job listing in the database
                JobListing.objects.update_or_create(
                    title=title,
                    company=company,
                    link=link
                )
            except AttributeError:
                continue