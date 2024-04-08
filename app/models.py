from django.db import models

# Create your models here.

class Savesearches(models.Model):
    companies = models.CharField(max_length=100000)
    job_title = models.CharField(max_length=100000)
    current_url = models.CharField(max_length=1000000,default=None)
    results = models.IntegerField(default=0)

    def __str__(self):
        return self.companies
    