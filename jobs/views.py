from django.shortcuts import render
from .models import JobListing

def job_list(request):
    """
    displays a list of job listings and provides search functionality.

    - if a query parameter 'q' is provided, filters jobs by title or company name.
    - if not, displays all job listings.
    """
    query = request.GET.get('q', '')
    if query:
        jobs = JobListing.objects.filter(title__icontains=query) | JobListing.objects.filter(company__icontains=query)
    else:
        jobs = JobListing.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'query': query})