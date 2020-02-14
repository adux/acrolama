# Pillow Compress
import sys
import os.path
import PIL.Image

from io import BytesIO

from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

"""
Thumbnail
https://stackoverflow.com/questions/23922289/django-pil-save-thumbnail-version-right-when-image-is-uploaded
"""

class Image(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=230, null=True, blank=True)
    image = models.ImageField(
        upload_to="images/",
        height_field="image_height",
        width_field="image_width",
    )
    thumbnail = models.ImageField(upload_to='images/thumbs/', editable=False)
    image_height = models.PositiveIntegerField(null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        if not self.image.closed:
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')
        super(Image, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = PIL.Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.thumbnail(
            settings.IMAGE_SIZE[0],
            PIL.Image.ANTIALIAS
        )
        imageTemproary.save(
            outputIoStream,
            format="JPEG",
            quality=75,
            subsampling=0,
            optimize=True,
        )
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(
            outputIoStream,
            "ImageField",
            "%s.jpg" % image.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(outputIoStream),
            None,
        )
        return image

    def formImage(self):
        """
        evaluate if dimension are good for portfolio
        """
        proportions = self.image_height / self.image_width

        if proportions == 1:
            form = "square"
        elif proportions == 0.5:
            form = "landscape"
        elif proportions == 2:
            form = "vertical"
        else:
            form = "not"
        return form

    def make_thumbnail(self):
        image = PIL.Image.open(self.image)
        image.thumbnail(settings.THUMB_SIZE[0], PIL.Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(
            thumb_filename,
            ContentFile(temp_thumb.read()),
            save=False
        )

        temp_thumb.close()

        return True

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

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Video, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = PIL.Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.thumbnail(
            (1170,1170),
            PIL.Image.ANTIALIAS
        )
        width, height = imageTemproary.size   # Get dimensions

        left = (width - 600)/2
        top = (height - 300)/2
        right = (width + 600)/2
        bottom = (height + 300)/2

        # Crop the center of the image
        imageTemproaryCrop = imageTemproary.crop((left, top, right, bottom))

        imageTemproaryCrop.save(
            outputIoStream,
            format="JPEG",
            quality=60,
            subsampling=0,
            optimize=True,
        )
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(
            outputIoStream,
            "ImageField",
            "%s.jpg" % image.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(outputIoStream),
            None,
        )
        return image
