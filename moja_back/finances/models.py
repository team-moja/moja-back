from django.db import models
from django.conf import settings


# Create your models here.
class Bank(models.Model):
    bank_name = models.CharField(max_length=255)
    bank_url = models.CharField(max_length=255)