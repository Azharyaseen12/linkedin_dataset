from django.db import models

# Create your models here.

class Savesearches(models.Model):
    companies = models.CharField(max_length=100000)
    job_title = models.CharField(max_length=100000)
    current_url = models.CharField(max_length=1000000,default=None)
    results = models.IntegerField(default=0)

    def __str__(self):
        return self.companies
    
# class Profile(models.Model):
#     username = models.CharField(max_length=1000,default=None)
#     job_title = models.CharField(max_length=5000,default=None)

#     def __str__(self):
#         return self.username

class Email(models.Model):
    mesage = models.CharField(max_length=100000,default=None,null=True)
    date = models.DateField(auto_now_add=True)

class Companies(models.Model):
    company = models.CharField(max_length=500)

    def __str__(self):
        return self.company
class UkCompanies(models.Model):
    country = models.CharField(max_length=1000)
    linkedin_profile_link = models.CharField(max_length=1000)

    def __str__(self):
        return self.country