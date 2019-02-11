from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save
from home.utils import unique_slug_generator
from .forms import ArrayAdminForm
###Reference Data

EVENTCATEGORY = [
    ('MC','Masterclass'),
    ('FS','Festival'),
    ('CY','Cycle'),
    ('WS','Workshop'),
    ('CA','Camp'),
    ('RT','Retreat'),
]

EXCEPTIONCATEGORY = [
    ('TI','Time'),
    ('LO','Location'),
]

LEVEL = [
    ('0', 'Multilevel'),
    ('1', 'Introduction'),
    ('2', 'Intermediate'),
    ('3', 'Advanced'),
    ('4', 'Profesional'),
]

DAYS = [
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
    ('6', 'Sunday'),
]


class Day(models.Model):
    day = models.CharField(max_length=10, choices=DAYS)
    def __str__(self):
        return '(%s) %s' % (self.day, self.get_day_display())


class TimeOption(models.Model):
    form = ArrayAdminForm
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    days = models.ForeignKey(Day, null=True, blank=True, on_delete=models.CASCADE)
    start_interval = ArrayField(
        models.CharField(max_length=5)
    )
    open_interval = ArrayField(
        models.CharField(max_length=5)
    )
    start_date = models.DateField(auto_now_add=False, auto_now=False, blank=True,null=True)
    end_date = models.DateField(auto_now_add=False, auto_now=False, blank=True,null=True)
    def __str__(self):
        return '%s - %s' % (self.name, self.start_interval)


class PriceOption(models.Model):
    abonament = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    reduction = models.BooleanField(default=False)
    price_CHF = models.CharField(max_length=5, null=True, blank=True)
    price_EURO = models.CharField(max_length=5, null=True, blank=True)
    def __str__(self):
        return '%s - %s' % (self.name, self.price_CHF)


class Level (models.Model):
    name = models.CharField(max_length=20, choices=LEVEL)
    description = models.TextField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.ForeignKey('home.Address', on_delete=models.CASCADE)
    image = models.ForeignKey('media.Image', on_delete=models.CASCADE)
    max_participants = models.CharField(max_length=5,null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    indication = models.TextField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return self.name


class TimeLocation(models.Model):
    timeoptions = models.ManyToManyField(TimeOption)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return '%s, %s' % (self.location, self.timeoptions)


class Team(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='team/', null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True,null=True)
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    manager = models.ManyToManyField(Team)
    todo = models.CharField(max_length=120, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Policy(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    def __str__(self):
        return self.name


class Exception(models.Model):
    category = models.CharField(max_length=15, choices=EXCEPTIONCATEGORY)
    start_date = models.DateField(auto_now=False,auto_now_add=False)
    end_date = models.DateField(auto_now=False,auto_now_add=False)
    def __str__(self):
        return '%s, %s' % (self.start_date, self.category)


class Event(models.Model):
    #References
    categorie = models.CharField(max_length=50, choices=EVENTCATEGORY)
    #Own
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    #locations = models.ManyToManyField(Location)
    #Date
    eventstart_date = models.DateField(auto_now=False,auto_now_add=False)
    eventend_date = models.DateField(auto_now=False,auto_now_add=False)
    timelocation = models.ManyToManyField(TimeLocation)
    #Price
    priceoptions = models.ManyToManyField(PriceOption)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    max_participants = models.CharField(max_length=5, null=True, blank=True)
    #timeoptions = models.ManyToManyField(TimeOption)
    #Media
    images = models.ManyToManyField('media.Image')
    videos = models.ManyToManyField('media.Video', blank=True)
    #Optional
    prerequisites = models.TextField(max_length=2000, null=True, blank=True)
    highlights = models.TextField(max_length=2000, null=True, blank=True)
    included = models.TextField(max_length=2000, null=True, blank=True)
    food = models.TextField(max_length=2000, null=True, blank=True)
    #config
    team = models.ManyToManyField(Team)
    #accounting = models.ManyToManyField('accounting.Accounting')
    published = models.BooleanField()
    registration = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def event_pre_save_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)
        pre_save.connect(event_pre_save_receiver, sender=Event)
