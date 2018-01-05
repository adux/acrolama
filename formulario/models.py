from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class Fest(models.Model):
    name        = models.CharField(max_length=120)
    address     = models.CharField(max_length=250)
    numero      = models.CharField(max_length=20)
    email       = models.CharField(max_length=250)
    option      = models.CharField(max_length=5)
    allergies   = models.CharField(max_length=300)
    date        = models.DateField(auto_now_add=True)
    datetime    = models.DateTimeField(auto_now_add=True)
    update      = models.DateField(auto_now=True)

