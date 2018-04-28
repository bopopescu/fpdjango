from django.db import models

# Create your models here.

class UFoodDB(models.Model):
    Description = models.TextField(max_length=500,blank=True,primary_key=False)
    Cases = models.CharField(max_length=25, blank=True,primary_key=False)
    Hunmiles = models.CharField(max_length=10, blank=True,primary_key=False)
    Twohunmiles = models.CharField(max_length=10, blank=True,primary_key=False)
    Fivhunmiles = models.CharField(max_length=10, blank=True,primary_key=False)
    CsvMonth = models.TextField(max_length=200,blank=True,primary_key=False)
    CsvYear = models.TextField(max_length=200,blank=True,primary_key=False)
    Local = models.CharField(max_length=10, blank=True,primary_key=False)


    def __unicode__(self):
        return self.title