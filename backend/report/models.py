from django.db import models

# Create your models here.
class Report(models.Model):
    report_id=models.CharField(max_length=255,primary_key=True)
    status=models.CharField(max_length=255,default='Running')
    file=models.FileField(upload_to='reports/',blank=True,null=True)