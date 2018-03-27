from django.db import models

# Create your models here.


class UFoodDB(models.Model):
    ID = models.CharField(max_length=100, primary_key=True)
    ProductID = models.TextField(max_length=200)
    Size = models.TextField(max_length=500)
    Produce = models.TextField(max_length=500)
        
    def __unicode__(self):
        return self.title
