from django.db import models

# Create your models here.
class StoreStatus(models.Model):
    store_id=models.CharField()
    status=models.CharField()
    timestamp_utc=models.DateTimeField()