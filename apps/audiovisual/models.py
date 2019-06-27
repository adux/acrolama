from django.db import models


class Image(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=230, null=True, blank=True)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title


class Video(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=230, null=True, blank=True)
    link = models.CharField(max_length=300)
    image = models.ImageField(upload_to="videos/")

    def __str__(self):
        return self.title
