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
    image = models.ImageField(
        upload_to="images/",
        height_field='image_height',
        width_field='image_width'
    )
    image_height = models.PositiveIntegerField(null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Image, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = PIL.Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.thumbnail(
            (1170,2340),
            PIL.Image.ANTIALIAS
        )
        imageTemproary.save(
            outputIoStream,
            format='JPEG',
            quality=90,
            optimize=True
        )
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(
            outputIoStream,'ImageField',
            "%s.jpg" % image.name.split('.')[0], 'image/jpeg',
            sys.getsizeof(outputIoStream),
            None
        )
        return image

    def formImage(self):
        """
        evaluate if dimension are good for portfolio
        """
        proportions = self.image_height/self.image_width

        if proportions == 1:
            form = "square"
        elif proportions == 0.5:
            form = "landscape"
        elif proportions == 2:
            form = "vertical"
        else:
            form = "not"
        return form


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
