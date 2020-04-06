from django.db import models
from django.db.models.signals import pre_save
from django.utils.functional import cached_property
from django.urls import reverse

from home.utils import unique_slug_generator

# Reference Data

EVENTCATEGORY = [
    ("MC", "Masterclass"),
    ("FT", "Festival"),
    ("CY", "Cycle"),
    ("WS", "Workshop"),
    ("CA", "Camp"),
    ("RT", "Retreat"),
]

EXCEPTIONCATEGORY = [
    ("TI", "Time"),
    ("LO", "Location"),
    ("TL", "TimeLocation"),
]

LEVEL = [
    ("0", "Multilevel"),
    ("1", "Introduction"),
    ("2", "Intermediate I"),
    ("3", "Intermediate II"),
    ("4", "Advanced"),
    ("5", "Profesional"),
]

CYCLE = [(i, i) for i in range(13)]

DAYS = [
    ("0", "Monday"),
    ("1", "Tuesday"),
    ("2", "Wednesday"),
    ("3", "Thursday"),
    ("4", "Friday"),
    ("5", "Saturday"),
    ("6", "Sunday"),
]

# TODO:not why i didn't use the days as a simple liest. Doesn't make much sense
class Day(models.Model):
    day = models.CharField(max_length=10, choices=DAYS)

    def __str__(self):
        return "%s" % (self.get_day_display())


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    manager = models.ManyToManyField("users.User")
    todo = models.CharField(max_length=120, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s | " % (self.name) + " - ".join(str(p.first_name) for p in self.manager.all())


class TimeOption(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    #this should be singular
    regular_days = models.ForeignKey(
        Day, null=True, blank=True, on_delete=models.CASCADE
    )
    class_starttime = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    class_endtime = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    open_starttime = models.TimeField(auto_now=False, auto_now_add=False)
    open_endtime = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        # return "%s" % (self.name)
        # Classes will have regular days
        if self.regular_days:
            return "%s, %s: %s - %s" % (
                self.name,
                self.regular_days,
                self.class_starttime.strftime("%H:%M"),
                self.class_endtime.strftime("%H:%M"),
            )
        # Events should not have and Name is used
        else:
            return "%s: %s - %s" % (
                self.name,
                self.open_starttime.strftime("%H:%M"),
                self.open_endtime.strftime("%H:%M"),
            )

    def get_class_start_times(self):
        return "%s - %s" % (
            self.class_starttime.strftime("%H:%M"),
            self.class_endtime.strftime("%H:%M"),
        )

    def get_open_start_times(self):
        return "%s - %s" % (
            self.open_starttime.strftime("%H:%M"),
            self.open_endtime.strftime("%H:%M"),
        )


class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.ForeignKey("address.Address", on_delete=models.CASCADE)
    image = models.ForeignKey("audiovisual.Image", on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField(default=2, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    indication = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)


class TimeLocation(models.Model):
    """
    time_options as a many to many was not the best desition ever probably
    it spears no practical time nor space
    """
    time_options = models.ManyToManyField(TimeOption)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return " - ".join(
            p.name for p in self.time_options.all()
        ) + " | %s" % (self.location)


class Irregularity(models.Model):
    category = models.CharField(max_length=15, choices=EXCEPTIONCATEGORY)
    description = models.TextField(max_length=2000)
    time_location = models.ManyToManyField(TimeLocation)

    class Meta:
        verbose_name_plural = "Irregularities"

    def __str__(self):
        return "%s, %s" % (self.description, self.category)


class PriceOption(models.Model):
    abonament = models.BooleanField(default=False)
    cycles = models.IntegerField(verbose_name="Numbero of Cycles")
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    reduction = models.BooleanField(default=False)
    price_chf = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_euro = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        if self.price_euro:
            return "%s, EUR: %s - CHF: %s" % (
                self.name,
                self.price_euro,
                self.price_chf,
            )
        else:
            return "%s, CHF: %s" % (self.name, self.price_chf)


# Sport Info
class Level(models.Model):
    name = models.CharField(max_length=20, choices=LEVEL)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.get_name_display()


class Discipline(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)

    class Meta:
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.name


class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=EVENTCATEGORY)
    cycle = models.IntegerField(
        default=0, choices=CYCLE, blank=True, null=True
    )
    title = models.CharField(max_length=100)
    event_startdate = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    event_enddate = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    description = models.TextField(max_length=3000)
    time_locations = models.ManyToManyField(TimeLocation)
    irregularities = models.ManyToManyField(Irregularity, blank=True)
    price_options = models.ManyToManyField(PriceOption)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField(default=2, null=True, blank=True)
    images = models.ManyToManyField("audiovisual.Image")
    videos = models.ManyToManyField("audiovisual.Video", blank=True)
    level = models.ForeignKey(
        Level, null=True, blank=True, on_delete=models.CASCADE
    )
    discipline = models.ForeignKey(
        Discipline, null=True, blank=True, on_delete=models.CASCADE
    )
    prerequisites = models.TextField(max_length=2000, null=True, blank=True)
    #TODO: change to teachers
    teacher = models.ManyToManyField("users.User", related_name="eventteacher")
    highlights = models.TextField(max_length=2000, null=True, blank=True)
    included = models.TextField(max_length=2000, null=True, blank=True)
    food = models.TextField(max_length=2000, null=True, blank=True)
    team = models.ManyToManyField(
        "users.User", related_name="eventteam", blank=True
    )
    published = models.BooleanField()
    registration = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    # class Meta:
    #     ordering = [""]

    @cached_property
    def fulltitle(self):
        if self.category == "CY" and self.cycle:
            if self.level.name == "2":
                return "Cycle 0." + str(self.cycle) + " - " + self.title
            elif self.level.name == "3":
                return "Cycle " + str(self.cycle) + " - " + self.title
            else:
                return self.title

    def get_absolute_url(self):
        if self.category == "CY":
            return reverse('class', args=[str(self.slug)])
        else:
            return reverse('event', args=[str(self.slug)])


    # @cached_property
    def __str__(self):
        if self.category == "CY":
            return "%s %s %s (%s) - %s" % (
                self.get_category_display(),
                self.level,
                self.cycle,
                self.event_startdate.strftime("%d %b"),
                self.title,
            )
        else:
            return "%s %s (%s) - %s" % (
                self.get_category_display(),
                self.level,
                self.event_startdate.strftime("%d %b"),
                self.title,
            )

# def event_pre_save_title(sender, instance, *args, **kwargs):


# pre_save.connect(event_pre_save_title, sender=Event)


def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(event_pre_save_receiver, sender=Event)
