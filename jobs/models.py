from django.db import models

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return f"{self.title} at {self.company}"