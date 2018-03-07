from django.db import models

# Create your models here.


class Workshop(models.Model):
    date            = models.DateField(auto_now=False, auto_now_add=False)
    time            = models.CharField(max_length=10)
    teachers        = models.TextField(max_length=120, blank=True, null=True)
    workshop        = models.TextField(max_length=300, blank=True, null=True)
    prerequisites   = models.TextField(max_length=300, blank=True, null=True)
    def day(self):
        return self.date.strftime('%A')

