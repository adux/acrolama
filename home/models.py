from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import pre_save
from home.utils import unique_slug_generator
from django.utils.translation import ugettext as _


# Static Content of Webpage
# Start About Section
class About(models.Model):
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.description


class AboutImage(models.Model):
    image = models.ForeignKey("audiovisual.Image", on_delete=models.CASCADE)
    general = models.ForeignKey(About, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class AboutTeam(models.Model):
    team = models.ForeignKey("users.User", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team.first_name


class AboutDate(models.Model):
    start = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    end = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
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
    email = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    inscribed_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email


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
