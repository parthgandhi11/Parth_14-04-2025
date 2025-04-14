from django.db import models

# Create your models here.
class MenuHours(models.Model):
    store_id=models.CharField()
    dayOfWeek=models.IntegerField()
    start_time_local=models.TimeField()
    end_time_local=models.TimeField()