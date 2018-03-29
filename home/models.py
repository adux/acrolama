from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from home.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class AboutMember(models.Model):
    name        = models.CharField(max_length=30)
    position    = models.CharField(max_length=30)
    content     = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class AboutGeneral(models.Model):
    description = models.TextField(max_length=300)

class AboutDate(models.Model):
    start       = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    end         = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    description = models.CharField(max_length=50)
    def yearstart(self):
        return self.start.strftime('%b %Y')
    def yearend(self):
            return self.end.strftime('%Y')

class Event(models.Model):
    Icon = (
        ('fas fa-redo','Masterclass'),
        ('fas fa-rocket','Festival'),
        ('fas fa-cogs','Cycle'),
        ('fas fa-cog','Workshop'),
        ('fas fa-star','Camp'),
        ('fas fa-star','Retreat'),
    )
    Ocurrance = (
        ('Wed','Wednesday\'s'),
        ('Thu','Thursday\'s'),
        ('Sun','Sunday\'s'),
        ('WedSun.','Wed. & Sunday\'s'),
        ('Year','Yearly'),
        ('One','One Time'),
    )
    Level = (
        ('A', 'Advanced'),
        ('B', 'Intermediate'),
        ('C', 'Introdution'),
        ('Z', 'Multilevel'),
    )

    cat             = models.CharField(max_length=13, choices=Icon, default=1)
    level           = models.CharField(max_length=1, choices=Level, default=1)
    title           = models.CharField(max_length=60)
    description     = models.TextField(max_length=300)
    prerequisites   = models.TextField(max_length=300, null=True, blank=True)
    location        = models.CharField(max_length=60)
    city            = models.CharField(max_length=20)
    ocurrance       = models.CharField(max_length=8, choices=Ocurrance, null=True,blank=True)
    datestart       = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    dateend         = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    price           = models.CharField(max_length=20, null=True, blank=True)
    publication     = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    slug            = models.SlugField(unique=True, null=True,blank=True)

    def get_datestart(self):
        if self.datestart.strftime('%b') == self.dateend.strftime('%b') and self.dateend.strftime('%d %b') != self.datestart.strftime('%d %b'):
            return self.datestart.strftime('%d')
        else:
            return self.datestart.strftime('%d %b')
    def get_timestart(self):
        return self.datestart.strftime('%H:%M')
    def get_dateend(self):
        if self.dateend.strftime('%d %b') == self.datestart.strftime('%d %b'):
            return self.dateend.strftime('')
        else:
            return self.dateend.strftime(' - %d %b')
    def get_timeend(self):
        return self.dateend.strftime('%H:%M')
    def __str__(self):
        return self.title

''' Signal of Django to generate slug if not created  '''
def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(event_pre_save_receiver,sender=Event)

class Testimonial(models.Model):
    text = models.TextField(max_length=350)
    author = models.CharField(max_length=30)
    def __str__(self):
        return self.author

class Portfolio(models.Model):
    owner           = models.ForeignKey(User)
    text            = models.TextField(max_length=30,blank=True,null=True)
    sec_text        = models.TextField(max_length=30,blank=True,null=True)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    upload          = models.ImageField(upload_to='portfolio/')
    def __str__(self):
        return self.text

