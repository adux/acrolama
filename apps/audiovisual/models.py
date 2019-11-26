from django.db import models

#Pillow Compress
import sys
import  PIL.Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Image(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=230, null=True, blank=True)
    image = models.ImageField(upload_to="images/")

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Image, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = PIL.Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.thumbnail((1600,1170), PIL.Image.ANTIALIAS)
        imageTemproary.save(outputIoStream , format='JPEG', quality=90, optimize=True)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image

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
