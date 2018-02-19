from django.db import models

# Create your models here.

class Clase(models.Model):
    CLASS_TYPE = (
        ('CY', 'Cycle'),
        ('WO', 'Workshop'),
        ('FE', 'Festival'),
    )
    name   = models.CharField(max_length=120)
    class_type      = models.CharField(max_length=2, choices=CLASS_TYPE)
    location        = models.CharField(max_length=120, blank=True, null=True)
    date            = models.DateField()
    enddate         = models.DateField()
    exception       = models.DateField()
    description     = models.CharField(max_length=300)
