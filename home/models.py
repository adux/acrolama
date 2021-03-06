import sys
import os.path
import PIL.Image

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from home.utils import unique_slug_generator


# Static Content of Webpage
# Start About Section


class AboutImage(models.Model):
    image = models.ForeignKey("audiovisual.Image", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.title


class AboutTeam(models.Model):
    team = models.ForeignKey("users.User", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team.first_name


class AboutDate(models.Model):
    start = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description = models.CharField(max_length=50)

    def yearstart(self):
        return self.start.strftime("%b %Y")

    def yearend(self):
        return self.end.strftime("%Y")

    def __str__(self):
        return self.description


# Start FAQ Section
class Faq(models.Model):
    question = models.CharField(max_length=300, null=True, blank=True)
    answer = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.question


# Start Variable Info Pages
class Info(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("info", args=[str(self.slug)])


def info_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(info_pre_save_receiver, sender=Info)


class InfoImage(models.Model):
    image = models.ForeignKey("audiovisual.Image", on_delete=models.CASCADE)
    general = models.ForeignKey(Info, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.title


class NewsList(models.Model):
    """
    TODO: I want to automatize this with a job that takes the next 3 events, with workshops
    as preferences and sets it every week?
    Cleans, image included, the previous events, so only 3 are used.
    """

    event = models.ForeignKey("project.Event", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="news/")
    thumbnail = models.ImageField(upload_to="news/thumbs/", editable=False)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.event.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        if not self.image.closed:
            if not self.make_thumbnail():
                raise Exception("Could not create thumbnail - is the file type valid?")
        super(NewsList, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = PIL.Image.open(image).convert("RGB")
        outputIoStream = BytesIO()
        imageTemproary.thumbnail((900, 300), PIL.Image.ANTIALIAS)
        imageTemproary.save(
            outputIoStream, format="WEBP", quality=75, subsampling=0, optimize=True,
        )
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(
            outputIoStream,
            "image",
            "%s.webp" % image.name.split(".")[0],
            "image/webp",
            sys.getsizeof(outputIoStream),
            None,
        )
        return image

    def make_thumbnail(self):
        image = PIL.Image.open(self.image).convert("RGB")
        image.thumbnail((450, 150), PIL.Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_filename = thumb_name + "_thumb.jpg"

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, "JPEG")
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)

        temp_thumb.close()

        return True


class Portfolio(models.Model):
    image = models.ForeignKey("audiovisual.Image", on_delete=models.CASCADE)
    order = models.CharField(max_length=1, blank=True, null=True)
    text = models.TextField(max_length=30, blank=True, null=True)
    sec_text = models.TextField(max_length=30, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.title


class Testimonial(models.Model):
    text = models.TextField(max_length=350)
    author = models.CharField(max_length=30)

    def __str__(self):
        return self.text
