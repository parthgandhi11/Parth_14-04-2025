from django.db import models

# Create your models here.
class Timezones(models.Model):
    store_id=models.CharField(unique=True)
    timezone_str=models.CharField(default='America/Chicago')