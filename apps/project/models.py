from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save
from home.utils import unique_slug_generator
###Reference Data

EVENTCATEGORY = [
    ('fas fa-redo','Masterclass'),
    ('fas fa-rocket','Festival'),
    ('fas fa-cogs','Cycle'),
    ('fas fa-cog','Workshop'),
    ('fas fa-star','Camp'),
    ('fas fa-seeding','Retreat'),
]

EXCEPTIONCATEGORY = [
    ('TI','Time'),
    ('LO','Location'),
    ('TL','TimeLocation'),
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
        return '%s' % (self.get_day_display())


class TimeOption(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    regular_days = models.ForeignKey(Day, null=True, blank=True, on_delete=models.CASCADE)
    class_starttime = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    class_endtime = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    open_starttime = models.TimeField(auto_now=False, auto_now_add=False)
    open_endtime = models.TimeField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return '%s: %s - %s' % (self.name, self.open_starttime, self.open_endtime)


class PriceOption(models.Model):
    abonament = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    reduction = models.BooleanField(default=False)
    price_chf = models.CharField(max_length=5, null=True, blank=True)
    price_euro = models.CharField(max_length=5, null=True, blank=True)
    def __str__(self):
        return '%s - %s' % (self.name, self.price_chf)


class Level(models.Model):
    name = models.CharField(max_length=20, choices=LEVEL)
    description = models.TextField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.get_name_display()


class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE)
    image = models.ForeignKey('audiovisual.Image', on_delete=models.CASCADE)
    max_capacity = models.CharField(max_length=5,null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    indication = models.TextField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return '%s' % (self.address)


class TimeLocation(models.Model):
    time_options = models.ManyToManyField(TimeOption)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return " vs ".join(p.name for p in self.time_options.all()) 


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    manager = models.ManyToManyField('users.Staff')
    todo = models.CharField(max_length=120, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Policy(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    def __str__(self):
        return self.name


class Exception(models.Model):
    category = models.CharField(max_length=15, choices=EXCEPTIONCATEGORY)
    description = models.TextField(max_length=2000)
    time_location = models.ManyToManyField(TimeLocation)
    def __str__(self):
        return '%s, %s' % (self.description, self.category)


class Event(models.Model):
    category = models.CharField(max_length=50, choices=EVENTCATEGORY)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    event_startdate = models.DateField(auto_now_add=False, auto_now=False, blank=True,null=True)
    event_enddate = models.DateField(auto_now_add=False, auto_now=False, blank=True,null=True)
    description = models.TextField(max_length=3000)
    time_locations = models.ManyToManyField(TimeLocation)
    price_options = models.ManyToManyField(PriceOption)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    max_participants = models.CharField(max_length=5, null=True, blank=True)
    images = models.ManyToManyField('audiovisual.Image')
    videos = models.ManyToManyField('audiovisual.Video', blank=True)
    prerequisites = models.TextField(max_length=2000, null=True, blank=True)
    highlights = models.TextField(max_length=2000, null=True, blank=True)
    included = models.TextField(max_length=2000, null=True, blank=True)
    food = models.TextField(max_length=2000, null=True, blank=True)
    staff = models.ManyToManyField('users.Staff')
    teacher = models.ManyToManyField('users.Teacher')
    published = models.BooleanField()
    registration = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(event_pre_save_receiver, sender=Event)