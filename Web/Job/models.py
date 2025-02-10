from django.db import models

# Create your models here.


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    details = models.TextField()
